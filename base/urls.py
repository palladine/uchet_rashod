from django.urls import path
from .views import Main, AddPostoffice, AddCartridge, AddSupply

urlpatterns = [
    path('main', Main.as_view(), name='main'),
    path('add_postoffice', AddPostoffice.as_view(), name='add_postoffice'),
    path('add_cartridge', AddCartridge.as_view(), name='add_cartridge'),
    path('add_supply', AddSupply.as_view(), name='add_supply'),
]
