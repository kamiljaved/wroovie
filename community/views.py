import re
from datetime import date, timedelta
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.models import Count, Max, Sum
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from posts.models import Article, Post, Thread
from .forms import CommunityCreateForm, CommunityUpdateForm
from .models import Community
from collections import Counter
from common.views import qget_suggCommunities, qget_suggPosts
from common.views import getFeedContextMin

#####~~~~~ RELATED CONSTRAINTS ~~~~~#####
# 2. Only the members of a Community can be selected as Admin of that Community.
# 3. A User’s Email must be verified before they can start joining Communities

#####~~~~~ APP VARIABLES ~~~~~#####
BASE_TEMPLATE_URL = 'community'
MAX_TOP_COMMUNITIES = 50
# assumption: any member can be searched using exact username
MAX_MEMBER_SEARCH_ITEMS = 50

#####~~~~~ QUERY FUNCTION ~~~~~#####
def qget_topCommunities(cnt=MAX_TOP_COMMUNITIES):
    return Community.objects.all().annotate(count=Count('members')).order_by('-count')[:cnt]

#####~~~~~ QUERY FUNCTION ~~~~~#####
def qget_trendingCommunities(cnt=MAX_TOP_COMMUNITIES):
    comm_ids = list(dict(Counter(Post.objects.filter(dt_creation__gte=(date.today() - timedelta(days=50))).values_list('community__id', flat=True)).most_common()).keys())[:cnt]
    comm = Community.objects.in_bulk(comm_ids)
    return [comm[x] for x in comm_ids]

