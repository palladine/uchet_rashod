from django.contrib import admin

from .models import User, Postoffice

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email', 'last_name',
                    'first_name', 'middle_name', 'postoffice_id', 'role',
                    'last_login', 'date_joined', 'is_staff', 'is_active']

class PostofficeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'index', 'address']

admin.site.register(User, UserAdmin)
admin.site.register(Postoffice, PostofficeAdmin)
