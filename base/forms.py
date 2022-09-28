import os.path
from django import forms
from django.forms import CharField, FileField, ModelChoiceField, EmailField, DateField, DateInput
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User, Cartridge, Postoffice, State,  Supply, OPS, Supply_OPS, Group


ht = '* Поле обязательное для заполнения'

# Implementation html Datalist
class DataListWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, user=None, **kwargs):
        super(DataListWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name})
        self.user = user

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(DataListWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name

        for item in self._list:
            if self.user and self.user.is_staff:
                data_list += f'<option data-value="{item.pk}" value="{item} [{item.group}]"></option>'
            else:
                data_list += f'<option data-value="{item.pk}" value="{item}"></option>'
        data_list += '</datalist>'
        return (text_html + data_list)


# ---------------  Login custom fields and form ---------------
class LoginField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ЛОГИН" обязательное для заполнения'), code='empty')


class PasswordField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПАРОЛЬ" обязательное для заполнения'), code='empty')


class LoginForm(forms.Form):
    login = LoginField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИМЯ ПОЛЬЗОВАТЕЛЯ (ЛОГИН)', 'autocomplete': 'off'}))
    password = PasswordField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))
# --------------- End Login ---------------



# ---------------  Add Group custom fields and form ---------------
class GroupNameField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ИМЯ ГРУППЫ" обязательное для заполнения'), code='empty')

        query_unique = Group.objects.filter(group_name=value).exists()
        if query_unique:
            raise ValidationError(('Группа с именем "{}" уже зарегистрирован. Введите другое имя'.format(value)), code='unique')


class AddGroupForm(forms.Form):
    group_name = GroupNameField(label='Группа', max_length=255, help_text=ht, required=True,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                                      'placeholder': 'ИМЯ ГРУППЫ', 'autocomplete': 'off'}))
# --------------- End Add Group ---------------



# ---------------  Add Postoffice custom fields and form ---------------
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
        if value:
            if not all(l.isdigit() for l in value):
                raise ValidationError(('Поле "ИНДЕКС" должно состоять из цифр'), code='isdigit')

            if len(value) != 6:
                raise ValidationError(('Поле "ИНДЕКС" неправильной длины'), code='length')
        else:
            raise ValidationError(('Поле "ИНДЕКС" обязательное для заполнения'), code='empty')