#####~~~~~ VIEW ~~~~~#####
# community homepage view (post list view) (orders post by top score)
def home(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")
    user_is_member = False
    if request.user.is_authenticated:
        user_is_member = request.user.joined_communities.filter(pk = community.id).exists()
    posts = community.get_top_posts()
    context = {'community': community, 'user_is_member': user_is_member, 'posts': posts, 'post_sorting': 'top'}
    # send suggestions if user is authenticated
    if request.user.is_authenticated:
        sugg_comm = qget_suggCommunities(request.user, 5)
        sugg_posts = qget_suggPosts(sugg_comm, 5)
        context['sugg_comm'] = sugg_comm
        context['sugg_posts'] = sugg_posts
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

#####~~~~~ VIEW ~~~~~#####
# community homepage view (latest post list view)
def latest(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")
    user_is_member = False
    if request.user.is_authenticated:
        user_is_member = request.user.joined_communities.filter(pk = community.id).exists()
    posts = community.get_latest_posts()
    context = {'community': community, 'user_is_member': user_is_member, 'posts': posts, 'post_sorting': 'latest'}
    # send suggestions if user is authenticated
    if request.user.is_authenticated:
        sugg_comm = qget_suggCommunities(request.user, 5)
        sugg_posts = qget_suggPosts(sugg_comm, 5)
        context['sugg_comm'] = sugg_comm
        context['sugg_posts'] = sugg_posts
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

#####~~~~~ VIEW ~~~~~#####
# community creation view
@login_required
def create(request):
    # creator, admins are all added to community /and/ later, only memebers can be added as community
    if not request.user.profile.email_verified:
        messages.warning(request, f'Please verify your email address first.')
        return redirect("home")
    if request.method == 'POST':
        form = CommunityCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # name = form.cleaned_data.get('name')
            # # test name validity (no spaces or bad characters allowed)
            # validate_name = UnicodeUsernameValidator()
            # try:
            #     validate_name(name)
            # except ValidationError:
            #     raise forms.ValidationError("Invalid Name for a Community!")
            # test passed
            community = form.save(commit=False)
            # add creator and admin to community member list
            community.creator = request.user
            name = community.name
            print(community.icon)
            community.save()
            community.members.add(community.creator)
            community.admins.add(community.creator)
            print(name)
            # community.members.add(community.admins.all())
            messages.success(request, f'Community Page created!')
            return redirect('community-home', name)      
        else:
            #raise forms.ValidationError("Please fix the errors.")
            return render(request, BASE_TEMPLATE_URL+'/create.html', {'form': form})
    else:
        form = CommunityCreateForm()
        context = {
            'form': form,
        } 
        return render(request, BASE_TEMPLATE_URL+'/create.html', context)

#####~~~~~ VIEW ~~~~~#####
# community update view
@login_required
def update(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")
    # refuse request if user is not admin
    if request.user not in community.admins.all():
        messages.warning(request, f'You are not authorized to view requested page.')
        return redirect('community-home', name)
    if request.method == 'POST':
        form = CommunityUpdateForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, f'Community Page updated successfully!')
            return redirect('community-home', name) 
        else:
            context = {
                'form': form,
                'name': community.name,
            }
            return render(request, BASE_TEMPLATE_URL+'/update.html', context)
    else:
        form = CommunityUpdateForm(instance=community)
        context = {
            'form': form,
            'name': community.name,
            'community': community,
        }
        return render(request, BASE_TEMPLATE_URL+'/update.html', context)

@login_required
def update_moderators(request, name):

    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        return Http404(f"Community {name} does not exist")

    moderators = community.admins.all()

    if request.user not in moderators:
        messages.error(request, "You are not authorized to access this page")
        return redirect('community-home', name)

    context = {
        'moderators': moderators.exclude(id=community.creator.id).exclude(id=request.user.id),
        'community': community,
        'name': community.name,
    }

    return render(request, BASE_TEMPLATE_URL+'/update_moderators.html', context)

#####~~~~~ VIEW ~~~~~#####
# community delete view
@login_required
def delete(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")
    # refuse request if user is not admin
    if request.user not in community.admins.all():
        messages.warning(request, f'You are not authorized to view requested page.')
        return redirect('community-home', name)
    if request.method == 'POST':
        # delete community and return to home
        community.delete()
        return redirect('home')
    else:
        return render(request, BASE_TEMPLATE_URL+'/delete.html', {'community': community})

#####~~~~~ VIEW ~~~~~#####
# top communities list (top community is one with higher number of members)
def topCommunities(request):
    communities = qget_topCommunities(MAX_TOP_COMMUNITIES)
    context = {
        'communities': communities,
        'heading': 'Top Communities',
        'empty_text': 'No Top Communities Yet'
    }
    context.update(getFeedContextMin(request, incl_top_comm=False))
    return render(request, 'community/community_list.html', context)

#####~~~~~ VIEW ~~~~~#####
# trending communities list (communities with most posts in recent month)
def trendingCommunities(request):
    # get recent month most-posts comunities
    communities = qget_trendingCommunities(MAX_TOP_COMMUNITIES)
    context = {
        'communities': communities,
        'heading': 'Popular Communities',
        'empty_text': 'No Popular Communities these days'
    }
    context.update(getFeedContextMin(request, incl_trnd_comm=False))
    return render(request, 'community/community_list.html', context)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# community join view
def joinCommunityToggle_AJAX(request, name):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'error': True, 'message': f'Not authorized.'})
    
    #####~~~~~ CONSTRAINT (3) ~~~~~#####
    # test if user email is verified
    if not request.user.is_authenticated:
        return JsonResponse({'error': True, 'message': f'You need to log in to be able to join a Community.', "redirect_to_login": True})    
    if not request.user.profile.email_verified:
        return JsonResponse({'error': True, 'message': f'Please verify your email address.'})
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        return JsonResponse({'error': True, 'message': f"The community page '{name}' does not exist."})
    # assuming creator is in admins, and all admins are members
    if request.user in community.admins.all():
        return JsonResponse({'error': True, 'message': f'Community admin cannot leave the Community.', "redirect_to_login": True})

    # no errors
    joined = False
    if community in request.user.joined_communities.all():
        joined = True
        community.members.remove(request.user)
        community.save()
        joined = False
    else:
        community.members.add(request.user)
        community.save()
        joined = True
    data = {
        "joined": joined,
        "error": False
    }
    return JsonResponse(data)

#####~~~~~ VIEW ~~~~~##### (AJAX)
# add or remove an admin (added admin must be member, adder must be admin)
def addRemoveAdminToggle_AJAX(request, name):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'error': True, 'message': f'Not authorized.'})
    # get community if exists
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        return JsonResponse({'error': True, 'message': f"The community page c/{name} does not exist."})
    # get user if exists
    try:
        username = request.POST['username']
    except:
        return JsonResponse({'error': True, 'message': f"Option 'username' not found."})

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': True, 'message': f"The user u/{username} does not exist."})
    # refuse request if requester is not admin
    if not community.admins.filter(id=request.user.id).exists():
        return JsonResponse({'error': True, 'message': f"You are not authorized for this action."})
    #####~~~~~ CONSTRAINT (2) ~~~~~#####
    # refuse request if user to be added/removed is not a member of that community
    if not community.members.filter(id=user.id).exists():
        return JsonResponse({'error': True, 'message': f"This user is not a member of the Community c/{name}."})
    
    # refuse request if user to be added/removed is requester
    if request.user == user:
        return JsonResponse({'error': True, 'message': f"You cannot modify your own status."})

    # refuse request if user to be added/removed is commuity-creator
    if user == community.creator:
        return JsonResponse({'error': True, 'message': f"The status of community creator cannot be changed."})

    error = False
    admin = False
    message = ""

    try:
        to_do = request.POST['to_do']
    except:
        return JsonResponse({'error': True, 'message': f"Option 'to_do' not found."})

    # to_do == true --> add user as admin
    # to_do == false --> removeuser as admin
    if to_do == "true":
        # add user to admin-list if not already an admin
        if community.admins.filter(id=user.id).exists():
            message = f"u/{username} is already an admin of the Community c/{name}."
            error = True
        else:
            community.admins.add(user)
            admin = True
            message = f"Succesfully added member u/{username} as admin of the Community c/{name}."
    else:
        # remove user from admin-list if they are an admin
        if community.admins.filter(id=user.id).exists():
            community.admins.remove(user.id)
            admin = False
            message = f"Succesfully removed member u/{username} as admin of the Community c/{name}."
        else:
            message = f"This user is already not an admin of the Community c/{name}."
            error = True
    data = {
        "admin": admin,
        "message": message,
        'error': error,
    }
    return JsonResponse(data)


