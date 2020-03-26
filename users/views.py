from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_verification_token, user_upgrade_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import get_user_model
import logging

def send_email_to_user(user_id, mail_subject, message, to_email):
    UserModel = get_user_model()
    try:        
        try:
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
        except email is None:
            logging.warning("Tried to send an invalid email")    

    except UserModel.DoesNotExist:
        logging.warning("Tried to send email to non-existing user '%s'" % user_id)

def profile(request, username):
    user = get_object_or_404(User, username=username)    

    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)

def register(request):

    if request.user.is_authenticated:
        return redirect("/profile")

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # help start
            current_site = get_current_site(request)
            mail_subject = 'thisBlog Sign-Up: Verify your email account'
            message = render_to_string('users/email_verify.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':email_verification_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_email_to_user(user.pk, mail_subject, message, to_email)
            # help end
            messages.success(request, f'Account created! You can now Log In using your credentials. Please check the verification email that we have sent your way.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def settings(request):
    
    if not request.user.profile.email_verified:
        messages.warning(request, f'Please verify your email address.')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def email_verify(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user2 = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user2.DoesNotExist):
        user2 = None
    if user2 is not None and email_verification_token.check_token(user2, token):
        user2.profile.email_verified = True
        user2.profile.save()
        user = request.user
        messages.success(request, f'Your email has been verified. You can now make a Post!')
        if (user.is_authenticated):
            if user.pk == user2.pk:
                return redirect('/profile')
            else:
                return redirect('/logout?next=/login')
        return redirect('/login')
    else:
        messages.warning(request, f'Email verification failed!')
        return redirect('/')


def user_upgrade(request, username, current):
    print(request.user.profile.PENDING_REQUEST_BECOME_INSTRUCTOR)

    if request.user.username == username:
        if request.user.profile.user_status == 1 and not request.user.profile.PENDING_REQUEST_BECOME_INSTRUCTOR:          
            
            # email start
            for admin in Profile.objects.filter(user_status=3):
                current_site = get_current_site(request)
                user = request.user
                mail_subject = 'thisBlog User Request: ' + user.username + ' wants to become an Instructor'
                message = render_to_string('users/email_user_upgrade_instructor.html', {
                    'admin': admin.user,
                    'user': user,
                    'request': 'Instructor',
                    'myurl': 'user_process_upgrade_instructor',
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':email_verification_token.make_token(user),
                })
                to_email = admin.user.email
                send_email_to_user.delay(admin.user.pk, mail_subject, message, to_email)
            # email end

            request.user.profile.PENDING_REQUEST_BECOME_INSTRUCTOR = True
            request.user.profile.save()
            messages.success(request, f'Your request to become an instructor has been submitted. You will be notified of our decision through email.')
            return redirect('profile')
        if request.user.profile.user_status == 2 and not request.user.profile.PENDING_REQUEST_BECOME_ADMIN:          
            request.user.profile.PENDING_REQUEST_BECOME_INSTRUCTOR = True
            messages.success(request, f'Your request to become an instructor has been submitted. You will be notified of our decision through email.')
            return redirect('profile')
    
    messages.add_message(request, messages.WARNING, f'Invalid Request')
    return redirect('profile')

def user_process_upgrade_instructor(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user2 = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user2.DoesNotExist):
        user2 = None
    if user2 is not None and user_upgrade_token.check_token(user2, token):
        user2.profile.email_verified = True
        user2.profile.save()
        user = request.user
        if user.is_authenticated:
            if user.profile.user_status==3:
                if user2.profile.user_status==1 and user2.profile.PENDING_REQUEST_BECOME_INSTRUCTOR==True:
                    user2.profile.PENDING_REQUEST_BECOME_INSTRUCTOR = False
                    user2.profile.user_status = 2
                    user2.profile.save()
                    
                    # notify user
                    current_site = get_current_site(request)
                    mail_subject = 'thisBlog Update: You have been granted Instructor level access'
                    message = 'Hi '+user2.username+',\n Congratulations! You have now become an Instructor.\n\n Log in now to see your status:\n http://'+current_site.domain+"/login?next=/user/"+user2.username
                    to_email = user2.email
                    send_email_to_user.delay(user2.pk, mail_subject, message, to_email)

                    messages.success(request, f'You have granted {user2.username} Instructor access')
                    return redirect('/')
                else:
                    messages.success(request, f'Link is No Longer Valid')
                    return redirect('/')
            else:
                messages.warning(request, f'Kindly sign in as an Admin to process this request')
                return redirect('/logout?next=/login?next='+request.path)
        else:
            messages.warning(request, f'Kindly sign in as an Admin to process this request')
            return redirect('/login?next='+request.path)
    else:
        messages.warning(request, f'Request cannot be processed')
        return redirect('/')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render, get_object_or_404, redirect


class FollowAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        pk = self.kwargs.get('pk')
        profile_second = get_object_or_404(Profile, pk=pk)
        profile = self.request.user.profile

        followed = False
        updated = False

        if self.request.user.is_authenticated and profile.pk != pk:
            if profile_second in profile.followings.all():
                profile.followings.remove(profile_second)
                profile.save()
                followed = False
                updated = True
            else:
                profile.followings.add(profile_second)
                profile.save()
                followed = True
                updated = True      
        
        data = {
            "updated": updated,
            "followed": followed,
        }
        return Response(data)
