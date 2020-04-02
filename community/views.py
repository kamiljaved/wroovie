from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from .models import Community

# Create your views here.
BASE_TEMPLATE_URL='community'

def home(request, name):
    try:
        community = Community.objects.get(name__iexact=name)
    except Community.DoesNotExist:
        raise Http404(f"The community page '{name}' does not exist.")

    context = {'community': community}
    return render(request, BASE_TEMPLATE_URL+'/home.html', context)

@login_required
def create(request):
    
    return render(request, BASE_TEMPLATE_URL+'/create.html', contxt)