from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.utils.deconstruct import deconstructible
# Create your models here.

# Community
# Members

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = str(instance.pk) + '-' + instance.user.username + '-{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

pr_community_icon = PathAndRename("community/icons")

class Community(models.Model):

    # attributes
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True)      # only alphabets (capital/small), no spaces
    tagline = models.CharField(max_length=50)   # short tagline
    about = models.CharField(max_length=500)    # no links allowed

    admins = models.ManyToManyField(User, related_name='administered_communities')
    members = models.ManyToManyField(User, related_name='joined_communities', through='Membership')

    icon = models.ImageField(default='profile_pics/default.png', upload_to=path_and_rename)
    banner = models.ImageField(null=True, blank=True, upload_to=path_and_rename)

    # last_mod = models.DateTimeField(auto_now=True)  # last modified
    # dtop = models.DateTimeField(auto_now_add=True)  # object creation (cannot be updated)
    dt_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name} - {self.tagline}'


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    dt_join = models.DateTimeField(default=timezone.now)