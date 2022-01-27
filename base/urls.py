from django.urls import path
from .views import (Main, AddPostoffice, AddCartridge, AddSupply, ApplySupply,
                    ShowCartridges, ShowUsers, ShowNomenclatures, AddOPS, ShowOPS)

urlpatterns = [
    path('main', Main.as_view(), name='main'),
    path('add_postoffice', AddPostoffice.as_view(), name='add_postoffice'),
    path('add_cartridge', AddCartridge.as_view(), name='add_cartridge'),
    path('add_supply', AddSupply.as_view(), name='add_supply'),
    path('apply_supply', ApplySupply.as_view(), name='apply_supply'),
    path('show_cartridges', ShowCartridges.as_view(), name='show_cartridges'),
    path('show_users', ShowUsers.as_view(), name='show_users'),
    path('show_nomenclatures', ShowNomenclatures.as_view(), name='show_nomenclatures'),
    path('add_ops', AddOPS.as_view(), name='add_ops'),
    path('show_ops', ShowOPS.as_view(), name='show_ops'),
]
