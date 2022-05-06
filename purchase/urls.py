
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('name/', views.get_name),
    path('dilie/', views.viewpdf),
    path('getname/', views.get_name),
    path('NewItem/', views.NewItem),
    path('NewCustomer/', views.NewCustomer),
    path('NewInvoice/', views.NewInvo),
    path('items/', views.ItemView.as_view()),    
    path('Invoices/', itemInvocieDesicription.as_view()),
    path('custList/', views.customerList.as_view()),
    path('', views.index, name='index'),

]
