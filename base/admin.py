from django.contrib import admin
from .models import User, Postoffice, Cartridge, Supply, Part, State, OPS, Supply_OPS, Part_OPS, State_OPS, Act, Group
from django.contrib.auth.admin import UserAdmin


class ShowGroupAdmin(admin.ModelAdmin):
    list_display = ['pk', 'group_name']



class ShowUserAdmin(UserAdmin):
    list_display = ['pk', 'username', 'email', 'last_name',
                    'first_name', 'middle_name', 'group', 'postoffice_id', 'role',
                    'last_login', 'date_joined', 'is_staff', 'is_active', 'is_superuser']
    readonly_fields = ["date_joined"]
    UserAdmin.fieldsets = ((None, {'fields': ('username', 'password', 'email', 'last_name',
                    'first_name', 'middle_name', 'group', 'postoffice_id', 'role',
                    'last_login', 'date_joined', 'is_staff', 'is_active', 'is_superuser')}),)



class ShowPostofficeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'postoffice_name', 'index', 'address', 'group']


class ShowCartridgeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nomenclature', 'printer_model', 'is_drum', 'source']


class ShowSupplyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supply._meta.get_fields()]


class ShowPartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Part._meta.get_fields()]


class ShowStateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in State._meta.get_fields()]


class ShowOPSAdmin(admin.ModelAdmin):
    list_display = ['id', 'postoffice', 'index', 'address']


class ShowSupplyOPSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supply_OPS._meta.fields]


class ShowPartOPSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Part_OPS._meta.get_fields()]


class ShowStateOPSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in State_OPS._meta.get_fields()]


class ShowActAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Act._meta.get_fields()]


admin.site.register(Group, ShowGroupAdmin)
admin.site.register(User, ShowUserAdmin)
admin.site.register(Postoffice, ShowPostofficeAdmin)
admin.site.register(Cartridge, ShowCartridgeAdmin)
admin.site.register(Supply, ShowSupplyAdmin)
admin.site.register(Part, ShowPartAdmin)
admin.site.register(State, ShowStateAdmin)
admin.site.register(OPS, ShowOPSAdmin)
admin.site.register(Supply_OPS, ShowSupplyOPSAdmin)
admin.site.register(Part_OPS, ShowPartOPSAdmin)
admin.site.register(State_OPS, ShowStateOPSAdmin)
admin.site.register(Act, ShowActAdmin)
