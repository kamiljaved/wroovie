from django.contrib import admin
from .models import Post, Thread, Article, Reply , PUpVote, PDownVote, RUpVote, RDownVote
from trix.admin import TrixAdmin
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Post)

@admin.register(Thread)
class ThreadAdmin(TrixAdmin, admin.ModelAdmin):
    trix_fields = ('content',)


# Apply summernote to all TextField in model.
class ArticleAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('content',)

admin.site.register(Article, ArticleAdmin)

# Register your models here.

admin.site.register(Reply)
admin.site.register(PUpVote)
admin.site.register(PDownVote)
admin.site.register(RUpVote)
admin.site.register(RDownVote)