from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from app.models import Document, AppUser, RootOrganization, Organization, Item, DocumentItem
from django.views.generic import ListView, DetailView
from app.forms import DocumentForm, OrganizationForm, UserRegistrationForm, RootOrganizationCreateForm, ItemForm
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
# Create your views here.
from django.http import HttpResponse
from app.serializers import OrganizationSerializer, DocumentSerializer, DocumentItemSerializer
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


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
class OrganizationAPIListView(ListAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        queryset = Organization.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset


class DocumentAPIListView(ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset


class DocumentItemAPIListView(ListAPIView):
    serializer_class = DocumentItemSerializer

    def get_queryset(self):
        queryset = DocumentItem.objects.filter(root=self.request.user.appuser.root_organization)
        return queryset
# </API>


# Generic views
class DocumentListView(LoginRequiredMixin, QueryRootMixin, ListView):
    login_url = reverse_lazy('login')
    model = Document


class DocumentView(LoginRequiredMixin, DetailView):
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
