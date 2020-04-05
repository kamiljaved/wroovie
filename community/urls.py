
from django.urls import path, re_path
from .views import home, JoinCommunityToggle

urlpatterns = [

    # community views
    path('<str:name>', home),

    # community actions
    path('<str:name>/join', JoinCommunityToggle),
]


