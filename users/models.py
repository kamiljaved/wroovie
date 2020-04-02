from django.db import models
from django.contrib.auth.models import User

import os

from django.utils.deconstruct import deconstructible
from enum import Enum
from common.storage import OverwriteStorage
from common.utils import resize_image

# users (FOLDER)
# -- comm1 (FOLDER)
# -- -- icon.png
# -- -- banner.png
# -- -- post_images (FOLDER)
# -- -- -- post1-pic1.png

BASE_PATH = "users"
PROFILE_PICTURES_PATH = os.path.join(BASE_PATH, 'profile_pictures')
DEFAULT_PROFILE_IMAGE_PATH = os.path.join(PROFILE_PICTURES_PATH, 'default.png')

def ProfileImageSavePath(instance, filename):
    return os.path.join(PROFILE_PICTURES_PATH, f'{instance.user.username}'+os.path.splitext(filename)[1])

""" @deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = str(instance.pk) + '-' + instance.user.username + '-{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)
 """

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=DEFAULT_PROFILE_IMAGE_PATH, storage=OverwriteStorage(), upload_to=ProfileImageSavePath)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # ******** /home/kamiljaved/Desktop/Django Workspace/db-project/dbwebproj/media/users/profile_pictures/kamiljaved_BUNctiE.png
        # https://stackoverflow.com/questions/34098434/django-image-save-typeerror-get-valid-name-missing-positional-argument-na
        resize_image(self.image.path, 300, 300)
