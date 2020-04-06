from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Community
from posts.models import Thread, Article

# Create your views here.
BASE_TEMPLATE_URL='community'

def home(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")
    
    user_is_member = False
    if request.user.is_authenticated:
        user_is_member = community in request.user.joined_communities.all()
        # user_is_member = request.user.joined_communities.filter(pk=community.id).exists()
    
    # user_is_member = community.member.filter(pk=u.id).exists()

    # Ordering
    # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#order-by
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/asc_or_desc.html for sql of ordering
    
    #filter yahin kar k bhejne hai in order - only a select number of posts
    # yani database sey get hi woh number of posts hon..?
    # aur actually thread aur article mix ho kr jaen gey...
    # there can be seperate pages besides 'home' that will show only threads or article i.e. tabs on the community page
    # aur phir i guess jab end of page puhoncho gey to eik function bna lete hain
    # that will give the next few posts - based on a number that we send from the page indicating how many posts deep the user is...
    # ok
    # hello call for a minute? ok i will call
    # https://pypi.org/project/django-extensions/
    # https://stackoverflow.com/questions/1074212/how-can-i-see-the-raw-sql-queries-django-is-running 
    # hello
    threads = Thread.objects.filter(community__pk=community.id)#.order_by('')
    articles = Article.objects.filter(community__pk=community.id)

    context = {'community': community, 'user_is_member': user_is_member, 'threads': threads, 'articles': articles}
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

@login_required
def create(request):
    
    return render(request, BASE_TEMPLATE_URL+'/create.html', context)

def JoinCommunityToggle(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")
    
    joined = False
    redirect_to_login = False

    if request.user.is_authenticated:
        if community in request.user.joined_communities.all():
            joined = True
            community.members.remove(request.user)
            community.save()
            joined = False
        else:
            community.members.add(request.user)
            community.save()
            joined = True
    else:
        redirect_to_login = True

    data = {
        "joined": joined,
        "redirect_to_login": redirect_to_login
    }
    return JsonResponse(data)
