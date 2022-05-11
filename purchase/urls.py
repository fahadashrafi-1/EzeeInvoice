
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('name/', views.get_name),
    path('getname/', views.get_name),
    path('NewItem/', views.NewItem),
    path('NewCustomer/', views.NewCustomer),
    path('NewInvoice/', views.NewInvo.as_view()),
    path('Invoices/', itemInvocieDesicription.as_view()),
    path('<pk>/InvoDetails/', invoDetail.as_view()),
    path('<pk>/InvoUpdate/', views.InvoiceUpdate.as_view()),
    path('items/', views.ItemView.as_view()),    
    path('<pk>/itemEdit/', views.ItemEdit.as_view()),
    path('<pk>/ItemDele/', views.ItemDelete.as_view()),
    path('custList/', views.customerList.as_view()),
    path('pdf/', views.pdfview),
    path('<pk>/pdf1/', views.pdfview1),

    path('', views.index, name='index'),

]
