from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Bebidavariacion, Producto,Orden,ordenIten,Bebidavariacion,Direccion,Pago 



class AddressAdmin(admin.ModelAdmin):
    list_display=[
        'direccion_line_1',
        'direccion_line_2',
        'cuidad',
        'addres_type',
    ]

admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(ordenIten)
admin.site.register(Bebidavariacion)
admin.site.register(Direccion,AddressAdmin)
admin.site.register(Pago)
# Register your models here.
