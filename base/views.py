import numpy as np
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import LoginForm, AddPostofficeForm, AddCartridgeForm, AddCartridgesFileForm, AddPartForm, AddSupplyForm, ShowCartridgesForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Postoffice, Cartridge, Supply, Part, State
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import pandas
import json
import os
from datetime import datetime
import mimetypes
from acc_materials.settings import BASE_DIR

def get_errors_form(form):
    errors_dict = {}
    for field in form.errors:
        # field -> string
        for f in form:
            if field == f.name:
                errors_dict[f.label] = form.errors[field].as_text()

    errors_list = ['{}'.format(v) for k, v in errors_dict.items()]
    errors_str = "; ".join(errors_list).replace('*', '').replace('.', '')
    return errors_str



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
            messages.error(request, get_errors_form(form))

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

            if user.role == '2':
                postoffice = user.postoffice_id.postoffice_name
                request.session['num_active_supplies'] = Supply.objects.filter(
                    postoffice_recipient=postoffice,
                    status_sending=True,
                    status_receiving=False).count()
                context.update({'num_active_supplies': request.session['num_active_supplies']})

            return render(request, 'main.html', context=context)
        else:
            return HttpResponseRedirect(reverse('login'))



class ShowUsers(View):
    def get(self, request):
        context = {'title': 'Зарегистрированные пользователи'}

        user = request.user
        if user.role == '1':
            all_users = User.objects.all()
            context.update({'users': all_users})

        return render(request, 'showusers.html', context=context)



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
            messages.error(request, get_errors_form(form))

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
                messages.error(request, get_errors_form(form_single), extra_tags='single')

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
                messages.error(request, get_errors_form(form_multy), extra_tags='multy')


        if 'download_template_cartridges' in request.POST:
            try:
                path = os.path.join(BASE_DIR, 'base/static/misc/')
                filename = 'template_cartridges.xlsx'
                file = open(path+filename, 'rb')
                mime_type, _ = mimetypes.guess_type(path+filename)
                response = HttpResponse(file, content_type=mime_type)
                response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

                messages.success(request, '', extra_tags='download_template_cartridges')
                return response
            except Exception as e:
                messages.error(request, 'Ошибка скачивания файла ({})'.format(e), extra_tags='download_template_cartridges')

        return render(request, 'addcartridge.html', context=context)





