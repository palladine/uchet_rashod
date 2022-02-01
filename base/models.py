from django.db import models
from django.contrib.auth.models import AbstractUser

'''
    Models:
    + 1. User (username, password, email, last_name, first_name, , middle_name, postoffice_id, 
                    is_staff, is_active, date_joined, last_login, role)
    + 2. Postoffice (name, index, address)
    + 3. Cartridge (nomenclature, printer_model, is_drum, source)
    + 4. Supply (postoffice_recipient, user_sender, user_recipient, data_text, 
                date_sending(db_index=True), date_receiving(db_index=True), status_sending, status_receiving)
    + 5. Part (id_supply, postoffice, nomenclature, amount)
    + 6. State (postoffice, cartridge, total_amount)
    + 7. OPS (postoffice, index, address)
   

    !! Добавление первого пользователя суперадмина:
    1. null=True (last_name, first_name, postoffice_id)
    2. миграция
    3. manage.py createsuperuser
    4. null в False (last_name, first_name, postoffice_id)
'''


# for 'objects' Model's attribute
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
    postoffice_id = models.ForeignKey("Postoffice", null=True, blank=False, on_delete=models.SET_NULL, verbose_name="Почтамт")
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
    printer_model = models.CharField(max_length=100, null=False, blank=False, default='', verbose_name="Модель принтера")
    is_drum = models.BooleanField(default=False, verbose_name="Драм")
    source = models.CharField(max_length=255, null=False, blank=True, default='', verbose_name="Ресурс картриджа")

    class Meta:
        verbose_name = "Картридж"
        verbose_name_plural = "Картриджи"

    def __str__(self):
        return "{}".format(self.nomenclature)



class Supply(BaseModel):
    postoffice_recipient = models.CharField(max_length=75, default='', null=False, blank=False, verbose_name="Почтамт получатель")
    user_sender = models.CharField(max_length=50, null=False, blank=False, verbose_name="Отправитель")
    user_recipient = models.CharField(max_length=50, null=False, blank=False, verbose_name="Получатель")
    data_text = models.TextField(null=False, blank=False, verbose_name="Данные поставки")
    date_sending = models.DateTimeField(null=True, blank=False, verbose_name="Дата отправки", db_index=True)
    date_receiving = models.DateTimeField(null=True, blank=False, verbose_name="Дата приемки", db_index=True)
    status_sending = models.BooleanField(default=False, verbose_name="Статус отправки")
    status_receiving = models.BooleanField(default=False, verbose_name="Статус приемки")

    class Meta:
        verbose_name = "Поставка в почтамт"
        verbose_name_plural = "Поставки в почтамты"

    def __str__(self):
        return "Поставка №{0} (на {1})".format(self.pk, self.postoffice_recipient)


class Part(BaseModel):
    id_supply = models.SmallIntegerField(default=-1, null=False, blank=False, verbose_name="ID Поставки")
    postoffice = models.CharField(max_length=75, null=False, blank=False, verbose_name="Почтамт получатель")
    cartridge = models.CharField(max_length=75, null=False, blank=False, verbose_name="Картридж")
    amount = models.SmallIntegerField(default=0, null=False, blank=False, verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция в поставке"
        verbose_name_plural = "Позиции в поставках"

    def __str__(self):
        return "Позиция №{}".format(self.pk)


class State(BaseModel):
    postoffice = models.ForeignKey('Postoffice', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Почтамт")
    cartridge = models.ForeignKey('Cartridge', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Картридж")
    total_amount = models.IntegerField(default=0, null=False, blank=False, verbose_name="Количество")

    class Meta:
        verbose_name = "Учет картриджей"
        verbose_name_plural = "Учет картриджей"

    def __str__(self):
        return "Учет картриджей"


class OPS(BaseModel):
    postoffice = models.ForeignKey('Postoffice', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Почтамт")
    index = models.CharField(max_length=6, null=True, blank=True, default='', verbose_name="Индекс")
    address = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name="Адрес")

    class Meta:
        verbose_name = "ОПС"
        verbose_name_plural = "ОПС"

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.index)


class Supply_OPS(BaseModel):
    ops_recipient = models.ForeignKey('OPS', null=True, blank=False, on_delete=models.PROTECT, verbose_name="ОПС получатель")
    user_sender = models.ForeignKey('User', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Отправитель")
    data_text = models.TextField(null=False, blank=False, verbose_name="Данные поставки")
    date_sending = models.DateTimeField(null=True, blank=False, verbose_name="Дата отправки", db_index=True)
    status_sending = models.BooleanField(default=False, verbose_name="Статус отправки")
    status_act = models.BooleanField(default=False, verbose_name="Статус распечатанного акта")

    class Meta:
        verbose_name = "Поставка ОПС"
        verbose_name_plural = "Поставка ОПС"

    def __str__(self):
        return "Поствка №{0} (на ОПС {1})".format(self.pk, self.ops_recipient.index)


class Part_OPS(BaseModel):
    id_supply_ops = models.ForeignKey('Supply_OPS', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Поставка")
    cartridge = models.ForeignKey('Cartridge', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Картридж")
    amount = models.IntegerField(default=0, null=False, blank=False, verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция в поставке ОПС"
        verbose_name_plural = "Позиции в поставке ОПС"

    def __str__(self):
        return "Позиция №{}".format(self.pk)


class State_OPS(BaseModel):
    ops = models.ForeignKey('OPS', null=True, blank=False, on_delete=models.PROTECT, verbose_name="ОПС")
    cartridge = models.ForeignKey('Cartridge', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Картридж")
    total_amount = models.IntegerField(default=0, null=False, blank=False, verbose_name="Количество")

    class Meta:
        verbose_name = "Учет картриджей ОПС"
        verbose_name_plural = "Учет картриджей ОПС"

    def __str__(self):
        return "Учет картриджей ОПС"