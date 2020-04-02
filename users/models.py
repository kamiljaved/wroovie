from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from enum import Enum

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

path_and_rename = PathAndRename("profile_pics")



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to=path_and_rename)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
        
        img.save(self.image.path)