class AddPostofficeForm(forms.Form):
    postoffice_name = PostofficeNameField(label='Почтамт', max_length=100, help_text=ht, required=True,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                                      'placeholder': 'ПОЧТАМТ',
                                                      'autocomplete': 'off'}))
    index = IndexField(label='Индекс', max_length=6, required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС'}))
    address = CharField(label='Адрес', max_length=255, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС'}))



class AddGroupField(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ИМЯ ГРУППЫ" обязательное для заполнения'), code='empty')


class AddPostofficeGroupForm(forms.Form):
    group = AddGroupField(label='Группа',
                                 queryset=None,
                                 help_text=ht, required=True,
                                 to_field_name='group_name',
                                 widget=None)

    postoffice_name = PostofficeNameField(label='Почтамт', max_length=100, help_text=ht, required=True,
                                          widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                                                        'placeholder': 'ПОЧТАМТ',
                                                                        'autocomplete': 'off'}))
    index = IndexField(label='Индекс', max_length=6, required=False,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС'}))
    address = forms.CharField(label='Адрес', max_length=255, required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС'}))

    def __init__(self, *args, **kwargs):
        super(AddPostofficeGroupForm, self).__init__(*args, **kwargs)

        self.fields['group'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                                 'placeholder': 'ВЫБЕРИТЕ ГРУППУ ...',
                                                                 'autocomplete': 'off'},
                                                     data_list=Group.objects.all().order_by('group_name'),
                                                          name='datalist_group')
# --------------- End Add Postoffice ---------------



# ---------------  Add Cartridge custom fields and form ---------------
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
# --------------- End Add Cartridge ---------------



# ---------------  Add Cartridges from file custom fields and form ---------------
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
                        widget=forms.FileInput(attrs={'class': 'form-control form-control-sm',
                                                      'placeholder': 'ВЫБЕРИТЕ ФАЙЛ ...',
                                                      'id': 'file',
                                                      'style': 'display: none;'}))
# --------------- End Add Cartridges from file ---------------



# --------------- Add OPS from file ---------------
class AddOPSFileForm(forms.Form):
    file = WorkFile(label='Файл', max_length=100, help_text=ht, required=True,
                        widget=forms.FileInput(attrs={'class': 'form-control form-control-sm',
                                                      'placeholder': 'ВЫБЕРИТЕ ФАЙЛ ...',
                                                      'id': 'file',
                                                      'style': 'display: none;'}))
# --------------- End Add OPS from file ---------------



# ---------------  Add Supply and Parts from file custom fields and form ---------------
class AddPartsFileForm(forms.Form):
    file = WorkFile(label='Файл', max_length=100, help_text=ht, required=True,
                    widget=forms.FileInput(attrs={'class': 'form-control form-control-sm',
                                                  'placeholder': 'ВЫБЕРИТЕ ФАЙЛ ...',
                                                  'id': 'file',
                                                  'style': 'display: none;'}))
# --------------- End Add Supply and Parts from file ---------------



# ---------------  Add Supply custom fields and form ---------------
class PostofficeField(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПОЧТАМТ" обязательное для заполнения'), code='empty')


class AddSupplyForm(forms.Form):
    postoffice_name = PostofficeField(label='Почтамт',
                                 queryset=None,
                                 help_text=ht, required=True,
                                 to_field_name='postoffice_name',
                                 widget=None)

    def __init__(self, user, *args, **kwargs):
        super(AddSupplyForm, self).__init__(*args, **kwargs)

        qs = Postoffice.objects.filter(group=user.group).order_by('postoffice_name')

        self.fields['postoffice_name'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                              'placeholder': 'ВЫБЕРИТЕ ПОЧТАМТ ...',
                                                              'autocomplete': 'off'}, data_list=qs,
                                                               name='datalist_postoffice', user=user)
# --------------- End Add Supply ---------------



# ---------------  Add Part custom fields and form ---------------
class SupplyField(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПОСТАВКА" обязательное для заполнения'), code='empty')

class NomenclaturePartField(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "НОМЕНКЛАТУРА" обязательное для заполнения'), code='empty')

class AmountField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "КОЛИЧЕСТВО" обязательное для заполнения'), code='empty')
        if int(value) < 0:
            raise ValidationError(('Значение в поле "КОЛИЧЕСТВО" должно быть положительное'), code='negotive')

class AddPartForm(forms.Form):
    supply = SupplyField(label='Поставка',
                        queryset=None,
                        help_text=ht, required=True,
                        to_field_name='pk',
                        widget=None)

    nomenclature_cartridge = NomenclaturePartField(label='Номенклатура картриджа',
                                                   queryset=None,
                                                   help_text=ht, required=True,
                                                   to_field_name='nomenclature',
                                                   widget=None)
    amount = AmountField(label='Количество', help_text=ht, required=True,
                        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'КОЛИЧЕСТВО'}))


    def __init__(self, user, *args, **kwargs):
        super(AddPartForm, self).__init__(*args, **kwargs)

        postoffices = Postoffice.objects.filter(group=user.group)
        postoffices_names = [name.postoffice_name for name in postoffices]
        qs = Supply.objects.filter(status_sending=False, postoffice_recipient__in=postoffices_names).order_by('-id')

        self.fields['supply'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                'placeholder': 'ВЫБЕРИТЕ ПОСТАВКУ ...',
                                                'autocomplete': 'off'}, data_list=qs, name='datalist_supply')

        sklad_po = Postoffice.objects.get(as_base=True)
        cartridges_sklad = State.objects.filter(postoffice=sklad_po, total_amount__gt=0)
        ctr = [c.cartridge.nomenclature for c in cartridges_sklad]
        self.fields['nomenclature_cartridge'].queryset = Cartridge.objects.filter(nomenclature__in=ctr)
        self.fields['nomenclature_cartridge'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                                                'placeholder': 'ВЫБЕРИТЕ НОМЕНКЛАТУРУ ...'},
                                                                         data_list=Cartridge.objects.filter(nomenclature__in=ctr).order_by('nomenclature'),
                                                                      name='datalist_cartridges')
# --------------- End Add Part  ---------------



# ---------------  Show Cartridges custom fields and form ---------------
class ShowCartridgesForm(forms.Form):
    postoffice_name = PostofficeField(label='Почтамт',
                                 queryset=None,
                                 help_text=ht, required=True,
                                 to_field_name='postoffice_name',
                                 widget=None)

    def __init__(self, user, *args, **kwargs):
        super(ShowCartridgesForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            qs = Postoffice.objects.all().order_by('group__group_name')
        else:
            qs = Postoffice.objects.filter(group=user.group).order_by('postoffice_name')

        self.fields['postoffice_name'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                              'placeholder': 'ВЫБЕРИТЕ ПОЧТАМТ ...',
                                                              'autocomplete': 'off'}, data_list=qs,
                                                               name='datalist_postoffice', user=user)


