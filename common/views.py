from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template import RequestContext


def handler404(request, exception):
    return render(request, '404.html', {})

def home(request):    

    context = {
        'user': request.user,
    }
    return render(request, 'common/home.html', context)


# user not signed in
#--------------------
# get top communities (region-wise)
# get top discussion threads (region-wise)
# get top articles
# get top questions

# user signed in
#---------------
# get top posts (parent) from followed communities 
# get top posts from recommended communities


