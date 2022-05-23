from sre_constants import SUCCESS
from django.forms import ModelForm, fields
from django.forms import formset_factory, inlineformset_factory
from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper() 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save_item', 'Save Item'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))

        self.helper.layout = Layout(
            Row(
                Column('item_number'),
                Column('item_name'),
                Column('item_detail')
            )
        )

class CustomerForm(ModelForm):
    class Meta:
        model = customers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper() 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save_customer', 'Save Customer'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))

        self.helper.layout = Layout(
            'cusotmer_name',
            Row(
                Column('mobile_no'),
                Column('land_Line'),
            ),
            'address',
            Row(
                Column('supplier_Terms'),
                Column('supplier_Contac_Name'),
            )                 
            ,            
        )

class InvoiceDescr(ModelForm):
    class Meta:
        model = invoice_description
        extra = 3
        fields = '__all__'
        success_url = '/'

InvoiceDescr = inlineformset_factory(invoice, invoice_description,
                                        form=InvoiceDescr, extra=3)

class NewInvoice(ModelForm):
    class Meta:
        model = invoice
        fields = '__all__'
        success_url = '/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper() 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save_customer', 'Save Customer'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))

        self.helper.layout = Layout(
            'cusotmer_name',
            Row(
                Column('department'),
                Column('vat'),
            ),
            'address',
            Row(
                Column('terms'),
                Column('comments'),
            )          
            ,            
        )
