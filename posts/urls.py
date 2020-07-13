from django.urls import path, re_path
from .views import (createReply_AJAX, delete, post, update, updateReply_AJAX)


# url patterns under ('p/')
urlpatterns = [
    
    # post urls
    path('<str:slug>/', post, name='post-detail'),
    path('<str:slug>/update/', update, name='post-update'),
    path('<str:slug>/delete/', delete, name='post-delete'),

    # reply create url
    path('<str:slug>/reply/', createReply_AJAX, name='reply-create'),

]
