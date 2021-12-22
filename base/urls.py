from django.urls import path
from .views import Main, AddPostoffice, AddCartridge, AddSupply, ApplySupply, ShowCartridges

urlpatterns = [
    path('main', Main.as_view(), name='main'),
    path('add_postoffice', AddPostoffice.as_view(), name='add_postoffice'),
    path('add_cartridge', AddCartridge.as_view(), name='add_cartridge'),
    path('add_supply', AddSupply.as_view(), name='add_supply'),
    path('apply_supply', ApplySupply.as_view(), name='apply_supply'),
    path('show_cartridges', ShowCartridges.as_view(), name='show_cartridges'),
]
