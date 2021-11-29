from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ЛОГИН'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))