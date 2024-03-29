from django.forms import ModelForm
from django.forms import inlineformset_factory
from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML
from django.urls import reverse_lazy
from .models import invoice, InvoiceDescription

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
        fields = ['item_name', 'item_detail']
        success_url = reverse_lazy('items-list')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper() 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save_item', 'Save Item'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))

        self.helper.layout = Layout(
            Row(
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
                Column('supplier_Contact_Name'),
            )                 
            ,            
        )

class InvoiceDescriPtion(ModelForm):
    class Meta:
        model = InvoiceDescription
        fields = ['items', 'quantity', 'item_price']
        extra = 3

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
            Row(
                Column('cusotmer_name'),
                Column('department'),
            ),
            Row(
                Column('terms'),
                Column('comments'),
            )          
            ,            
        )

InvoiceDescr = inlineformset_factory(invoice, InvoiceDescription,exclude=['total_price','total_vat', 'total_line_value'], can_delete=False)

class InvoDescrFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'items',
            'item_price',
            'quantity',
            'get_total',
        )
        self.render_required_fields = True


