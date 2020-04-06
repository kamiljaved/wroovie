from django.db import models
from community.models import Community 
from django.contrib.auth.models import User
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here. terminal

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")
    dt_creation = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    upvotes = models.ManyToManyField(User, blank = True, related_name='upvoted_posts')
    downvotes = models.ManyToManyField(User, blank = True, related_name='downvoted_posts')


class Thread(Post):
    title = models.CharField(max_length=75)
    content = models.TextField(max_length=1500)

    view_count = models.IntegerField("Views", default=0)

    # main_replies = models.ForeignKey(Reply)

# reply can have replies of itself, those replies will also be associated to the main thread...
# what if a reply is a reply to a reply through thread?
# but then what about replies to the main thread?

# for base replies we can have parent null for other we can have parent as those replies
# would be very redundant as very possibly there'd be more number of main replies than replies to replies
# we can do one thing

# here instead of null we can have foreign key towards the parent reply of the thread for main replies
class Reply(MPTTModel):

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    # achha ab yaha kya krna baki reh gya hai
    # wo path_and_rename kidhar kia hai??
    # community k models mein tha
    # kahin aur nahi chahiye hoga??
    # yr try to see 
    # there?
    
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, related_name='replies')

    dt_creation = models.DateTimeField(default=timezone.now)


    upvotes = models.ManyToManyField(User, blank = True, related_name='upvoted_replies')
    downvotes = models.ManyToManyField(User, blank = True, related_name='downvoted_replies')

    content = models.TextField(max_length=3000)

    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, db_index=True, on_delete=models.SET_NULL)
    
    # i will be back in a few minutes
    # ok

    # and check in clean that a parent should be either a thread or a reply
    # or, we could just use this same model for article comments.....

class Article(Post):
    
    title = models.CharField(max_length=75)
    content =  models.TextField(max_length=3000)

    view_count = models.IntegerField("Views", default=0)

# class Block(models.Model):
#     post = models.ForeignKey(Post)
    
    
# class ImageBlock(Block):
#     image = models.ImageField(default='', blank=True, upload_to=path_and_rename)


#     file_attachment = models.FileField(default='', blank=True, upload_to='blog_file-attachments/', verbose_name='File Attachment')
#     video_embed = EmbedVideoField(default='', blank=True, verbose_name='Video Link')
#     video_file = models.FileField(blank=True, upload_to='blog_videos/', verbose_name="Video Upload", help_text="Supported Formats: mp4, mkv")


# class TextBlock(Block):
#     text = models.TextField()

