from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
import django.views.defaults as default_views

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

from common.views import handler404 as hndlr404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        re_path(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        re_path(r'^404/$', hndlr404, kwargs={'exception': Exception('Page not Found')}),
        re_path(r'^500/$', default_views.server_error),
    ]