# --------------- End Show Cartridges ---------------



# ---------------  Add OPS custom fields and form ---------------
class AddOPSForm(forms.Form):
    postoffice_name = PostofficeField(label='Почтамт',
                                 queryset=None,
                                 help_text=ht, required=True,
                                 to_field_name='postoffice_name',
                                 widget=None)
    index = IndexField(label='Индекс ОПС', max_length=6, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС ОПС'}))
    address = forms.CharField(label='Адрес ОПС', max_length=255, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС ОПС'}))

    def __init__(self, user, *args, **kwargs):
        super(AddOPSForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            qs = Postoffice.objects.all().order_by('group__group_name')
        else:
            qs = Postoffice.objects.filter(group=user.group).order_by('postoffice_name')
        self.fields['postoffice_name'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                              'placeholder': 'ВЫБЕРИТЕ ПОЧТАМТ ...',
                                                              'autocomplete': 'off'},
                                                       data_list=qs, name='datalist_postoffice', user=user)
# --------------- End Add OPS ---------------



# ---------------  Add OPS custom fields and form for User (Not administrator) ---------------
class AddOPSForm_U(forms.Form):
    index = IndexField(label='Индекс ОПС', max_length=6, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС ОПС'}))
    address = forms.CharField(label='Адрес ОПС', max_length=255, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС ОПС'}))
# --------------- End Add OPS for User (Not Administrator) ---------------



# ---------------  Add Supply OPS custom fields and form ---------------
class OPSField(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ОПС" обязательное для заполнения'), code='empty')


class TaskNaumenField(CharField):
    def clean(self, value):
        if value:
            if not((value[0:2].lower() == 'rp' and value[2:].isdigit()) or value.isdigit()):
                raise ValidationError(('Поле "НОМЕР ЗАПРОСА В NAUMEN" неправильного формата'), code='isdigit')

class AddSupplyOPSForm(forms.Form):
    ops = OPSField(label='ОПС',
                   queryset=None,
                   help_text=ht, required=True,
                   widget=None)


    task_naumen = TaskNaumenField(label='Номер запроса в Naumen', max_length=10, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                                            'placeholder': 'НОМЕР ЗАПРОСА В NAUMEN',
                                                            'autocomplete': 'off'}))

    def __init__(self, po, *args, **kwargs):
        super(AddSupplyOPSForm, self).__init__(*args, **kwargs)
        self.fields['ops'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                'placeholder': 'ВЫБЕРИТЕ ОПС ...',
                                                'autocomplete': 'off'},
                                         data_list=OPS.objects.filter(postoffice=po).order_by('index'), name='datalist_ops')
# --------------- End Add Supply OPS ---------------


# ---------------  Add Part OPS custom fields and form ---------------
class SupplyOPSField(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПОСТАВКА" обязательное для заполнения'), code='empty')

class AddPartOPSForm(forms.Form):
    supply_ops = SupplyOPSField(label='Поставка на опс',
                                queryset=None,
                                help_text=ht, required=True,
                                to_field_name='pk',
                                widget=None)

    nomenclature_cartridge = NomenclaturePartField(label='Номенклатура картриджа',
                                                   queryset=None,
                                                   help_text=ht, required=True,
                                                   to_field_name='nomenclature',
                                                   widget=None)

    amount = AmountField(label='Количество', help_text=ht, required=True,
                         widget=forms.NumberInput(
                             attrs={'class': 'form-control form-control-sm', 'placeholder': 'КОЛИЧЕСТВО'}))

    def __init__(self, po, *args, **kwargs):
        super(AddPartOPSForm, self).__init__(*args, **kwargs)
        self.fields['supply_ops'].queryset = Supply_OPS.objects.filter(ops_recipient__postoffice=po, status_sending=False)
        self.fields['supply_ops'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                'placeholder': 'ВЫБЕРИТЕ ПОСТАВКУ ...',
                                                'autocomplete': 'off'},
                                                data_list=Supply_OPS.objects.filter(ops_recipient__postoffice=po,
                                                                             status_sending=False).order_by('-id'), name='datalist_supply_ops')

        cartridges_po = State.objects.filter(postoffice=po, total_amount__gt=0)
        ctr = [c.cartridge.nomenclature for c in cartridges_po]
        self.fields['nomenclature_cartridge'].queryset = Cartridge.objects.filter(nomenclature__in=ctr)
        self.fields['nomenclature_cartridge'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                'placeholder': 'ВЫБЕРИТЕ НОМЕНКЛАТУРУ ...',
                                                'autocomplete': 'off'},
                                                data_list=Cartridge.objects.filter(nomenclature__in=ctr).order_by('nomenclature'),
                                                                      name='datalist_cartridges')
# --------------- End Add Part OPS  ---------------



# ---------------  Add User custom fields and form ---------------
class AddUserLoginField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ИМЯ ПОЛЬЗОВАТЕЛЯ" обязательное для заполнения'), code='empty')

        query_unique = User.objects.filter(username=value).exists()
        if query_unique:
            raise ValidationError(('Пользователь с именем "{}" уже зарегистрирован, введите другое имя'.format(value)),
                                  code='unique')

class AddUserLastnameField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ФАМИЛИЯ" обязательное для заполнения'), code='empty')

class AddUserFirstnameField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ИМЯ" обязательное для заполнения'), code='empty')

class AddUserMiddlenameField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ОТЧЕСТВО" обязательное для заполнения'), code='empty')

class AddUserEmailField(EmailField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "E-MAIL" обязательное для заполнения'), code='empty')

        result = validate_email(value)



class AddUserForm(forms.Form):
    login = AddUserLoginField(label='Имя пользователя',
                       max_length=100, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИМЯ ПОЛЬЗОВАТЕЛЯ (ЛОГИН)', 'autocomplete': 'off'}))

    password = PasswordField(label='Пароль', help_text=ht, widget=forms.PasswordInput(
                                 attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))

    firstname = AddUserFirstnameField(label='Имя', max_length=100, help_text=ht, required=True,
                                      widget=forms.TextInput(
                                          attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИМЯ',
                                                 'autocomplete': 'off'}))

    lastname = AddUserLastnameField(label='Фамилия', max_length=100, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ФАМИЛИЯ', 'autocomplete': 'off'}))


    middlename = AddUserMiddlenameField(label='Отчество', max_length=100, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ОТЧЕСТВО', 'autocomplete': 'off'}))


    postoffice = PostofficeField(label='Почтамт',
                                 queryset=None,
                                 help_text=ht, required=True,
                                 to_field_name='postoffice_name',
                                 widget=None)

    email = AddUserEmailField(label='E-mail', max_length=255, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'E-MAIL', 'autocomplete': 'off'}))


    def __init__(self, user, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            qs = Postoffice.objects.all().order_by('group__group_name')
        else:
            qs = Postoffice.objects.filter(group=user.group).order_by('postoffice_name')

        self.fields['postoffice'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                              'placeholder': 'ВЫБЕРИТЕ ПОЧТАМТ ...',
                                                              'autocomplete': 'off'}, data_list=qs,
                                                          name='datalist_postoffice', user=user)
# --------------- End Add User ---------------



# --------------- Show OPS form ---------------
class ShowOPSForm(forms.Form):
    group = AddGroupField(label='Группа',
                          queryset=None,
                          help_text=ht, required=True,
                          to_field_name='group_name',
                          widget=None)

    def __init__(self, *args, **kwargs):
        super(ShowOPSForm, self).__init__(*args, **kwargs)

        self.fields['group'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                            'placeholder': 'ВЫБЕРИТЕ ГРУППУ ...',
                                                            'autocomplete': 'off'},
                                                     data_list=Group.objects.all().order_by('group_name'),
                                                     name='datalist_group')
# --------------- End Show OPS form ---------------



# --------------- Show Refuse form ---------------
class PostofficeFieldEmpty(ModelChoiceField):
    # Validation
    def clean(self, value):
        if not value:
            #raise ValidationError(('Поле "ПОЧТАМТ" обязательное для заполнения'), code='empty')
            return value


class ShowRefuseForm(forms.Form):
    postoffice = PostofficeFieldEmpty(label='Почтамт',
                                 queryset=Postoffice.objects.none(),
                                 help_text=ht, required=False,
                                 to_field_name='postoffice_name',
                                 widget=None)

    date_s = DateField(label="C", required=False,
                       widget=DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm',
                                               'placeholder': 'ДАТА С ...',
                                               'min': "2022-01-01",
                                                'max': "2099-01-01"}), localize=True)

    date_p = DateField(label="По", required=False,
                       widget=DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm',
                                               'placeholder': 'ДАТА ПО ...',
                                               'min': "2022-01-01",
                                               'max': "2099-01-01"}), localize=True)

    def __init__(self, user, *args, **kwargs):
        super(ShowRefuseForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            qs = Postoffice.objects.all().order_by('group__group_name')
        else:
            qs = Postoffice.objects.filter(group=user.group).order_by('postoffice_name')

        self.fields['postoffice'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                              'placeholder': 'ВЫБЕРИТЕ ПОЧТАМТ ...',
                                                              'autocomplete': 'off'}, data_list=qs,
                                                          name='datalist_postoffice', user=user)



    # def clean_postoffice(self):
    #     postoffice_name = self.cleaned_data['postoffice']
    #
    #     print('!!!!!!! ', postoffice_name)
    #
    #     return postoffice_name




