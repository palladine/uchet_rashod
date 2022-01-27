import os.path
from django import forms
from django.forms import CharField, FileField, ModelChoiceField
from django.core.exceptions import ValidationError
from .models import User, Cartridge, Postoffice, Supply


ht = '* Поле обязательное для заполнения'



# ---------------  Login custom fields and form ---------------
class LoginField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ЛОГИН" обязательное для заполнения'), code='empty')

        query_unique = Postoffice.objects.filter(postoffice_name=value).exists()
        if query_unique:
            raise ValidationError(('Пользователь с именем "{}" уже зарегистрирован, введите другое имя'.format(value)),
                                  code='unique')

class PasswordField(CharField):
    # Validation
    def clean(self, value):
        if not value:
            raise ValidationError(('Поле "ПАРОЛЬ" обязательное для заполнения'), code='empty')


class LoginForm(forms.Form):
    login = LoginField(label='Имя пользователя',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ЛОГИН', 'autocomplete': 'off'}))
    password = PasswordField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПАРОЛЬ'}))
# --------------- End Login ---------------



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
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ПОЧТАМТ'}))
    index = IndexField(label='Индекс', max_length=6, required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС'}))
    address = forms.CharField(label='Адрес', max_length=255, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС'}))
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
                                             queryset=Postoffice.objects.all(),
                                             help_text=ht, required=True,
                                             to_field_name='postoffice_name',
                                             empty_label='ВЫБЕРИТЕ ПОЧТАМТ ...',
                                             widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
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

class AddPartForm(forms.Form):
    supply = SupplyField(label='Поставка',
                        queryset=Supply.objects.filter(status_sending = False),
                        help_text=ht, required=True,
                        to_field_name='pk',
                        empty_label='ВЫБЕРИТЕ ПОСТАВКУ ...',
                        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    nomenclature_cartridge = NomenclaturePartField(label='Номенклатура картриджа',
                                                    queryset=Cartridge.objects.all(),
                                                    help_text=ht, required=True,
                                                    to_field_name='nomenclature',
                                                    empty_label='ВЫБЕРИТЕ НОМЕНКЛАТУРУ ...',
                                                    widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    amount = AmountField(label='Количество', help_text=ht, required=True,
                        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'КОЛИЧЕСТВО'}))
# --------------- End Add Supply ---------------



# ---------------  Show Cartridges custom fields and form ---------------
class ShowCartridgesForm(forms.Form):
    postoffice_name = PostofficeField(label='Почтамт',
                                             queryset=Postoffice.objects.all(),
                                             help_text=ht, required=True,
                                             to_field_name='postoffice_name',
                                             empty_label='ВЫБЕРИТЕ ПОЧТАМТ ...',
                                             widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
# --------------- End Show Cartridges ---------------



# ---------------  Add OPS custom fields and form ---------------
class AddOPSForm(forms.Form):
    postoffice_name = PostofficeField(label='Почтамт',
                                          queryset=Postoffice.objects.all(),
                                          help_text=ht, required=True,
                                          to_field_name='postoffice_name',
                                          empty_label='ВЫБЕРИТЕ ПОЧТАМТ ...',
                                          widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    index = IndexField(label='Индекс ОПС', max_length=6, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС ОПС'}))
    address = forms.CharField(label='Адрес ОПС', max_length=255, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС ОПС'}))
# --------------- End Add OPS ---------------



# ---------------  Add OPS custom fields and form for User ---------------
class AddOPSForm_U(forms.Form):
    index = IndexField(label='Индекс ОПС', max_length=6, help_text=ht, required=True,
                       widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ИНДЕКС ОПС'}))
    address = forms.CharField(label='Адрес ОПС', max_length=255, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'АДРЕС ОПС'}))
# --------------- End Add OPS for User ---------------