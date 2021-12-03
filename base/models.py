from django.db import models
from django.contrib.auth.models import AbstractUser

'''
    Models:
    + 1. User (username, password, email, last_name, first_name, , middle_name, postoffice_id, 
                    is_staff, is_active, date_joined, last_login, role)
    + 2. Postoffice (name, index, address)
    + 3. Cartridge (nomenclature)
    
    4. Operation (id, cartridge_id, postoffice_id, amount_up, amount_down, date_operation(db_index=True))
    5. State (id, cartridge_id, postoffice_id, amount)

    !! Добавление первого пользователя суперадмина:
    1. null=True (last_name, first_name, postoffice_id)
    2. миграция
    3. manage.py createsuperuser
    4. null в False (last_name, first_name, postoffice_id)
'''

class BaseModel(models.Model):
    objects = models.Manager()
    class Meta:
        abstract = True



class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=50, null=False, blank=False, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=255, null=False, blank=False, verbose_name="Пароль")
    email = models.EmailField(max_length=255, null=False, blank=False, verbose_name="E-mail")
    last_name = models.CharField(max_length=50, null=True, blank=False, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, null=True, blank=False, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    postoffice_id = models.ForeignKey("Postoffice", null=True, blank=False, on_delete=models.CASCADE, verbose_name="Почтамт")
    date_joined = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name="Дата регистрации")
    last_login = models.DateTimeField(null=True, blank=False, verbose_name="Дата последнего входа")

    roles = (
        ('1', 'Администратор'),
        ('2', 'Пользователь'),
    )
    role = models.CharField(max_length=50, default=2, choices=roles, null=False,  blank=False, verbose_name="Роль")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)



class Postoffice(BaseModel):
    postoffice_name = models.CharField(max_length=75, unique=True, null=False, blank=False, verbose_name="Почтамт")
    index = models.CharField(max_length=6, null=True, blank=True, default='', verbose_name="Индекс")
    address = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name="Адрес")

    class Meta:
        verbose_name = "Почтамт"
        verbose_name_plural = "Почтамты"

    def __str__(self):
        return "{}".format(self.postoffice_name)


class Cartridge(BaseModel):
    nomenclature = models.CharField(max_length=75, unique=True, null=False, blank=False, verbose_name="Номенклатура картриджа")

    class Meta:
        verbose_name = "Картридж"
        verbose_name_plural = "Картриджи"

    def __str__(self):
        return "Картридж {}".format(self.nomenclature)