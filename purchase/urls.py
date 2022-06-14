from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('name/', views.get_name),
    path('getname/', views.get_name),
    path('NewItem/', views.NewItem),
    path('items/', views.ItemView.as_view(), name='items-list'),    
    path('<pk>/itemEdit/', views.ItemEdit.as_view()),
    path('<pk>/ItemDele/', views.ItemDelete.as_view()),    
    path('NewCustomer/', views.NewCustomer),
    path('<pk>/CustDetail/', views.customerDetails.as_view()),
    path('custList/', views.customerList.as_view(), name='cust-list'),
    path('custList/<pk>/CustUpdat/', views.customerUpdate.as_view()),
    path('custList/<pk>/CustDelete/', views.customerDelete.as_view()),
    path('NewInvoice/', views.NewInvo.as_view()),
    path('Invoices/', itemInvocieDesicription.as_view(), name='invo-list'),
    path('Search/', InvoiceSerchView.as_view()),
    path('<pk>/InvoDetails/', invoDetail.as_view()),
    path('<pk>/InvoDetailsPdf/', PDFTempView.as_view()),
    path('<pk>/InvoUpdate/', views.InvoiceUpdate.as_view()),
    path('pdf/', views.pdfview),
    path('<pk>/pdf1/', views.pdfview1),
    path('charts/', views.chart),
    path('', views.index, name='index'),

]
