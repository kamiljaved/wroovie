import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Max
from django.utils import timezone
from common.storage import OverwriteStorage
from common.utils import computeProminentColor, resizeImage


#####~~~~~ APP VARIABLES ~~~~~#####
BASE_PATH = "community"
DEFAULT_COMMUNITY_ICON_PATH = os.path.join(BASE_PATH, 'default_icon.png')

#####~~~~~ UTILITY FUNCTION ~~~~~#####
def CommunityIconSavePath(instance, filename):
    return os.path.join(BASE_PATH, instance.name, 'icon' + os.path.splitext(filename)[1])

#####~~~~~ UTILITY FUNCTION ~~~~~#####
def CommunityBannerSavePath(instance, filename):
    return os.path.join(BASE_PATH, instance.name, 'banner' + os.path.splitext(filename)[1])

#####~~~~~ MODEL ~~~~~#####
class Community(models.Model):
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True)     # only alphabets (capital/small), no spaces
    title = models.CharField(max_length=50)                 # short tagline
    about = models.CharField(max_length=500)
    dt_creation = models.DateTimeField(default=timezone.now)
    # many-to-many relation attributes
    admins = models.ManyToManyField(User, related_name='administered_communities')
    members = models.ManyToManyField(User, related_name='joined_communities', through='Membership')
    # theming attributes
    icon = models.ImageField(default=DEFAULT_COMMUNITY_ICON_PATH, storage=OverwriteStorage(), upload_to=CommunityIconSavePath)
    banner = models.ImageField(null=True, blank=True, storage=OverwriteStorage(), upload_to=CommunityBannerSavePath)
    highlight_color_hex =  models.CharField(default='000000', max_length=8, blank=True) 

    def __str__(self):
        return f'{self.name} - {self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # resize image and banner
        resizeImage(self.icon.path, 300, 300)
        if self.banner:
            resizeImage(self.banner.path, 500, 500)
        # set highlight color
        self.highlight_color_hex = computeProminentColor(self.icon.path)
        super().save(update_fields=['highlight_color_hex'])

    def get_top_posts(self, count = None):
        if count is None:
            return self.posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation') 
        else: 
            return self.posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).order_by('-count', '-dt_creation')[:count]
    
    def get_latest_posts(self, count = None):
        return self.posts.all() if count is None else self.posts.all()[:count]
    
    def get_top_post(self):
        return self.get_top_posts(1)
    
    def get_top_post_score(self):
        return self.posts.all().annotate(count=(Count('upvotes__id')-Count('downvotes__id'))).aggregate(Max('count'))['count__max']

    class Meta:
        ordering = ['-dt_creation']

#####~~~~~ (THROUGH) MODEL ~~~~~#####
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    dt_join = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-dt_join']


# Community (FOLDER)
# -- comm1 (FOLDER)
# -- -- icon.png
# -- -- banner.png
# -- -- post_images (FOLDER)
# -- -- -- post1-pic1.png

# last_mod = models.DateTimeField(auto_now=True)  # last modified
# dtop = models.DateTimeField(auto_now_add=True)  # object creation (cannot be updated)