from django.contrib import admin
from .models import User, Postoffice, Cartridge, Supply, Part
from django.contrib.auth.admin import UserAdmin


class ShowUserAdmin(UserAdmin):
    list_display = ['pk', 'username', 'email', 'last_name',
                    'first_name', 'middle_name', 'postoffice_id', 'role',
                    'last_login', 'date_joined', 'is_staff', 'is_active']
    readonly_fields = ["date_joined"]
    UserAdmin.fieldsets = ((None, {'fields': ('username', 'password', 'email', 'last_name',
                    'first_name', 'middle_name', 'postoffice_id', 'role',
                    'last_login', 'date_joined', 'is_staff', 'is_active')}),)



class ShowPostofficeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'postoffice_name', 'index', 'address']


class ShowCartridgAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nomenclature', 'printer_model', 'is_drum', 'source']


class ShowSupplyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supply._meta.get_fields()]


class ShowPartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Part._meta.get_fields()]



admin.site.register(User, ShowUserAdmin)
admin.site.register(Postoffice, ShowPostofficeAdmin)
admin.site.register(Cartridge, ShowCartridgAdmin)
admin.site.register(Supply, ShowSupplyAdmin)
admin.site.register(Part, ShowPartAdmin)
