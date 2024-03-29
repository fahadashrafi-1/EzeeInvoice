from itertools import count
from typing import Text
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotFound, FileResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import templatize
from django.views.generic import ListView
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
from wkhtmltopdf.views import PDFTemplateView 
from datetime import datetime
import qrcode
from django.db.models import Sum
import base64
from io import BytesIO


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
    paginate_by = 12
    model = invoice
  

class InvoiceSerchView(ListView):
    model = invoice
    template_name = 'invoice_serch.html'

    def get_queryset(self, q):
        query = self.request.GET.get(q)
        context = invoice.objects.filter(terms__icontains = query)
        return context

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

def NewCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cust-list')            
    else:
        form =  CustomerForm()
    return render(request, 'purchase/customer_create.html', {'form': form})

class invoDetail(DetailView):
    model = invoice
    template_name = 'purchase/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        query = InvoiceDescription.objects.filter(invoice_id=self.kwargs['pk'])
        context['invoice_items'] = query
        context['total_amount'] = query.aggregate(Sum('total_price'))
        context['total_vat'] = query.aggregate(Sum('total_vat'))
        context['total_price'] = query.aggregate(Sum('total_line_value'))
        data = [context['total_amount'], context['total_vat'], context['total_price']]
        context['qrdata'] = qrcode.make(data)
        file = context['qrdata']
        file.save("purchase/static/qr.png")
        return context

class PDFTempView(PDFTemplateView):
    model = invoice
    template_name = 'purchase/invoice_detail_pdf.html'
    filename = 'Invoice_'+str(datetime.now())+'.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        master = get_object_or_404(invoice, id=self.kwargs['pk'])
        context['invoice'] = master
        query = InvoiceDescription.objects.filter(invoice_id=self.kwargs['pk'])
        context['invoice_items'] = query
        context['total_amount'] = query.aggregate(Sum('total_price'))
        context['total_vat'] = query.aggregate(Sum('total_vat'))
        context['total_price'] = query.aggregate(Sum('total_line_value'))
        data = [context['total_amount'], context['total_vat'], context['total_price']]
        context['qrdata'] = qrcode.make(data)
        # context['qrdata'] = context['qrdata']
        file = context['qrdata']
        file.save("qr.jpeg")
        buffered = BytesIO()
        file.save(buffered, format="PNG")
        context['qrdata'] = base64.b64encode(buffered.getvalue())
        context['qrdata'] = context['qrdata'].decode()
              
        
       
        return context

class NewInvo(CreateView):
    model = invoice
    fields = ['department', 'cusotmer_name', 'terms' , 'comments']
    template_name = 'purchase/invoice_form.html'
    success_url = '/Invoices/'
    form_name = NewInvoice()

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
            return redirect('invo-list')
        else:
            return HttpResponse('Form Not Saved Saved')

class InvoiceUpdate(UpdateView):
    model = invoice
    fields = ['cusotmer_name', 'department', 'terms', 'comments']
    success_url = '/Invoices/'
    template_name = 'purchase/invocie_update.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['InvoiceDescr'] = InvoiceDescr(self.request.POST, instance=self.object)
            context['InvoiceDescr'].full_clean()
        else:
            context['InvoiceDescr'] =InvoiceDescr(instance=self.object)
        
        return context
 
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formsat = context['InvoiceDescr']

        if formsat.is_valid():
            response = super().form_valid(form)
            formsat.instance = self.object
            formsat.save()
            return response
        else:
            return super().form_invalid(formsat)

def NewItem(request):
    if request.method == "POST":
        form = ItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items-list')            
    else:
        form = ItemsForm()

    return render(request, 'purchase/item_create.html', {'form': form})

class ItemView(ListView):
    model = items
    template_name = 'purchase/item_list.html'

class ItemDelete(DeleteView):
    model = items
    fields = '__all__'
    template_name = 'purchase/item_delete.html'
    success_url = reverse_lazy('items-list')

class ItemEdit(UpdateView):
    model = items
    fields = '__all__'
    template_name = 'purchase/name.html'
    success_url = reverse_lazy('items-list')

class customerList(ListView):
    model = customers
    template_name = 'purchase/customer_list.html'

class customerDetails(DetailView):
    model = customers
    fields = '__all__'
    success_url = '/custList/'

class customerUpdate(UpdateView):
    model = customers
    fields = '__all__'
    success_url = '/custList/'

class customerDelete(DeleteView):
    model = customers
    success_url = reverse_lazy('cust-list')
    
def pdfview1(request, pk):

    context = invoice.objects.get(id=pk)
    # context['company'] = invoice.cusotmer_name
    x = ['ezee invoice']
    qr = QRCodeImage([x], size=40 * mm)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    cent = p._pagesize[0] / 2
    
    p.drawCentredString(cent, 800, "ezee invoice")
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
    vat_wise = df.groupby(df.invoice_Date.dt.month)[['total_Vat']].sum()
    x = x.reset_index()

    
    plot_div = plot([Scatter(x=x['invoice_Date'], y=x['total_Ammount'],
                        mode='lines',  name='test',
                        opacity=0.8, marker_color='Purple')],
                        output_type='div')

    plot_div2 = plot([Scatter(x=x['invoice_Date'], y=vat_wise['total_Vat'],
                        mode='lines',  name='test1',
                        opacity=0.9, marker_color='Green')],
                        output_type='div')

    return render(request, "purchase/charts_page.html", 
                    context={'plot_div': plot_div, 
                            'plot_div2': plot_div2,
                            })


