from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static


# main url patterns
urlpatterns = [

    # django admin urls
    path('admin/', admin.site.urls),

    # my app urls
    path('', include('common.urls')),
    path('u/', include('users.urls')),
    path('c/', include('community.urls')),
    path('p/', include('posts.urls')),
    
    # other app urls
    path('trixeditor/', include('trix.urls')),
    path('summernote/', include('django_summernote.urls')),
    
]

handler404 = 'common.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
