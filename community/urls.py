
from django.urls import path, re_path

from .views import (addRemoveAdminToggle_AJAX, create, delete, home,
                    joinCommunityToggle_AJAX, latest, update, update_moderators, searchMember_AJAX)


# url patterns under ('c/')
urlpatterns = [

    # community views urls
    path('<str:name>/', home, name='community-home'),              # top posts list
    path('<str:name>/latest/', latest, name='community-latest'),   # latest posts list

    # community actions urls
    path('<str:name>/update/', update, name='community-update'),
    path('<str:name>/update/moderators/', update_moderators, name='community-update-moderators'),
    # path('<str:name>/remove/moderator/', remove_moderator_AJAX, name='community-remove-moderator'),
    # path('<str:name>/add/moderator/', add_moderator_AJAX, name='community-add-moderator'),
    path('<str:name>/update/moderators/search/', searchMember_AJAX, name='search-member'),
    path('<str:name>/delete/', delete, name='community-delete'),
    path('<str:name>/join/', joinCommunityToggle_AJAX, name='community-join'),
    path('<str:name>/admin-edit/', addRemoveAdminToggle_AJAX, name='community-admin-edit'),

]

