from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Community

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

    context = {'community': community, 'user_is_member': user_is_member}
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