class AddSupply(View):

    def get(self, request):
        context = {}
        user = request.user

        form_supply = AddSupplyForm()
        form_part = AddPartForm()

        supplies = Supply.objects.filter(status_sending=False)
        active_supplies = [k for k in supplies if Part.objects.filter(id_supply=k.pk).count()>0]
        ids = [i.pk for i in active_supplies]
        all_sup_wparts = [(Supply.objects.get(pk=p), Part.objects.filter(id_supply=p)) for p in ids]

        context.update({'user': user,
                        'title': 'Создать поставку картриджей на почтамт',
                        'form_part': form_part,
                        'form_supply': form_supply,
                        'supplies': all_sup_wparts})

        return render(request, 'addsupply.html', context=context)



    def post(self, request):
        context = {}
        form_supply = AddSupplyForm(request.POST)
        form_part = AddPartForm(request.POST)
        user = request.user

        context.update(
            {'title': 'Создать поставку картриджей на почтамт',
             'form_supply': form_supply,
             'form_part': form_part,
             'user': user})

        if 'but_supply' in request.POST:
            if form_supply.is_valid():
                postoffice = request.POST.get('postoffice_name')

                # save supply
                supply = Supply(postoffice_recipient=postoffice)
                supply.save()

                messages.success(request,
                                 '{} создана. Необходимо добавить позиции в поставку.'.format(supply),
                                 extra_tags='supply')
                return HttpResponseRedirect(reverse('add_supply'))
            else:
                messages.error(request, get_errors_form(form_supply), extra_tags='supply')


        if 'but_part' in request.POST:
            if form_part.is_valid():
                id_supply = request.POST.get('supply')
                supply = Supply.objects.get(pk=id_supply)

                nomenclature = request.POST.get('nomenclature_cartridge')
                amount = request.POST.get('amount')

                # save Part
                part = Part(id_supply=id_supply, postoffice=supply.postoffice_recipient, cartridge=nomenclature, amount=amount)
                part.save()

                messages.success(request,
                                 'Позиция в поставку ({}) добавлена.'.format(supply),
                                 extra_tags='part')
                return HttpResponseRedirect(reverse('add_supply'))
            else:
                messages.error(request, get_errors_form(form_part), extra_tags='part')



        if 'download_template_parts' in request.POST:
            try:
                path = os.path.join(BASE_DIR, 'base/static/misc/')
                filename = 'template_parts.xlsx'
                file = open(path + filename, 'rb')
                mime_type, _ = mimetypes.guess_type(path + filename)
                response = HttpResponse(file, content_type=mime_type)
                response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

                messages.success(request, '', extra_tags='download_template_parts')
                return response
            except Exception as e:
                messages.error(request, 'Ошибка скачивания файла ({})'.format(e), extra_tags='download_template_parts')


        id_sup_send = False
        for var in request.POST:
            if var.startswith('butsend'):
                id_sup_send = var.split('_')[1]

        if id_sup_send:
            user = request.user
            user_sender = '{0} ({1} {2})'.format(user.username, user.last_name, user.first_name)

            parts_send = Part.objects.filter(id_supply=id_sup_send)
            data_text = ''
            for p in parts_send:
                str_act = '{0}:{1};'.format(p.cartridge, p.amount)
                data_text += str_act

            date_sending = datetime.now()
            status_sending = True

            Supply.objects.filter(pk=id_sup_send).update(user_sender=user_sender,
                                                        data_text=data_text,
                                                        date_sending=date_sending,
                                                        status_sending=status_sending)
            return HttpResponseRedirect(reverse('add_supply'))


        id_part_del = False
        for var in request.POST:
            if var.startswith('butpartdel'):
                id_part_del = var.split('_')[1]

        if id_part_del:
            Part.objects.filter(pk=id_part_del).delete()
            return HttpResponseRedirect(reverse('add_supply'))

        id_sup_del = False
        for var in request.POST:
            if var.startswith('butsupdel'):
                id_sup_del = var.split('_')[1]

        if id_sup_del:
            Part.objects.filter(id_supply=id_sup_del).delete()
            Supply.objects.get(pk=id_sup_del).delete()
            return HttpResponseRedirect(reverse('add_supply'))

        supplies = Supply.objects.filter(status_sending=False)
        active_supplies = [k for k in supplies if Part.objects.filter(id_supply=k.pk).count() > 0]
        ids = [i.pk for i in active_supplies]
        all_sup_wparts = [(Supply.objects.get(pk=p), Part.objects.filter(id_supply=p)) for p in ids]

        context.update({'supplies': all_sup_wparts})

        return render(request, 'addsupply.html', context=context)



