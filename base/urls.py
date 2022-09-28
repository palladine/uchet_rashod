from django.urls import path
from .views import (Main, AddPostoffice, AddCartridge, AddSupply, ApplySupply,
                    ShowCartridges, ShowUsers, ShowNomenclatures, AddOPS, ShowOPS,
                    AddSupplyOPS, ShowSupplyOPS, AddUser, ShowSupply, AddGroup,
                    ShowRefuse, AddOrder, ShowOrders, MoveCartridges, AddToStock)

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('main', Main.as_view(), name='main'),
    path('add_group', AddGroup.as_view(), name='add_group'),
    path('add_user', AddUser.as_view(), name='add_user'),
    path('add_postoffice', AddPostoffice.as_view(), name='add_postoffice'),
    path('add_cartridge', AddCartridge.as_view(), name='add_cartridge'),
    path('add_supply', AddSupply.as_view(), name='add_supply'),
    path('apply_supply', ApplySupply.as_view(), name='apply_supply'),
    path('show_cartridges', ShowCartridges.as_view(), name='show_cartridges'),
    path('show_users', ShowUsers.as_view(), name='show_users'),
    path('show_nomenclatures', ShowNomenclatures.as_view(), name='show_nomenclatures'),
    path('add_ops', AddOPS.as_view(), name='add_ops'),
    path('show_ops', ShowOPS.as_view(), name='show_ops'),
    path('add_supply_ops', AddSupplyOPS.as_view(), name='add_supply_ops'),
    path('show_supply_ops', ShowSupplyOPS.as_view(), name='show_supply_ops'),
    path('show_supply', ShowSupply.as_view(), name='show_supply'),
    path('show_refuse', ShowRefuse.as_view(), name='show_refuse'),
    path('add_order', AddOrder.as_view(), name='add_order'),
    path('show_orders', ShowOrders.as_view(), name='show_orders'),
    path('move_cartridges', MoveCartridges.as_view(), name='move_cartridges'),
    path('add_tostock', AddToStock.as_view(), name='add_tostock'),
]
