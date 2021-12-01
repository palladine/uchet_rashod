from django.contrib import admin
from .models import User, Postoffice, Cartridge
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
    list_display = ['pk', 'name', 'index', 'address']


class ShowCartridgAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nomenclature']


admin.site.register(User, ShowUserAdmin)
admin.site.register(Postoffice, ShowPostofficeAdmin)
admin.site.register(Cartridge, ShowCartridgAdmin)
