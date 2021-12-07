from django.views import View
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import LoginForm, AddPostofficeForm, AddCartridgeForm, AddCartridgesFileForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Postoffice, Cartridge
from django.contrib import messages


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
        user = request.user
        form = AddPostofficeForm()

        context.update({'user': user, 'title': 'Добавление почтамта', 'form': form})

        return render(request, 'addpostoffice.html', context=context)


    def post(self, request):
        context = {}
        form = AddPostofficeForm(request.POST)
        context.update({'title': 'Добавление почтамта', 'form': form })

        if form.is_valid():

            postoffice_name = request.POST.get('postoffice_name')
            index = request.POST.get('index')
            address = request.POST.get('address')

            # save
            postoffice = Postoffice(postoffice_name=postoffice_name, index=index, address=address)
            postoffice.save()
            messages.success(request, 'Почтамт добавлен')

            return HttpResponseRedirect(reverse('add_postoffice'))

        else:
            errors_dict = {}
            for field in form.errors:
                # field -> string
                for f in form:
                    if field == f.name:
                        errors_dict[f.label] = form.errors[field].as_text()

            errors_list = ['{}'.format(v) for k, v in errors_dict.items()]
            errors_str = "; ".join(errors_list)

            messages.error(request, errors_str)

        return render(request, 'addpostoffice.html', context=context)



class AddCartridge(View):

    def get(self, request):
        context = {}
        user = request.user

        form_single = AddCartridgeForm()
        form_multy = AddCartridgesFileForm()

        context.update({'user': user,
                        'title': 'Добавление номенклатуры картриджа',
                        'form_single': form_single,
                        'form_multy': form_multy})

        return render(request, 'addcartridge.html', context=context)

    def post(self, request):
        context = {}
        form = AddCartridgeForm(request.POST)
        context.update({'title': 'Добавление номенклатуры картриджа', 'form': form })

        if form.is_valid():

            nomenclature = request.POST.get('nomenclature')
            printer = request.POST.get('printer_model')
            drum = True if request.POST.get('is_drum') else False

            # save
            cartridge = Cartridge(nomenclature=nomenclature, printer_model=printer, is_drum=drum)
            cartridge.save()
            messages.success(request, 'Номенклатура картриджа добавлена')

            return HttpResponseRedirect(reverse('add_cartridge'))

        else:
            errors_dict = {}
            for field in form.errors:
                # field -> string
                for f in form:
                    if field == f.name:
                        errors_dict[f.label] = form.errors[field].as_text()

            errors_list = ['{}'.format(v) for k, v in errors_dict.items()]
            errors_str = "; ".join(errors_list)

            messages.error(request, errors_str)

        return render(request, 'addcartridge.html', context=context)