from django import forms

ht = '* Поле обязательное для заполнения'

class LoginForm(forms.Form):
    login = forms.CharField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ЛОГИН'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))


class AddPostofficeForm(forms.Form):
    name = forms.CharField(label='Почтамт', max_length=100, help_text=ht,
                           widget=forms.TextInput(attrs={'class': 'form-control form-control-sm required', 'placeholder': 'ПОЧТАМТ'}))
    index = forms.CharField(label='Индекс', max_length=6,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС'}))
    address = forms.CharField(label='Адрес', max_length=255,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС'}))