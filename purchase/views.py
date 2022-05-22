import re
from typing import Text
from dagster import success_hook
from django import http
from django.http import response
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, FileResponse, HttpResponseRedirect
from django.utils.translation import templatize
from django.views.generic import ListView
from pendulum import datetime
from requests import request
from .models import *
import pandas as pd
from django.template.response import TemplateResponse
from reportlab.pdfgen import canvas
import io
from reportlab_qrcode import QRCodeImage
from reportlab.lib.units import mm
from reportlab.platypus.tables import Table
from .forms import InvoiceDescr, NameForm, ItemsForm, CustomerForm, NewInvoice
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
import datetime as dt




def pdfview(request):
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
    context = {
    'tot_custo' : customers.objects.all().count(),
    'tot_items' : items.objects.all().count(),
    'tot_invoi' : invoice.objects.all().count(),
    }
    return TemplateResponse(request, 'purchase/index.html', {'entries': context})

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
            form.save()
            return HttpResponseRedirect('/items/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ItemsForm()
    return render(request, 'purchase/name.html', {'form': form})

def NewCustomer(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/custList/')

    else:
        form = CustomerForm()

    return render(request, 'purchase/name.html', {'form': form})

class invoDetail(DetailView):
    model = invoice
    template_name = 'purchase/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_items'] = invoice_description.objects.filter(invoice_id=self.kwargs['pk'])
        data = ['EzeInovice', '123459878', 100, 15, dt.datetime.now()]
        context['qrdata'] = QRCodeImage([data], size=40 * mm)

        return context
        

        
 
class NewInvo(CreateView):
    model = invoice
    fields = '__all__'
    success_url = '/'
        
    def get_context_data(self, **kwargs):
        context = super(NewInvo, self).get_context_data(**kwargs)
        if self.request.POST:
            context['InvoiceDescr'] = InvoiceDescr(self.request.POST)
        else:
            context['InvoiceDescr'] = InvoiceDescr()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['InvoiceDescr']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return HttpResponse('Form Saved')
        else:
            return super().form_invalid(formset)
            # return HttpResponse('Form Not Saved Saved')

class InvoiceUpdate(UpdateView):
    model = invoice
    fields = '__all__'
    success_url = '/'
    template_name = 'purchase/invocie_update.html'
        
    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdate, self).get_context_data(**kwargs)
        context['invoice_items'] = invoice_description.objects.filter(invoice_id=self.kwargs['pk'])
        if self.request.POST:
            context['invoice_items'] = InvoiceDescr(self.request.POST)
        else:
            context['invoice_items'] = InvoiceDescr()
        return context
            

class ItemView(ListView):
    model = items
    template_name = 'purchase/item_list.html'

class ItemDelete(DeleteView):
    model = items
    fields = '__all__'
    template_name = 'purchase/item_delete.html'
    success_url = '/items/'

class ItemEdit(UpdateView):
    model = items
    fields = '__all__'
    template_name = 'purchase/name.html'
    success_url = '/items/'

class customerList(ListView):
    model = customers
    template_name = 'purchase/customer_list.html'

class customerDetails(DetailView):
    model = customers
    fields: '__all__'
    success_url = '/custList/'

    # template_name = 'purchase/customer_list.html'

class customerUpdate(UpdateView):
    model = customers
    fields = '__all__'
    success_url = '/custList/'
    # template_name = 'purchase/customer_list.html'

class customerDelete(DeleteView):
    model = customers
    
    # template_name = 'purchase/customer_list.html'

def pdfview1(request, pk):

    context = invoice.objects.get(id=pk)
    x = ["Ezee Invocie", 123456789, 50, 30, 290]
    qr = QRCodeImage([x], size=40 * mm)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    cent = p._pagesize[0] / 2
    
    p.drawCentredString(cent, 800, "Ezee Invoices")
    p.drawCentredString(cent, 750, "Vat No : 123456789")
    
    p.drawString(10, 700, "Customer Name : The First Customer")
    p.drawString(10, 680, "Invoice No : 13")
    p.drawString(470, 700, "Date : 25-June-2022")
    p.drawString(470, 680, "Due On: 25-June-2022")

    p.drawCentredString(cent, 650, "Items")

    data = ['1','2','3','4','5']
    width = 400
    height = 100
    f = Table(data)
    f.wrapOn(p, width, height)
    f.drawOn(p, 10, 550)

 

    
    # destList = []
    # for i in context:
    #     destList.append(i)

    # x2 = [tot_custo , tot_invoices, tot_items, context]

    # qr2 = QRCodeImage([x2], size=40 * mm)
    # qr3 = QRCodeImage([destList], size=40 * mm)

    qr.drawOn(p, 300, 10)
    # qr2.drawOn(p, 100, 10)
    # qr3.drawOn(p, 400, 10)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Ezee-Invoice.pdf')

from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go


def chart(request):
    context = invoice.objects.values()
    df = pd.DataFrame(context)
    df['invoice_Date'] = pd.to_datetime(df['invoice_Date'])
    x = df.groupby(df.invoice_Date.dt.month)[['total_Ammount']].sum()
    x = x.reset_index()

    
    plot_div = plot([Scatter(x=x['invoice_Date'], y=x['total_Ammount'],
                        mode='lines',  name='test',
                        opacity=0.8, marker_color='Purple')],
               output_type='div')

    return render(request, "purchase/charts_page.html", context={'plot_div': plot_div})


