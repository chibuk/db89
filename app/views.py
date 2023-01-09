from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from app.models import Document, City
from django.views.generic import ListView, DetailView
from app.forms import CityForm, DocumentForm

# Create your views here.
from django.http import HttpResponse


def index(request):
    documents = Document.objects.all()
    citys = City.objects.all()
    return render(request, 'app/index.html', {"documents": documents, "citys": citys})


# Generic views
class DocumentListView(ListView):
    model = Document


class DocumentView(DetailView):
    model = Document


class DocumentCreate(CreateView):
    model = Document
    form_class = DocumentForm


class CityListView(ListView):
    model = City


class CityView(DetailView):
    model = City


class CityCreate(CreateView):
    model = City
    form_class = CityForm


class CityUpdate(UpdateView):
    model = City
    form_class = CityForm


class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('city-list')


# def add_city(request):
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#             except:
#                 form.add_error(None, 'Ошибка добавления города')
#             return HttpResponseRedirect(reverse('add_city'))
#     else:
#         form = CityForm()
#     list = City.objects.all()
#     return render(request, 'app/add_city.html', {'form': form, 'list': list})