class ApplySupply(View):

    def get(self, request):
        context = {}

        postoffice = request.user.postoffice_id
        supplies = Supply.objects.filter(postoffice_recipient=postoffice, status_sending=True, status_receiving=False)
        ids = [i.pk for i in supplies]
        all_sup_wparts = [(Supply.objects.get(pk=p), Part.objects.filter(id_supply=p)) for p in ids]

        context.update({'supplies': all_sup_wparts})
        context.update({'num_active_supplies': request.session['num_active_supplies']})

        return render(request, 'applysupply.html', context=context)


    def post(self, request):
        context = {}

        id_but_apply = False
        for var in request.POST:
            if var.startswith('butapply'):
                id_but_apply = var.split('_')[1]

        if id_but_apply:
            supply = Supply.objects.get(pk=id_but_apply)
            user = request.user
            supply.user_recipient = '{0} ({1} {2})'.format(user.username, user.last_name, user.first_name)
            supply.date_receiving = datetime.now()
            supply.status_receiving = True


            # change State
            postoffice_apply = Postoffice.objects.get(postoffice_name=supply.postoffice_recipient)

            active_parts = Part.objects.filter(id_supply=supply.pk)
            for part in active_parts:
                    cartridge_apply = Cartridge.objects.get(nomenclature=part.cartridge)
                    state, state_created = State.objects.get_or_create(cartridge_id=cartridge_apply.pk, postoffice_id=postoffice_apply.pk)
                    if state_created:
                        state.total_amount = part.amount
                    else:
                        state.total_amount += part.amount
                    state.save()

            supply.save()  # !!!! after all actions

            #####
            postoffice = user.postoffice_id.postoffice_name
            request.session['num_active_supplies'] = Supply.objects.filter(
                postoffice_recipient=postoffice,
                status_sending=True,
                status_receiving=False).count()


            return HttpResponseRedirect(reverse('apply_supply'))

        postoffice = request.user.postoffice_id
        supplies = Supply.objects.filter(postoffice_recipient=postoffice, status_sending=True, status_receiving=False)
        ids = [i.pk for i in supplies]
        all_sup_wparts = [(Supply.objects.get(pk=p), Part.objects.filter(id_supply=p)) for p in ids]
        context.update({'supplies': all_sup_wparts})
        context.update({'num_active_supplies': request.session['num_active_supplies']})

        return render(request, 'applysupply.html', context=context)



class ShowCartridges(View):

    def get(self, request):
        context = {'title': 'Картриджи на почтамте'}

        user = request.user

        states = request.session.get('states', False)
        postoffice = request.session.get('postoffice', False)

        if postoffice:
            request.session['postoffice'] = False

        if isinstance(states, list):
            request.session['states'] = False
        else:
            ### по аналогии с post !
            postoffice = user.postoffice_id
            postoffice_id = Postoffice.objects.get(postoffice_name=postoffice).pk
            query = State.objects.filter(postoffice_id=postoffice_id)
            states = []
            for q in query:
                states.append([q.cartridge.nomenclature, q.total_amount])

        if user.role == '1':
            form = ShowCartridgesForm()
            context.update({'form': form})

        if user.role == '2':
            context.update({'num_active_supplies': request.session['num_active_supplies']})

        context.update({'states': states, 'postoffice': postoffice})

        return render(request, 'showcartridges.html', context=context)



    def post(self, request):
        context = {}
        form = ShowCartridgesForm(request.POST)
        context.update({'title': 'Картриджи на почтамте', 'form': form})

        if form.is_valid():
            postoffice_name = request.POST.get('postoffice_name')
            postoffice_id = Postoffice.objects.get(postoffice_name=postoffice_name).pk

            # !!!!!!!
            query = State.objects.filter(postoffice_id=postoffice_id)

            states = []
            for q in query:
                states.append([q.cartridge.nomenclature, q.total_amount])

            request.session['states'] = states
            request.session['postoffice'] = postoffice_name

            return HttpResponseRedirect(reverse('show_cartridges'))

        else:
            messages.error(request, get_errors_form(form))


        postoffice = request.user.postoffice_id
        postoffice_id = Postoffice.objects.get(postoffice_name=postoffice).pk

        query = State.objects.filter(postoffice_id=postoffice_id)
        states = []
        for q in query:
            states.append([q.cartridge.nomenclature, q.total_amount])

        context.update({'states': states, 'postoffice': postoffice, 'form': form})
        return render(request, 'showcartridges.html', context=context)


class ShowNomenclatures(View):
    def get(self, request):
        context = {'title': 'Зарегистрированные номенклатуры картриджей'}

        user = request.user
        if user.role == '2':
            context.update({'num_active_supplies': request.session['num_active_supplies']})

        cartridges = Cartridge.objects.all()

        # pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(cartridges, 15)
        try:
            nomenclatures = paginator.page(page)
        except PageNotAnInteger:
            nomenclatures = paginator.page(1)
        except EmptyPage:
            nomenclatures = paginator.page(paginator.num_pages)


        context.update({'nomenclatures': nomenclatures, 'range_visible': 2})

        return render(request, 'shownomenclatures.html', context=context)

