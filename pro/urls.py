from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_requests/', views.my_requests, name='my_requests'),
    path('request/', views.request, name='request'),
    path('sign/', views.logins, name='logins'),
    path('requests/delete/<int:pk>/', views.delete_request, name='delete_request'),
    path('categories/', views.managecategories, name='managecategories'),
    path('categories/add/', views.add_category, name='addcategory'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('panale/', views.panale, name='panale'),
    path('requests/status/<int:pk>/', views.status, name='status'),
    path('requests/', views.managerequests, name='managerequests'),
]
