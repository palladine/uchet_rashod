from django.shortcuts import render
from django.views import View
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, AddPostofficeForm
from django.contrib.auth import authenticate, login, logout
from .models import Postoffice



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
            user = request.user
            context = {'user': user,
                       'title': 'Главная'}
            return render(request, 'main.html', context=context)
        else:
            return HttpResponseRedirect(reverse('login'))


class AddPostoffice(View):
    def get(self, request):
        context = {}

        msg = request.session.get('msg', False)
        error = request.session.get('error', False)
        request.session['msg'] = False
        request.session['error'] = False

        user = request.user
        form = AddPostofficeForm()
        context.update({'user': user, 'title': 'Добавление почтамта', 'form': form, 'msg': msg, 'error': error})
        return render(request, 'addpostoffice.html', context=context)

    def post(self, request):

        form = AddPostofficeForm(request.POST)
        context = { 'form': form }
        if form.is_valid():
            name = request.POST.get('name')
            index = request.POST.get('index')
            address = request.POST.get('address')

            # save
            postoffice = Postoffice(name=name, index=index, address=address)
            postoffice.save()
            request.session['msg'] = 'Почтамт добавлен'

            return HttpResponseRedirect(reverse('add_postoffice'))
        else:
            request.session['error'] = form.errors
        return render(request, 'addpostoffice.html', context=context)