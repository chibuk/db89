from datetime import datetime
from django_xhtml2pdf.views import PdfMixin
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.aggregates import Max, Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet

from app.models import Document, AppUser, RootOrganization, Organization, Item, DocumentItem
from django.views.generic import ListView, DetailView
from app.forms import DocumentForm, OrganizationForm, UserRegistrationForm, RootOrganizationCreateForm, ItemForm
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
# Create your views here.
from django.http import HttpResponse
from app.serializers import OrganizationSerializer, DocumentSerializer, DocumentItemSerializer, ItemSerializer
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
import requests


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('document-list'))
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


class QueryRootMixin:
    """Предотвращает показ всех объектов из БД, которые могут принадлежать другим профиляи.
    Переопределяет метод, для возврата queryset в котором есть объекты только данной текущей (профиль) организации
    (поле root), т.е. делает фильрацию по root равному текущей организации"""

    def get_queryset(self):
        queryset = self.model.objects.filter(root=self.request.user.appuser.root_organization)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class CreateRootMixin:
    """Добавим к сохраняемому объекту значение текущего профиля RootOrganization"""

    def form_valid(self, form):
        form.instance.root = self.request.user.appuser.root_organization
        return super().form_valid(form)


# <API>
class OrganizationAPIListView(ListCreateAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        queryset = Organization.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(root=self.request.user.appuser.root_organization)


class DocumentAPIListView(ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset


class DocumentItemAPIListView(ListCreateAPIView):
    serializer_class = DocumentItemSerializer

    def get_queryset(self):
        queryset = DocumentItem.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset


# ModelViewSets
class ItemAPIModelView(ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.filter(root=self.request.user.appuser.root_organization)
        # queryset = Item.objects.filter(root=RootOrganization.objects.last())   #dev
        return queryset

    def perform_create(self, serializer):
        serializer.save(root=self.request.user.appuser.root_organization)

    def search(self, request, keyword, *args, **kwargs):
        # keyword = kwargs.get["keyword"]
        # keyword = request.query_params["keyword"]
        queryset = self.filter_queryset(self.get_queryset()).filter(name__icontains=keyword)
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DocumentAPIModelView(ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset

    def perform_create(self, serializer):
        _root = self.request.user.appuser.root_organization
        _data = self.request.data
        serializer.save(root=_root,
                        sender=Organization.objects.filter(root=_root).get(id=_data['sender']),
                        receiver=Organization.objects.filter(root=_root).get(id=_data['receiver']),
                        payer=Organization.objects.filter(root=_root).get(id=_data['payer']))

    def last(self, request, *args, **kwargs):
        # field = request.query_params["field"]
        instance = self.get_queryset().last()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DocumentitemAPIModelView(ModelViewSet):
    serializer_class = DocumentItemSerializer

    def get_queryset(self):
        queryset = DocumentItem.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset
    """После создания, изменения или удаления, пересчет суммы в связанном документе"""
    def calculatedocsum (self, doc_id):
        _document = Document.objects.get(id=doc_id)
        _items = self.get_queryset().filter(document=_document)  # Все строки
        _document.doc_sum = 0  # сброс значения
        for item in _items:
            _document.doc_sum += item.item_sum  # суммируем поля
        _document.save()

    def perform_create(self, serializer):
        _root = self.request.user.appuser.root_organization
        _data = self.request.data
        _document = Document.objects.filter(root=_root).get(id=_data['document'])
        serializer.save(root=_root,
                        document=_document,
                        item=Item.objects.filter(root=_root).get(name=_data['name']))
        self.calculatedocsum(doc_id=_data['document'])

    def perform_destroy(self, instance):
        _id = instance.document.id
        instance.delete()
        self.calculatedocsum(doc_id=_id)

    def perform_update(self, serializer):
        _id = self.request.data['document']
        serializer.save()
        self.calculatedocsum(doc_id=_id)

    """Возвращает список объектов, принадлежащих документу id URL...doclist?doc_id=id"""
    def document_list (self, request, *args, **kwargs):
        _doc_id = request.query_params['doc_id']
        queryset = self.filter_queryset(self.get_queryset()).filter(document=_doc_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrganizationAPIModelView(ModelViewSet):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        queryset = Organization.objects.filter(root=self.request.user.appuser.root_organization)
        # queryset = Organization.objects.filter(root=RootOrganization.objects.last())    #dev
        return queryset

    def perform_create(self, serializer):
        serializer.save(root=self.request.user.appuser.root_organization)

    def search(self, request, keyword, *args, **kwargs):
        # keyword = kwargs.get["keyword"]
        # keyword = request.query_params["keyword"]
        queryset = self.filter_queryset(self.get_queryset()).filter(
            Q(name__icontains=keyword) | Q(inn__icontains=keyword))
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DocumentNumber(LoginRequiredMixin, APIView):
    """Выдает очередной номер для нового документа по правилам именования:
    - TODO: каждый год нумерация начинается сначала,
    - номера в пределах года уникальные,
    - следующий номер получаем на основе последнего, прибавляя единицу к числу в конце"""
    renderer_classes = [JSONRenderer]

    @staticmethod
    def strplus(s):
        """Номер состоит из перфикса и числа. Разбираем строку на перфикс и число, увеличеваем
        число (счетчик) и собираем обратно"""
        num = ''
        prefix = ''
        for i in range(len(s) - 1, -1, -1):  # перебор символов с конца
            if s[i].isdigit():  # в конце должно быть число, числа слева от других знаков
                num = s[i] + num  # итерпретируются как строка (префикс)
            else:  # с первого не числа идет префикс
                prefix = s[i] + prefix
        num = num if len(num) > 0 else "0000"  # если чила нет, то появится "0001"
        ll = len(num)
        num = str(int(num) + 1)  # тут теряем нули в начале числа 001->1
        for i in range(ll - len(num)):  # тут их восстанавливаем 1->001
            num = "0" + num
        return prefix + num

    def get(self, request):
        # TODO: если в этом году нет документов, то номер сразу равен пустой ("") строке, иначе:
        # TODO: добавить в строке ниже в выборку фильтр: в переделах текущего года.
        max_num = (Document.objects.filter(root=self.request.user.appuser.root_organization)
                   .filter(date__year=datetime.now().year).aggregate(Max('number')))
        if max_num['number__max']:
            numb = self.strplus(max_num['number__max'])
        else:
            numb = self.strplus('0000')
        return Response({"number": numb})  # sample response: {"number":"Т012"}


class CurrencyCBR(APIView):
    """Конвертер валют, учебное задание https://db89.ru/api/v1/currency?to=RUB&from=USD&value=1"""
    renderer_classes = [JSONRenderer]

    # Считаем через курс к рублю, т.к. https://www.cbr-xml-daily.ru/ не поддерживает смену базовой валюты
    def get(self, request):
        data = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()
        data['rates']['RUB'] = 1  # в data все курсы к базовой валюте RUB, нет там записи RUB, добавляем
        param_from = request.query_params['from']  # считываем параметр
        data_from = data['rates'][param_from]  # сохраняем его значение
        param_to = request.query_params['to']
        data_to = data['rates'][param_to]
        param_value = request.query_params['value']
        result = (float(data_to) / 1) / (float(data_from) / 1) * float(param_value)  # расчет через курс к рублю
        return Response({'result': round(result, 2), 'resource': "https://www.cbr-xml-daily.ru/latest.js"})


# </API>


# Generic views
class DocumentListView(LoginRequiredMixin, QueryRootMixin, ListView):
    login_url = reverse_lazy('login')
    model = Document


class DocumentView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Document


class DocumentPDFView(LoginRequiredMixin, PdfMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Document


class DocumentCreate(LoginRequiredMixin, CreateRootMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Document
    form_class = DocumentForm
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.root = self.request.user.appuser.root_organization
    #     self.object.save()
    #     return HttpResponseRedirect(self.object.get_absolute_url())


class DocumentDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Document
    success_url = reverse_lazy("document-list")


class DocumentUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Document
    form_class = DocumentForm


class AppUserListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = AppUser

    def get_queryset(self):
        queryset = self.request.user.appuser.root_organization.users.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class AppUserView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = AppUser


class AppUserCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = User
    form_class = UserRegistrationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password2'])
        self.object.username = self.object.email
        self.object.save()
        root = self.request.user.appuser.root_organization
        new_appuser = AppUser.objects.create(user=self.object, root_organization=root)
        new_appuser.save()
        """Добавить appuser объект в список appuser'ов текущего root"""
        root.users.add(new_appuser)
        root.save()
        return HttpResponseRedirect(new_appuser.get_absolute_url())


class AppUserUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("appuser-list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password2'])
        self.object.username = self.object.email
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserDelete(LoginRequiredMixin, DeleteView):
    """ Удаление пользлвателя встроенной системы auth, каскадом удалится наш AppUser """
    login_url = reverse_lazy('login')
    model = User
    success_url = reverse_lazy("appuser-list")


class RootOrganzationListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = RootOrganization

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        queryset = self.model.objects.filter(users=self.request.user.appuser)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class RootOrganizationView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = RootOrganization

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.user.appuser.root_organization = self.object
        self.request.user.appuser.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class RootOrganizationCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Organization
    form_class = RootOrganizationCreateForm

    def form_valid(self, form):
        self.object = form.save()
        root = RootOrganization.objects.create(profile=self.object)
        root.users.add(self.request.user.appuser)
        root.save()
        return HttpResponseRedirect(root.get_absolute_url())


class OrganzationListView(LoginRequiredMixin, QueryRootMixin, ListView):
    login_url = reverse_lazy('login')
    model = Organization


class OrganizationView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Organization


class OrganizationCreate(LoginRequiredMixin, CreateRootMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Organization
    form_class = OrganizationForm


class OrganizationUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Organization
    form_class = OrganizationForm


class OrganizationDelete(LoginRequiredMixin, DeleteView):
    """ Удаление организации """
    login_url = reverse_lazy('login')
    model = Organization
    success_url = reverse_lazy("organization-list")


class ItemCreate(LoginRequiredMixin, CreateRootMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Item
    form_class = ItemForm


class ItemUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Item
    form_class = ItemForm


class ItemDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Item
    success_url = reverse_lazy('item-list')


class ItemView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Item


class ItemListView(LoginRequiredMixin, QueryRootMixin, ListView):
    login_url = reverse_lazy('login')
    model = Item
