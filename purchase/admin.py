from django.contrib import admin
from .models import customers, items, invoice , invoice_description
from django.db.models import F, Sum


admin.site.site_header = 'Eee-Zee Invoice'


# class InLineInvoices(admin.StackedInline):
#     model = invoice

# # class InLineItems(admin.StackedInline):
# #     model = items

# # class InLineCustomers(admin.StackedInline):
# #     model = customers

class invoicedescriptionInline(admin.TabularInline):
    model = invoice_description
    exclude = (['total_price', 'total_vat', 'vat'])
    extra = 3


class invoiceadmin(admin.ModelAdmin):
    exclude = ['total_Ammount', 'vat' , 'total_Vat', 'department']
    list_display = (['invoice_Date', 'cusotmer_name', 'total_Vat', 'total_Ammount'])
    inlines = [invoicedescriptionInline,]


class CustomInvoices(admin.ModelAdmin):
    list_display = ('department', 'cusotmer_Name', 'invoice_Date', 'get_total')
    list_filter = ('department', 'invoice_Date')
    list_display_links = ('department','cusotmer_Name')
    # list_editable = ('item_price',)
    list_max_show_all = (10)
    search_fields = ( 'department',)

    # def get_PrHead(self, obj):
    #     return obj.purchase_head.department

    # # get_PrHead.short_description = 'PR Company'

    # def get_supplier(self, obj):
    #     return obj.purchase_head.cusotmer_name
    
    

    # def get_total(self, obj):
    #     return obj.item_price * obj.quantity
    
    # def get_vat(self, obj):
    #     return (obj.item_price * obj.quantity)  *  15 

    # def get_quantiy_items(self, obj):
    #     return obj.items.count()

class itemsDisplay(admin.ModelAdmin):
    list_display = (['item_name', 'item_detail', 'item_date_created'])

class customerDisplay(admin.ModelAdmin):
    list_display = (['cusotmer_name', 'address', 'mobile_no'])



admin.site.register(invoice, invoiceadmin),
admin.site.register(items, itemsDisplay),
admin.site.register(customers, customerDisplay),


