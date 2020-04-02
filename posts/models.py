from django.db import models
from community.models import Community 
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    dt_creation = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)     # if User is deleted, their post is also deleted

    upvotes = models.ManyToManyField(User, blank = True, related_name='upvoted_posts')
    downvotes = models.ManyToManyField(User, blank = True, related_name='downvoted_posts')


class Thread(Post):
    title = models.CharField(max_length=75)
    content = models.TextField(max_length=1500)

    view_count = models.IntegerField("Views", default=0)
    replies = models.ManyToManyField(Reply, blank=True)

    main_reply = models.ForeignKey(Reply)

# reply can have replies of itself, those replies will also be associated to the main thread...
# what if a reply is a reply to a reply through thread?
# but then what about replies to the main thread?

# for base replies we can have parent null for other we can have parent as those replies
# would be very redundant as very possibly there'd be more number of main replies than replies to replies
# we can do one thing

# here instead of null we can have foreign key towards the parent reply of the thread for main replies
class Reply(Post):
    
    parent = models.ForeignKey(Post, null=False, related_name=)

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

