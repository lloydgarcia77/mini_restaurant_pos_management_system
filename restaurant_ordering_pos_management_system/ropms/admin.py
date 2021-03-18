from django.contrib import admin
from ropms import models
from import_export.admin import ImportExportModelAdmin 
from django.db.models import Q, Avg, Count, Sum, F, FloatField
# Register your models here.

admin.site.site_url = "/admin/pos/dashboard"

class CustomerTableAdmin(ImportExportModelAdmin):
    list_display = ('id','name', 'description', 'capacity', 'status', 'date_added')
    list_editable = ('name', 'description', 'capacity', 'status',)
    list_filter = ( 'capacity', 'status',)
    search_fields = ('id','name', 'description', 'capacity', 'status', 'date_added') 
    list_per_page = 10

admin.site.register(models.CustomerTable, CustomerTableAdmin)


class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('id','f_name', 'm_name', 'l_name', 'age', 'gender','email', 'is_valid','date_added')
    list_editable = ('f_name', 'm_name', 'l_name', 'age', 'email', 'gender','is_valid',)
    list_filter = ( 'gender','is_valid',)
    search_fields = ('id','name', 'description', 'capacity', 'status','email','is_valid', 'date_added') 
    list_per_page = 10

admin.site.register(models.Customer, CustomerAdmin)

class MenuAdmin(ImportExportModelAdmin):
    list_display = ('id','image', 'name', 'description', 'status', 'category','price', 'date_added')
    list_editable = ('image', 'name', 'description', 'status', 'category','price',)
    list_filter = ( 'category', 'status')
    search_fields = ('id','name', 'description', 'capacity', 'status','email', 'date_added') 
    list_per_page = 10

admin.site.register(models.Menu, MenuAdmin)

class WaitingAdmin(ImportExportModelAdmin):
    list_display = ('id','customer' ,'table','date_added')
    list_editable = ('customer' ,'table',) 
    search_fields = ('id','customer' ,'table','date_added') 
    list_per_page = 10

admin.site.register(models.Waiting, WaitingAdmin)

class CartAdmin(ImportExportModelAdmin):
    list_display = ('id','customer' ,'menu_item','quantity','date_added')
    list_editable = ('customer' ,'menu_item','quantity',) 
    search_fields = ('id','customer' ,'menu_item','quantity','date_added')
    list_filter = ( 'customer', 'menu_item') 
    list_per_page = 10

admin.site.register(models.Cart, CartAdmin)

class POSAdmin(ImportExportModelAdmin):
    list_display = ('id','customer_name' ,'table_name', 'menu_name', 'quantity','price','total','date_added') 
    search_fields = ('id','customer_name' ,'table_name', 'menu_name', 'quantity','price','total','date_added') 
    list_per_page = 10 


admin.site.register(models.POS, POSAdmin)