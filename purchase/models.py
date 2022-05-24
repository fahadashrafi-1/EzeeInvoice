from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.json import CaseInsensitiveMixin

# Create your models here.

class items(models.Model):
    item_number = models.CharField(verbose_name='Reference No' , max_length=30, blank=True ,help_text='item-001')
    item_name = models.CharField( verbose_name='Items' , max_length=60, help_text='Paper Cups grey')
    item_detail = models.CharField(verbose_name='Item Details' , max_length=120, blank=True, help_text='Paper Cups grey')
    item_date_created = models.DateField('Creation Date', auto_now_add=True, help_text='Date when item was created')

    def __str__(self):
        """String for representing the Model object."""
        return self.item_name

class invoice(models.Model):
    invoice_Date = models.DateField(auto_now=True)
    department = models.CharField(max_length=80 , help_text='Finance')
    cusotmer_name =models.ForeignKey('customers', on_delete=models.CASCADE)
    total_Ammount = models.FloatField('Total', default=0)
    total_Vat = models.FloatField('Vat Ammount', default=0)
    terms = models.CharField('Terms of Payment',max_length=300, blank=True)
    comments = models.CharField('Comments',max_length=300, blank=True)
    
    # item_description = models.ForeignKey('item_description', on_delete=models.CASCADE)
       
    def __str__(self):
        """String for representing the Model object."""
        return str(self.cusotmer_name)

class invoice_description(models.Model):
    invoice = models.ForeignKey(invoice, on_delete=models.CASCADE)
    items = models.ForeignKey(items, on_delete=models.CASCADE)
    item_price = models.IntegerField(default=0, help_text='200')
    quantity = models.IntegerField('Quantity',default=0, blank=False)
    total_price = models.IntegerField('Total Ammount',default=0, help_text='item_price * item quantity')
    total_vat = models.IntegerField('Vat',default=0, help_text='200')
        
    def __str__(self):
        """String for representing the Model object."""
        return str(self.items)
    
    @property
    def get_total(self):
        return self.item_price * self.quantity
    
    @property
    def get_vat(self):
        return self.get_total * 0.15

    @property
    def invoice_total(self):
        return self.get_total + self.get_vat
     
    
    def save(self, *args, **kwargs):
        self.total_price = self.get_total
        self.total_vat = self.get_vat
        invoice.total_Ammount = self.invoice_total
        super(invoice_description, self).save()
        
   
class customers(models.Model):
    cusotmer_name = models.CharField(max_length=120, help_text='Fortune Makers')
    address = models.CharField(max_length=120, help_text='106 Ar Riyadh Aveneu')
    supplier_Terms = models.CharField(max_length=200)
    supplier_Contact_Name = models.CharField(max_length=200)
    mobile_no = models.IntegerField(help_text="0505050505", default=123)
    land_Line = models.IntegerField(help_text="096611-2335464", default=123)


    def __str__(self):
        """String for representing the Model object."""
        return self.cusotmer_name