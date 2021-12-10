import os.path

from django import forms
from django.forms import CharField, FileField
from django.core.exceptions import ValidationError
from .models import User, Cartridge, Postoffice


ht = '* Поле обязательное для заполнения'

## Custom fields LoginForm
class LoginField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ЛОГИН" обязательное для заполнения'), code='empty')

        query_unique = Postoffice.objects.filter(postoffice_name=value).exists()
        if query_unique:
            raise ValidationError(('Пользователь с именем "{}" уже зарегистрирован, введите другое имя'.format(value)),
                                  code='unique')

class PasswordField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПАРОЛЬ" обязательное для заполнения'), code='empty')


class LoginForm(forms.Form):
    login = LoginField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ЛОГИН'}))
    password = PasswordField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))



## Custom fields AddPostOfficeForm
class PostofficeNameField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПОЧТАМТ" обязательное для заполнения'), code='empty')

        query_unique = Postoffice.objects.filter(postoffice_name=value).exists()
        if query_unique:
            raise ValidationError(('Почтамт с именем "{}" уже зарегистрирован. Введите другое имя'.format(value)), code='unique')


class IndexField(CharField):
    # Validation
    def clean(self, value):
        if not all(l.isdigit() for l in value):
            raise ValidationError(('Поле "ИНДЕКС" должно состоять из цифр'), code='isdigit')

        if len(value) != 6:
            raise ValidationError(('Поле "ИНДЕКС" неправильной длины'), code='length')


class AddPostofficeForm(forms.Form):
    postoffice_name = PostofficeNameField(label='Почтамт', max_length=100, help_text=ht, required=True,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПОЧТАМТ'}))
    index = IndexField(label='Индекс', max_length=6, required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС'}))
    address = forms.CharField(label='Адрес', max_length=255, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС'}))



## Custom fields AddCartridgeForm
class NomenclatureField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "НОМЕНКЛАТУРА" обязательное для заполнения'), code='empty')

        query_unique = Cartridge.objects.filter(nomenclature=value.strip()).exists()
        if query_unique:
            raise ValidationError(('Номенклатура картриджа "{}" уже зарегистрирована. Введите другое имя'.format(value)),
                                  code='unique')


class PrinterModelField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "МОДЕЛЬ ПРИНТЕРА" обязательное для заполнения'), code='empty')


class AddCartridgeForm(forms.Form):
    nomenclature = NomenclatureField(label='Номенклатура картриджа', max_length=100, help_text=ht, required=True,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'НОМЕНКЛАТУРА'}))
    printer_model = PrinterModelField(label='Модель принтера', max_length=100, help_text=ht, required=True,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'МОДЕЛЬ ПРИНТЕРА'}))
    is_drum = forms.BooleanField(label='Является драмом', required=False,
                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}))
    source = forms.CharField(label='Ресурс картриджа', required=False, max_length=255,
                                widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'РЕСУРС КАРТРИДЖА'}))




# Custom field AddCartridgesFileForm
class WorkFile(FileField):

    # Validation
    def clean(self, data, initial=None):
        # data -> InMemoryUploadedFile

        if not data:
            raise ValidationError(('Поле "ФАЙЛ" обязательное для заполнения'), code='empty')

        valid_extensions = ['xlsx', 'xls']
        extension = data.name.split('.')[1]

        if not extension.lower() in valid_extensions:
            raise ValidationError(('Неподдерживаемый формат файла'))

        return data   # !!!

class AddCartridgesFileForm(forms.Form):
    '''
        <form enctype="multipart/form-data" method="post"> ...            in template.html
        form = AddCartridgesFileForm(request.POST, request.FILES) ...     in views.py
    '''
    file = WorkFile(label='Файл', max_length=100, help_text=ht, required=True,
                        widget=forms.FileInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ФАЙЛ'}))


