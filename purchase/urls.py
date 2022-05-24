
from fileinput import filename
from django.urls import path
from .views import *
from . import views
from django.urls import URLPattern
from wkhtmltopdf.views import PDFTemplateView



urlpatterns = [
    path('name/', views.get_name),
    path('getname/', views.get_name),
    path('NewItem/', views.NewItem),
    path('NewCustomer/', views.NewCustomer),
    path('<pk>/CustDetail/', views.customerDetails.as_view()),
    path('custList/', views.customerList.as_view()),
    path('custList/<pk>/CustUpdat/', views.customerUpdate.as_view()),
    path('custList/<pk>/CustDelete/', views.customerDelete.as_view()),
    path('NewInvoice/', views.NewInvo.as_view()),
    path('InvocieHeader/', views.InvocieHeader),
    path('Invoices/', itemInvocieDesicription.as_view()),
    path('<pk>/InvoDetails/', invoDetail.as_view()),
    path('<pk>/InvoDetailsPdf/', PDFTemplateView.as_view(template_name='purchase/invoice_detail.html',filename='my_template.pdf'), name='pdf'),
    path('<pk>/InvoUpdate/', views.InvoiceUpdate.as_view()),
    path('items/', views.ItemView.as_view()),    
    path('<pk>/itemEdit/', views.ItemEdit.as_view()),
    path('<pk>/ItemDele/', views.ItemDelete.as_view()),
    path('pdf/', views.pdfview),
    path('<pk>/pdf1/', views.pdfview1),
    path('charts/', views.chart),

    path('', views.index, name='index'),

]
