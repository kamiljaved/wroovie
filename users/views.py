import logging
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import authentication, permissions
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import Profile
from .tokens import emailVerificationToken
from community.models import Membership
from common.views import getFeedContextMin

#####~~~~~ UTILITY FUNCTION ~~~~~#####
# sends an email to user-email
def sendEmailToUser(user_id, mail_subject, message, to_email):
    UserModel = get_user_model()
    try:        
        try:
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
        except Exception as e:
            logging.warning(f'Tried to send an invalid email: ${e}')    
    except UserModel.DoesNotExist:
        logging.warning("Tried to send email to non-existing user '%s'" % user_id)

#####~~~~~ UTILITY FUNCTION ~~~~~#####
# send email to user for verification
def sendAccountVerificationEmail(username=None):
    user = None
    # get user from db
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # cannot find user, TODO throw some error
        return
    username = user.username
    email = user.email
    mail_subject = 'wroovie signup: Verify Your EMAIL Account'
    message = render_to_string('users/email_verify.html', {
        'user': user,
        'domain': Site.objects.get_current().domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':emailVerificationToken.make_token(user),
    }) 
    sendEmailToUser(user.pk, mail_subject, message, email)

#####~~~~~ VIEW ~~~~~#####
# get user profile page
def profile(request, username):
    user = get_object_or_404(User, username=username)    
    req_page = request.GET.get('page')
    req_sort = request.GET.get('sort')

    page = "posts"
    sort = "top"

    if req_page is not None and req_page != "":
        if req_page == "comments":
            page = req_page
        elif request.user.is_authenticated:
            if req_page == 'upvoted' or req_page == "downvoted":
                page = req_page
            elif request.user == user:
                if req_page == 'saved':
                    page = req_page
                elif req_page == "editprofile":
                    return redirect('settings')
                elif user.administered_communities and req_page == "modpanel":
                    return redirect('modpanel')

    if req_sort is not None and req_sort != "":
        if req_sort == "latest":
            sort = req_sort

    context = {
        'profile_user': user,
        'profile': user.profile,
        'page': page,
        'sort': sort,
        'show_comm_info': True, # feed-view
    }
    
    # extra (sidebar) stuff
    if request.user == user:
        rec_memb = Membership.objects.filter(user=user).order_by('-dt_join')[:5]
        context['rec_memb'] = rec_memb
    return render(request, 'users/profile.html', context)

#####~~~~~ VIEW ~~~~~#####
# user and profile settings update view
@login_required
def settings(request):
    # warn user to verify email
    if not request.user.profile.email_verified:
        messages.warning(request, f'Please verify your email address.')
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile', request.user.username)
        else:
            context = {
                'form': p_form,
                'profile_user': request.user,
                'profile': request.user.profile,
                'page': 'editprofile',
            }
            return render(request, 'users/profile.html', context)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'form': p_form,
            'profile_user': request.user,
            'profile': request.user.profile,
            'page': 'editprofile',
        }
        return render(request, 'users/profile.html', context)

#####~~~~~ VIEW ~~~~~#####
# user moderator panel
# list of administered communities
@login_required
def modpanel(request):
    # warn user to verify email
    if not request.user.profile.email_verified:
        messages.warning(request, f'Please verify your email address.')

    if not request.user.administered_communities.all():
        return redirect('profile', request.user.username)

    communities = request.user.administered_communities.all()

    context = {
        'communities': communities,
        'profile_user': request.user,
        'profile': request.user.profile,
        'page': 'modpanel',
    }
    return render(request, 'users/profile.html', context)

#####~~~~~ VIEW ~~~~~#####
# list of joined communities
@login_required
def userJoinedCommunities(request, username):

    user = get_object_or_404(User, username=username)    

    if request.user != user:
        return redirect('profile', user.username)

    communities = request.user.joined_communities.all()

    context = {
        'communities': communities,
        'heading': 'Joined Communities',
        'empty_text': 'Its a little lonely here :('
    }
    context.update(getFeedContextMin(request))
    return render(request, 'community/community_list.html', context)

#####~~~~~ VIEW ~~~~~#####
# user login view
def login(request):
    if request.method == 'POST' and request.is_ajax():
        if request.user.is_authenticated:
            data = {'message': 'already logged in'}
            return JsonResponse(data)
        else:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            data = {}
            if user is None:
                data = {'message': 'failure'}
                return JsonResponse(data)
            else:
                auth_login(request, user)
                data = {'message': 'success'}
                return JsonResponse(data)
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'redirect_path': request.path})

