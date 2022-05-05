from sre_constants import SUCCESS
from django.forms import ModelForm, fields
from django.forms import formset_factory
from django import forms
from .models import *

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_father_name = forms.CharField(label='your Father Name', max_length=100)
    your_mother_name = forms.CharField(label='your Mother Name', max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class ItemsForm(ModelForm):
    class Meta:
        model = items
        fields = ['item_number', 'item_name', 'item_detail']

class CustomerForm(ModelForm):
    class Meta:
        model = customers
        fields = '__all__'
        

class InvoiceDescr(forms.Form):
    model = invoice_description
    extra = 3

class NewInvoice(ModelForm):
    model = invoice
    # extra = 
