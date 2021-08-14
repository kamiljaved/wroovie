import os
from django.contrib.auth.models import User
from django.db import models
from common.storage import OverwriteStorage
from common.utils import resizeImage
from posts.models import Post
from common.utils import computeProminentColor
from django.db.models import Count, Max

#####~~~~~ APP VARIABLES ~~~~~#####
BASE_PATH = "users"
PROFILE_PICTURES_PATH = os.path.join(BASE_PATH, 'profile_pictures')
PROFILE_BANNERS_PATH = os.path.join(BASE_PATH, 'profile_banners')
DEFAULT_PROFILE_IMAGE_PATH = os.path.join(BASE_PATH, 'default_profile_picture.png')

#####~~~~~ UTILITY FUNCTION ~~~~~#####
def profileImageSavePath(instance, filename):
    return os.path.join(PROFILE_PICTURES_PATH, f'{instance.user.username}'+os.path.splitext(filename)[1])

#####~~~~~ UTILITY FUNCTION ~~~~~#####
def profileBannerSavePath(instance, filename):
    return os.path.join(PROFILE_BANNERS_PATH, f'{instance.user.username}'+os.path.splitext(filename)[1])

#####~~~~~ MODEL ~~~~~#####
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=DEFAULT_PROFILE_IMAGE_PATH, storage=OverwriteStorage(), upload_to=profileImageSavePath)
    email_verified = models.BooleanField(default=False)

    # extra stuff
    banner = models.ImageField(null=True, blank=True, storage=OverwriteStorage(), upload_to=profileBannerSavePath)
    saved_posts = models.ManyToManyField(Post, blank=True, related_name='saved_by')
    highlight_color_hex =  models.CharField(default='000000', max_length=8, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resizeImage(self.image.path, 300, 300)
        # resize banner
        if self.banner:
            resizeImage(self.banner.path, 500, 500)
        # set highlight color
        self.highlight_color_hex = computeProminentColor(self.image.path)
        super().save(update_fields=['highlight_color_hex'])

    def get_top_posts(self, count = None):
        if count is None:
            return self.user.posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation') 
        else: 
            return self.user.posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:count]
    
    def get_latest_posts(self, count = None):
        return self.user.posts.all() if count is None else self.user.posts.all()[:count]

    def get_top_saved_posts(self, count = None):
        if count is None:
            return self.saved_posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation') 
        else: 
            return self.saved_posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:count]
    
    def get_latest_saved_posts(self, count = None):
        return self.saved_posts.all() if count is None else self.saved_posts.all()[:count]

    def get_top_comments(self, count = None):
        if count is None:
            return self.user.replies.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation') 
        else: 
            return self.user.replies.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:count]
    
    def get_latest_comments(self, count = None):
        return self.user.replies.all().order_by('-dt_creation')  if count is None else self.user.replies.all().order_by('-dt_creation')[:count]

    def get_top_upvoted_posts(self, count = None):
        if count is None:
            return self.user.upvoted_posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation') 
        else: 
            return self.user.upvoted_posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:count]
    
    def get_latest_upvoted_posts(self, count = None):
        return self.user.upvoted_posts.all() if count is None else self.user.upvoted_posts.all()[:count]
 
    def get_top_downvoted_posts(self, count = None):
        if count is None:
            return self.user.downvoted_posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation') 
        else: 
            return self.user.downvoted_posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:count]
    
    def get_latest_downvoted_posts(self, count = None):
        return self.user.downvoted_posts.all() if count is None else self.user.downvoted_posts.all()[:count]

# users (FOLDER)
# -- comm1 (FOLDER)
# -- -- icon.png
# -- -- banner.png
# -- -- post_images (FOLDER)
# -- -- -- post1-pic1.png