
from django.urls import path, re_path
from .views import home


BASE_TEMPLATE_URL='community'

urlpatterns = [
    path('<str:name>', home),
]