# --------------- End Show Refuse form ---------------



# --------------- Show Refuse form User ---------------
class ShowRefuseFormUser(forms.Form):
    date_s = DateField(label="C", required=False,
                       widget=DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm',
                                               'placeholder': 'ДАТА С ...',
                                               'min': "2022-01-01",
                                               'max': "2099-01-01"}), localize=True)

    date_p = DateField(label="По", required=False,
                       widget=DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm',
                                               'placeholder': 'ДАТА ПО ...',
                                               'min': "2022-01-01",
                                               'max': "2099-01-01"}), localize=True)
# --------------- End Show Refuse form User ---------------



# --------------- Autoorder form part change ---------------
class AmountPartField(CharField):
    # Validation
    def clean(self, value):
        if value:
            if not all(l.isdigit() for l in value):
                raise ValidationError((''), code='isdigit')

            if len(value) > 3:
                raise ValidationError((''), code='length')
        else:
            raise ValidationError((''), code='empty')

class AutoorderFormPartChange(forms.Form):
    amount = AmountPartField(label="Количество", max_length=3, required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control form-control-sm px-1',
                                                       'placeholder': '',
                                                       'autocomplete': 'off'}))
# --------------- End Autoorder form part change ---------------



# --------------- Autoorder form new part change ---------------
class AutoorderFormNewPart(forms.Form):
    nomenclature_cartridge = NomenclaturePartField(label='Номенклатура картриджа',
                                                   queryset=None,
                                                   help_text=ht, required=False,
                                                   to_field_name='nomenclature',
                                                   widget=None)

    amount_newpart = AmountField(label='Количество', max_length=3, required=False,
                         widget=forms.NumberInput(
                             attrs={'class': 'form-control form-control-sm px-1',
                                    'placeholder': '',
                                    'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        super(AutoorderFormNewPart, self).__init__(*args, **kwargs)
        self.fields['nomenclature_cartridge'].widget = DataListWidget(
            attrs={'class': 'form-select form-select-sm datalist', 'placeholder': 'НОМЕНКЛАТУРА ...'},
            data_list=Cartridge.objects.all().order_by('nomenclature'),
            name='datalist_cartridges')

# --------------- End Autoorder form new part change ---------------



# --------------- Show order form ----------------------------------
class ShowOrderForm(forms.Form):
    postoffice_name = PostofficeField(label='Почтамт',
                                 queryset=None,
                                 help_text=ht, required=True,
                                 to_field_name='postoffice_name',
                                 widget=None)

    def __init__(self, user, *args, **kwargs):
        super(ShowOrderForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            qs = Postoffice.objects.all().order_by('group__group_name')
        else:
            qs = Postoffice.objects.filter(group=user.group).order_by('postoffice_name')

        self.fields['postoffice_name'].widget = DataListWidget(attrs={'class': 'form-select form-select-sm datalist',
                                                              'placeholder': 'ВЫБЕРИТЕ ПОЧТАМТ ...',
                                                              'autocomplete': 'off'}, data_list=qs,
                                                               name='datalist_postoffice', user=user)

# --------------- End Show Cartridges ---------------


# --------------- Change amount autoorder form ------
class ChangeAmountAutoorderForm(forms.Form):
    new_amount = AmountField(label='Количество', max_length=3, required=False,
                                 widget=forms.NumberInput(
                                     attrs={'class': 'form-control form-control-sm px-1',
                                            'placeholder': '',
                                            'autocomplete': 'off'}))
# --------------- End change amount autoorder -------
