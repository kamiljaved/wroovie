from django.contrib import admin
from .models import Post, Thread, Article, Reply

# Register your models here.
admin.site.register(Post)
admin.site.register(Thread)
admin.site.register(Article)
admin.site.register(Reply)