#####~~~~~ VIEW ~~~~~#####
# logout is done using django's builT-in logout class-based view function (see common.urls)

#####~~~~~ VIEW ~~~~~#####
# user creation view
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        data = {
            'message':'',
            'error':'',
            'account':{}
        }
        # test email validity
        try:
            validate_email(email)
        except ValidationError as e:
            # email invalid
            data['message'] = 'invalid_email'
            print(e)
            data['error'] = e.messages
            return JsonResponse(data)    
        # test email availability
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # email available, hence test username
            # test username validity
            validate_username = UnicodeUsernameValidator()
            try:
                validate_username(username)
            except ValidationError as e:
                data['message'] = 'invalid_username'
                print(e.messages)
                data['error'] = e.messages
                return JsonResponse(data)
            # test username availability
            try:
                match = User.objects.get(username=username)
            except User.DoesNotExist:
                # username available, hence test password
                # test password validity
                try:
                    validate_password(password1)
                except ValidationError as e:
                    # password invalid
                    data['message'] = 'invalid_password'
                    print(e)
                    data['error'] = e.messages
                    return JsonResponse(data)
                # password valid, test password1 & password2 match
                if password1 == password2:
                    # passwords match
                    # all seems good, attempt account creation
                    user = get_user_model().objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    # check if user's been created
                    try:
                        user = User.objects.get(username=username, email=email)
                    except User.DoesNotExist:
                        # account not created, unknown error
                        data['message'] = 'error'
                        data['error'] = ['Unknown error. User account not created.']
                        return JsonResponse(data)
                    # user created successfully and stored in 'user' var
                    # send verification email to new user
                    sendAccountVerificationEmail(username=username)
                    # return user credentials and success message
                    data['message'] = 'created'
                    data['account'] = {'username':user.username, 'email':user.email}
                    return JsonResponse(data) # user expected to be redirected by sign-up webpage
                else:
                    # passwords mismatch
                    data['message'] = 'password_mismatch'
                    data['error'] = ['Passwords do not match']
                    return JsonResponse(data)
            # username in use
            data['message'] = 'unavailable_username'
            return JsonResponse(data)
        # email in use
        data['message'] = 'unavailable_email'
        return JsonResponse(data)
    else:
        return render(request, 'users/register.html', {'redirect_path': request.path})

#####~~~~~ VIEW ~~~~~#####
# email verification link view
def emailVerify(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user2 = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user2.DoesNotExist):
        user2 = None
    if user2 is not None and emailVerificationToken.check_token(user2, token):
        user2.profile.email_verified = True
        user2.profile.save()
        user = request.user
        messages.success(request, f'Your email has been verified. You can now make a Post!')
        if (user.is_authenticated):
            if user.pk == user2.pk:
                return redirect('profile', user.username)
            else:
                return redirect('/logout?next=/login')
        return redirect('login')
    else:
        messages.warning(request, f'Email verification failed!')
        return redirect('/')

#####~~~~~ VIEW ~~~~~##### (AJAX)
# user deletion view
@login_required
def deleteAccount_AJAX(request):
    if request.method == 'POST' and request.is_ajax():
        if not request.user.is_authenticated:
            data = {'deleted': False, 'message': 'not logged in'}
            return JsonResponse(data)
        else:
            user_pass = request.user.password
            entered_pass = request.POST["password"]
            if check_password(user_pass, entered_pass):
                request.user.delete()
                data = {'deleted': True, 'message': 'failure'}
                return JsonResponse(data)
            data = {'deleted': False, 'message': 'failure'}
            return JsonResponse(data)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# user signup email test 
def validateEmail_AJAX(request):
    data = {
        'message':'',
        'error':'',
        'email':''
    }
    if request.method == 'POST':
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError as e:
            data['message'] = 'invalid'
            print(e)
            data['error'] = e.messages
            return JsonResponse(data)    
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            data['message'] = 'available'
            data['email'] = email
            return JsonResponse(data)
        data['message'] = 'unavailable'
        return JsonResponse(data)
    else:
        data['message'] = 'error'
        data['error'] = 'Request Not Supported'
        return JsonResponse(data)


