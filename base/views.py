from django.shortcuts import render
from django.views import View
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout



class UserLogin(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            context = {'form': form}
            return render(request, 'login.html', context=context)
        else:
            return HttpResponseRedirect(reverse('main'))


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['login']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main'))

            else:
                error ='Неверное имя пользователя или пароль'
                context = {'form': form, 'error': error}
                return render(request, 'login.html', context=context)

        else:
            context = {'form': form}
            return render(request, 'login.html', context=context)



class UserLogout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))



class Main(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {'user': request.user, 'title': 'Главная', 'role': request.user.role}
            return render(request, 'main.html', context=context)
        else:
            return HttpResponseRedirect(reverse('login'))