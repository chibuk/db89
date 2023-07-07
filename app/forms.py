import re
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from app.models import Document, Organization, RootOrganization, Item, DocumentItem


class DocumentForm(ModelForm):

    receiver1 = forms.CharField(label='Получатель')

    class Meta:
        model = Document
        exclude = ['root'] #, 'sender', 'receiver', 'payer']

    def clean_city(self):
        data = self.cleaned_data['city']
        text = ''
        for word in data.split():
            if re.match(r'^([А-я]+)-*([А-я]+)$', word):
                text += word.title() + " "
            else:
                raise ValidationError('Только слова через пробел или дефис.')
        return text.strip()


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ["root"]


class UserRegistrationForm(ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают!')
        return password2


class RootOrganizationCreateForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ['root']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['root']