def searchMember_AJAX(request, name):
    if not (request.method == "POST" and request.is_ajax()):
        messages.error("Not authorized.")
        return redirect("community-home", name)

    search_qry = request.POST['search_qry']

    if re.match("\s+", search_qry) is not None:
        return JsonResponse({'error': True, 'message': f'The search query contains whitespaces'})

    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        return JsonResponse({'error': True, 'message': f"The community page c/{name} does not exist."})

    moderators = community.admins.all()

    if request.user not in moderators:
        return JsonResponse({'error': True, 'message': f'You are not authorized for this action'})

    members = community.members.filter(username__icontains=search_qry)[:MAX_MEMBER_SEARCH_ITEMS]

    members_only = []
    for member in members:
        if member not in moderators:
            members_only.append(member)

    result_dict = {}
    for result in members_only:
        result_dict[str(result.id)] = result.username

    return JsonResponse({'error': False, 'result': result_dict})
    

    






# POSTS_PER_PAGE = 10

# def get_top_posts(community, days, page):
#     return community.posts.filter(dt_creation__gte=(date.today() - timedelta(days=days))).annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[page*POSTS_PER_PAGE: (page+1)*POSTS_PER_PAGE]
# def get_top_posts(community, days, page):
#     print(f'Community name: {community.name}')
#     return community.posts.all()

# get posts ajax
# def get_posts_ajax(request, id, days, page):
#     if request.method == 'POST':
#         try:
#             community = Community.objects.get(pk=id)
#         except Community.DoesNotExist:
#             raise Http404(f"The community with id '{id}' does not exist.")
#         posts = get_top_posts(community, days, page)
#         data = {}
#         return JsonResponse(data)

    # Ordering
    # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#order-by
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/asc_or_desc.html for sql of ordering
    
    # https://pypi.org/project/django-extensions/
    # https://stackoverflow.com/questions/1074212/how-can-i-see-the-raw-sql-queries-django-is-running 
