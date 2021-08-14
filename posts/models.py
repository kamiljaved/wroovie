from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from community.models import Community
from mptt.models import MPTTModel, TreeForeignKey
from trix.fields import TrixField
from common.utils import getImageLinks, get_timesince_minified
from common.templatetags.extra_tags import cool_number

#####~~~~~ (PARENT) MODEL ~~~~~#####
class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="posts")
    title = models.CharField(max_length=75)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    dt_creation = models.DateTimeField(default=timezone.now)
    # many-to-many relation attributes
    upvotes = models.ManyToManyField(User, through='PUpVote', related_name='upvoted_posts')
    downvotes = models.ManyToManyField(User, through='PDownVote', related_name='downvoted_posts')
    views = models.ManyToManyField(User, blank=True, related_name='viewed_posts')       # user visits  (1 view per user)

    class Meta:
        ordering = ['-dt_creation']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        # set post slug
        self.slug = self.get_slug()
        super().save(update_fields=['slug'])

    def get_slug(self):
        return f'{self.id}-{slugify(self.title)}'

    def get_reply_count(self):
        return Reply.objects.filter(post=self).count()

    def is_thread(self):
        return hasattr(self, 'thread')
    
    def is_article(self):
        return hasattr(self, 'article')

    def get_type(self):
        return 'Thread' if hasattr(self, 'thread') else 'Article'
    
    def get_score(self):
        return self.upvotes.count() - self.downvotes.count()
    
    def get_score_string(self, num_decimals=1):
        return cool_number(self.get_score(), num_decimals)

    def __str__(self):
        return f'({self.get_type()}) by ({self.author}) in ({self.community.name}) - ({self.title})'
        
    def get_simplified_str(self):
        return f'{self.get_type()}: {self.title}'

    def get_timesince_minified(self):
        return get_timesince_minified(self.dt_creation)

#####~~~~~ MODEL ~~~~~#####
class Article(Post):
    content = models.TextField(error_messages={'required':"Please add some content to the post"})    # for rich text editing, embedding, image adding
    main_img_url = models.URLField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        # set article main image url (if exists)
        img_url_list = getImageLinks(self.content)
        if img_url_list:
            self.main_img_url = img_url_list[0]
        super().save(update_fields=['main_img_url'])
        
#####~~~~~ MODEL ~~~~~#####
class Thread(Post):
    content = TrixField('Content')   # for rich text editing

#####~~~~~ MODEL ~~~~~#####
class Reply(MPTTModel):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='replies')
    # parent is NULL for a Reply made directly to a Post
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, db_index=True, on_delete=models.CASCADE)
    content = TrixField('Content')   
    dt_creation = models.DateTimeField(default=timezone.now)
    # meany-to-many relation attributes
    upvotes = models.ManyToManyField(User, through='RUpVote', related_name='upvoted_replies')
    downvotes = models.ManyToManyField(User, through='RDownVote', related_name='downvoted_replies')
    
    class Meta:
        ordering = ['-dt_creation']

    def get_score(self):
        return self.upvotes.count() - self.downvotes.count()

    def get_score_string(self, num_decimals=1):
        return cool_number(self.get_score(), num_decimals)

    def __str__(self):
        if self.parent is None:
            parent_str = self.post.get_simplified_str()
        else:
            parent_str = self.parent.content[0:10]
        return f'Reply by "{self.author}" on "{parent_str}" in "{self.post.get_simplified_str()}"'

#####~~~~~ (PARENT) MODEL ~~~~~#####
class PVote(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dt_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

#####~~~~~ (THROUGH) MODEL ~~~~~#####
class PUpVote(PVote):
    pass

    def __str__(self):
        return f'(Upvote) by ({self.user}) on ({self.post.get_simplified_str()})'

#####~~~~~ (THROUGH) MODEL ~~~~~#####
class PDownVote(PVote):
    pass

    def __str__(self):
        return f'(Downvote) by ({self.user}) on ({self.post.get_simplified_str()})'

#####~~~~~ (PARENT) MODEL ~~~~~#####
class RVote(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    dt_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def get_type(self):
        return 'Upvote' if hasattr(self, 'rupvote') else 'Downvote'

    def __str__(self):
        return f'({self.get_type()}) by ({self.user}) on Reply ({self.reply})'

#####~~~~~ (THROUGH) MODEL ~~~~~#####
class RUpVote(RVote):
    pass

#####~~~~~ (THROUGH) MODEL ~~~~~#####
class RDownVote(RVote):
    pass
