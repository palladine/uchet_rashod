import numpy as np
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import LoginForm, AddPostofficeForm, AddCartridgeForm, AddCartridgesFileForm, AddPartForm, AddSupplyForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Postoffice, Cartridge, Supply, Part
from django.contrib import messages
import pandas
import json

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
            errors_dict = {}
            for field in form.errors:
                # field -> string
                for f in form:
                    if field == f.name:
                        errors_dict[f.label] = form.errors[field].as_text()

            errors_list = ['{}'.format(v) for k, v in errors_dict.items()]
            errors_str = "; ".join(errors_list).replace('*', '').replace('.', '')

            messages.error(request, errors_str)

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
            errors_str = "; ".join(errors_list).replace('*', '').replace('.', '')

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


    def get_errors_form(self, form):
        errors_dict = {}
        for field in form.errors:
            # field -> string
            for f in form:
                if field == f.name:
                    errors_dict[f.label] = form.errors[field].as_text()

        errors_list = ['{}'.format(v) for k, v in errors_dict.items()]
        errors_str = "; ".join(errors_list).replace('*', '').replace('.', '')
        return errors_str


    def post(self, request):
        context = {}

        form_single = AddCartridgeForm(request.POST)
        form_multy = AddCartridgesFileForm(request.POST, request.FILES)
        context.update({'title': 'Добавление номенклатуры картриджа', 'form_single': form_single, 'form_multy': form_multy})

        if 'single' in request.POST:
            if form_single.is_valid():
                nomenclature = request.POST.get('nomenclature').strip()
                printer = request.POST.get('printer_model')
                source = request.POST.get('source')
                drum = True if request.POST.get('is_drum') else False

                # save
                cartridge = Cartridge(nomenclature=nomenclature, printer_model=printer, is_drum=drum, source=source)
                cartridge.save()
                messages.success(request, 'Номенклатура картриджа добавлена', extra_tags='single')

                return HttpResponseRedirect(reverse('add_cartridge'))

            else:
                messages.error(request, self.get_errors_form(form_single), extra_tags='single')

        if 'multy' in request.POST:
            if form_multy.is_valid():
                file_object = form_multy.cleaned_data.get('file')
                file_bytes = file_object.read()

                wb = pandas.read_excel(file_bytes)  #  wb -----> DataFrame

                count_created = 0
                for unit in wb.to_numpy():
                    nomenclature = unit[0].strip()
                    printer = unit[1]
                    drum = True if str(unit[2]).strip() == 'Да' or unit[2] == 1 else False
                    source = '' if str(unit[3]) == 'nan' else str(unit[3])


                    # save
                    obj, created = Cartridge.objects.filter(nomenclature=nomenclature).get_or_create(
                        nomenclature=nomenclature,
                        printer_model=printer,
                        is_drum=drum,
                        source=source)
                    if created:
                        count_created += 1


                messages.success(request, f'Номенклатуры картриджей добавлены ({count_created} позиций)', extra_tags='multy')
                return HttpResponseRedirect(reverse('add_cartridge'))
            else:
                messages.error(request, self.get_errors_form(form_multy), extra_tags='multy')


        return render(request, 'addcartridge.html', context=context)





class AddSupply(View):

    def get(self, request):
        context = {}
        user = request.user

        form_supply = AddSupplyForm()
        form_part = AddPartForm()

        supplies = Supply.objects.filter(status_sending=False)
        ids = [i.pk for i in supplies]


        context.update({'user': user,
                        'title': 'Создать поставку картриджей на почтамт',
                        'form_part': form_part,
                        'form_supply': form_supply})



        return render(request, 'addsupply.html', context=context)



    def post(self, request):

        form_supply = AddSupplyForm(request.POST)
        form_part = AddPartForm(request.POST)


        if 'but_supply' in request.POST:
            if form_supply.is_valid():
                postoffice = request.POST.get('postoffice_name')

                # save
                supply = Supply(postoffice_recipient=postoffice)
                supply.save()

                messages.success(request,
                                 '{} создана. Необходимо добавить позиции в поставку.'.format(supply),
                                 extra_tags='supply')

            return HttpResponseRedirect(reverse('add_supply'))

        if 'but_part' in request.POST:
            if form_part.is_valid():
                id_supply = request.POST.get('supply')
                supply = Supply.objects.get(pk=id_supply)


                # TODO session, output table parts, save Supply !
                nomenclature = request.POST.get('nomenclature_cartridge')
                amount = request.POST.get('amount')

                # save Part
                part = Part(id_supply=id_supply, postoffice=supply.postoffice_recipient, nomenclature=nomenclature, amount=amount)
                part.save()

                messages.success(request,
                                 'Позиция в поставку ({}) добавлена.'.format(supply),
                                 extra_tags='part')

            return HttpResponseRedirect(reverse('add_supply'))

