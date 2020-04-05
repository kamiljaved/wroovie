from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.utils.deconstruct import deconstructible
from common.storage import OverwriteStorage
from common.utils import resize_image
# Create your models here.

# Community
# Members


# Community (FOLDER)
# -- comm1 (FOLDER)
# -- -- icon.png
# -- -- banner.png
# -- -- post_images (FOLDER)
# -- -- -- post1-pic1.png

BASE_PATH = "community"
DEFAULT_COMMUNITY_ICON_PATH = os.path.join(BASE_PATH, 'default_icon.png')

def CommunityIconSavePath(instance, filename):
    return os.path.join(BASE_PATH, instance.name, 'icon' + os.path.splitext(filename)[1])

def CommunityBannerSavePath(instance, filename):
    return os.path.join(BASE_PATH, instance.name, 'banner' + os.path.splitext(filename)[1])

# @deconstructible
# class PathAndRename(object):

#     def __init__(self, sub_path, rename):
#         self. path= sub_path

#     def __call__(self, instance, filename):
#         # ext = filename.split('.')[-1]
#         # set filename as random string
#         # filename = str(instance.pk) + '/' + instance.user.username + '-{}.{}'.format(uuid4().hex, ext)
#         # return the whole path to the file
#         return os.path.join(self.path, filename)

# pr_community_icon = PathAndRename("community/icons")
# pr_community_banner = PathAndRename("community/icons")


class Community(models.Model):

    # attributes
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True)      # only alphabets (capital/small), no spaces
    title = models.CharField(max_length=50)   # short tagline
    about = models.CharField(max_length=500)    # no links allowed

    admins = models.ManyToManyField(User, related_name='administered_communities')
    members = models.ManyToManyField(User, related_name='joined_communities', through='Membership')

    icon = models.ImageField(default=DEFAULT_COMMUNITY_ICON_PATH, storage=OverwriteStorage(), upload_to=CommunityIconSavePath)
    banner = models.ImageField(null=True, blank=True, storage=OverwriteStorage(), upload_to=CommunityBannerSavePath)

    # last_mod = models.DateTimeField(auto_now=True)  # last modified
    # dtop = models.DateTimeField(auto_now_add=True)  # object creation (cannot be updated)
    dt_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name} - {self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        resize_image(self.icon.path, 300, 300)
        if self.banner:
            resize_image(self.banner.path, 500, 500)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    dt_join = models.DateTimeField(default=timezone.now)