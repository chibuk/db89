from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('document/list/', views.DocumentListView.as_view(), name='document-list'),
    path('document/<int:pk>/', views.DocumentView.as_view(), name='document-detail'),
    path('document/add/', views.DocumentCreate .as_view(), name='document-add'),
    path('city/list/', views.CityListView.as_view(), name='city-list'),
    path('city/<int:pk>/', views.CityView.as_view(), name='city-detail'),
    path('city/add/', views.CityCreate.as_view(), name='city-add'),
    path('city/<int:pk>/update/', views.CityUpdate.as_view(), name='city-update'),
    path('city/<int:pk>/delete/', views.CityDelete.as_view(), name='city-delete'),
]