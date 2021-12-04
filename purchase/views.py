import re
from typing import Text
from django import http
from django.http import response
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, FileResponse, HttpResponseRedirect
from django.utils.translation import templatize
from django.views.generic import ListView
from .models import *
import pandas as pd
from django.template.response import TemplateResponse
from reportlab.pdfgen import canvas
import io
from reportlab_qrcode import QRCodeImage
from reportlab.lib.units import mm
from .forms import NameForm, ItemsForm, CustomerForm, NewInvoice
from django.views.generic import ListView



def viewpdf(request):


    x = ["Ezee Invocie", 123456789, 50, 30, 290]
    qr = QRCodeImage([x], size=40 * mm)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    cust = customers.objects.all()
    tot_custo = customers.objects.all().count()
    tot_invoices = invoice.objects.all().count()
    tot_items = items.objects.all().count()

    p.drawString(10, 500, "Total Customers "+ str(tot_custo) + "Total Invoices "+ str(tot_invoices) + "Total Items "+ str(tot_items))

    # for i in cust:
    #     print(i)
    #     p.drawString(i)
    
    p.drawString(10, 10, "Hello World")
    x2 = [tot_custo , tot_invoices, tot_items]

    qr2 = QRCodeImage([x2], size=40 * mm)
    qr.drawOn(p, 300, 10)
    qr2.drawOn(p, 100, 10)
    
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Ezee-Invoice.pdf')

def index(request):
    tot_custo = customers.objects.all().count()
    tot_invoices = invoice.objects.all().count()
    tot_items = items.objects.all().count()

    return TemplateResponse(request, 'purchase/index.html', {'entries': tot_custo})

def get_name(request):
    return HttpResponse("Fahad is a good developing developer")

class itemInvocieDesicription(ListView):
    model = invoice
   

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'purchase/name.html', {'form': form})


def NewItem(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ItemsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ItemsForm()

    return render(request, 'purchase/name.html', {'form': form})


def NewCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pur/')

    else:
        form = CustomerForm()

    return render(request, 'purchase/name.html', {'form': form})
    

def NewInvoice(request):
    if request.method == 'POST':
        form = NewInvoice(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = NewInvoice()

    return render(request, 'purchase/name.html', {'form': form})
    

class ItemView(ListView):
    model = items
    template_name = 'purchase/item_list.html'

class customerList(ListView):
    model = customers
    template_name = 'purchase/customer_list.html'



