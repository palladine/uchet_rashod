from django.urls import path
from .views import Main, AddPostoffice

urlpatterns = [
    path('main', Main.as_view(), name='main'),
    path('add_postoffice', AddPostoffice.as_view(), name='add_postoffice'),
]
