from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'ЛОГИН'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'ПАРОЛЬ'}))