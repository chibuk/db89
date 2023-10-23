from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('document/list/', views.DocumentListView.as_view(), name='document-list'),
    path('document/<int:pk>/', views.DocumentView.as_view(), name='document-detail'),
    path('document/<int:pk>/pdf', views.DocumentPDFView.as_view(), name='document-detail.pdf'),
    path('document/add/', views.DocumentCreate.as_view(), name='document-add'),
    path('document/update/<int:pk>/', views.DocumentUpdate.as_view(), name='document-update'),
    path('document/delete/<int:pk>/', views.DocumentDelete.as_view(), name='document-delete'),
    path('appuser/list/', views.AppUserListView.as_view(), name='appuser-list'),
    path('appuser/<int:pk>/', views.AppUserView.as_view(), name='appuser-detail'),
    path('appuser/add/', views.AppUserCreate.as_view(), name='appuser-add'),
    path('appuser/update/<int:pk>', views.AppUserUpdate.as_view(), name='appuser-update'),
    path('appuser/delete/<int:pk>', views.UserDelete.as_view(), name='appuser-delete'),
    path('root/list/', views.RootOrganzationListView.as_view(), name='rootorganization-list'),
    path('root/<int:pk>/', views.RootOrganizationView.as_view(), name='rootorganization-detail'),
    path('root/add/', views.RootOrganizationCreate.as_view(), name='rootorganization-add'),
    path('organization/add/', views.OrganizationCreate.as_view(), name='organization-add'),
    path('organization/list/', views.OrganzationListView.as_view(), name='organization-list'),
    path('organization/<int:pk>/', views.OrganizationView.as_view(), name='organization-detail'),
    path('organization/update/<int:pk>/', views.OrganizationUpdate.as_view(), name='organization-update'),
    path('organization/delete/<int:pk>/', views.OrganizationDelete.as_view(), name='organization-delete'),
    path('item/add/', views.ItemCreate.as_view(), name='item-add'),
    path('item/list/', views.ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', views.ItemView.as_view(), name='item-detail'),
    path('item/update/<int:pk>/', views.ItemUpdate.as_view(), name='item-update'),
    path('item/delete/<int:pk>/', views.ItemDelete.as_view(), name='item-delete'),
    path('logout/', views.logoutView, name='logout'),
    path('api/v1/organizations/', views.OrganizationAPIModelView.as_view({'post': 'create',
                                                                          'get': "list"})),
    path('api/v1/organizations/<int:pk>/', views.OrganizationAPIModelView.as_view({'get': 'retrieve',
                                                                                   'put': 'partial_update',
                                                                                   'delete': 'destroy',
                                                                                   'patch': 'partial_update'})),
    path('api/v1/organizations/search/<str:keyword>', views.OrganizationAPIModelView.as_view({'get': 'search'})),
    path('api/v1/documents/', views.DocumentAPIModelView.as_view({'post': 'create',
                                                                  'get': 'list'})),
    path('api/v1/documents/<int:pk>/', views.DocumentAPIModelView.as_view({'get': 'retrieve',
                                                                           'put': 'partial_update',
                                                                           'delete': 'destroy',
                                                                           'patch': 'partial_update'})),
    path('api/v1/documents/last/', views.DocumentAPIModelView.as_view({'get': 'last'})),
    path('api/v1/documentitems/', views.DocumentitemAPIModelView.as_view({'post': 'create',
                                                                      'get': 'list'})),
    path('api/v1/documentitems/<int:pk>/', views.DocumentitemAPIModelView.as_view({'get': 'retrieve',
                                                                               'put': 'partial_update',
                                                                               'delete': 'destroy',
                                                                               'patch': 'partial_update'})),
    path('api/v1/documentitems/doclist', views.DocumentitemAPIModelView.as_view({'get': 'document_list'})),
    # path('api/v1/documentitems/', views.DocumentItemAPIListView.as_view()),
    path('api/v1/items/', views.ItemAPIModelView.as_view({'post': 'create',
                                                          'get': 'list'})),
    path('api/v1/items/<int:pk>/', views.ItemAPIModelView.as_view({'get': 'retrieve',
                                                                   'put': 'partial_update',
                                                                   'delete': 'destroy',
                                                                   'patch': 'partial_update'})),
    path('api/v1/items/search/<str:keyword>', views.ItemAPIModelView.as_view({'get': "search"})),
    path('api/v1/currency', views.CurrencyCBR.as_view()),
    path('api/v1/documentnumber/', views.DocumentNumber.as_view()),
]
