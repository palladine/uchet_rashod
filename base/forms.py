from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from .models import Postoffice


ht = '* Поле обязательное для заполнения'


class LoginForm(forms.Form):
    login = forms.CharField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ЛОГИН'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))



## Custom Fields AddPostOfficeForm

class PostofficeNameField(CharField):
    label = 'Почтамт',
    max_length = 100,
    help_text = ht,
    required = True,
    widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПОЧТАМТ'})

    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПОЧТАМТ" обязательное для заполнения.'), code='empty')

        query_unique = Postoffice.objects.filter(postoffice_name=value).exists()
        if query_unique:
            raise ValidationError(('Почтамт с именем "{}" уже зарегистрирован. Введите другое имя.'.format(value)), code='unique')


class IndexField(CharField):
    label = 'Индекс',
    max_length = 6,
    required = False,
    widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС'})

    # Validation
    def clean(self, value):
        if not all(l.isdigit() for l in value):
            raise ValidationError(('Поле "ИНДЕКС" должно состоять из цифр'), code='empty')

        if len(value) != 6:
            raise ValidationError(('Поле "ИНДЕКС" неправильной длины.'), code='length')


class AddPostofficeForm(forms.Form):
    postoffice_name = PostofficeNameField()
    index = IndexField()
    address = forms.CharField(label='Адрес', max_length=255, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС'}))
