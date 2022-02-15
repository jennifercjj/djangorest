
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.
User = get_user_model()
class Bebidavariacion(models.Model):
    nombre=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    ADDRESS_CHOICES=(
        ('B','Facturacion'),
        ('S','Envio'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion_line_1 = models.CharField(max_length=150)
    direccion_line_2 = models.CharField(max_length=150)
    cuidad = models.CharField(max_length=150)
    addres_type = models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    defecto=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.direccion_line_1},{self.direccion_line_2},{self.cuidad}"

    class Meta:
        verbose_name_plural='Direcciones'
    
class Producto(models.Model):
    title= models.CharField(max_length=150)
    slug=models.SlugField(unique=True)
    image= models.ImageField(upload_to='product_images')
    descripcion= models.TextField()
    precio=models.PositiveIntegerField(default=1)
    creado=models.DateField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activado= models.BooleanField(default=False)
    avalible_bebida=models.ManyToManyField(Bebidavariacion)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug':self.slug})
    #para mostar el precio
    def get_precio(self):
        return "{:.2f}".format(self.precio/100)
#clase inetermedio
class ordenIten(models.Model):
    order=models.ForeignKey("Orden",related_name='items',on_delete=models.CASCADE)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    bebida = models.ForeignKey(Bebidavariacion,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.cantidad} x {self.producto.title}"
    def get_precio_total(self):
        return self.cantidad*self.producto.precio
    def get_total(self):
        precio=self.get_precio_total()
        return "{:.2f}".format(precio/100)

class Orden(models.Model):
    user=models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    incio_fecha=models.DateTimeField(auto_now_add=True)
    orden_fecha=models.DateTimeField(blank=True, null=True)
    ordenn=models.BooleanField(default=False)
    ##itens
    facturacion_direccion= models.ForeignKey(
        Direccion, related_name='facturacion_direccion', blank=True, null=True,on_delete=models.SET_NULL)
    envio_direccion= models.ForeignKey(
        Direccion, related_name='envio_direccion', blank=True,null=True,on_delete=models.SET_NULL)    
    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"Orden-{self.pk}"
    
    def get_raw_subtotal(self):
        total=0
        for order_iten in self.items.all():
            total+=order_iten.get_precio_total()
        return  total
    def get_subtotal(self):
        subtotal=self.get_raw_subtotal()
        return "{:.2f}".format(subtotal/100)
    def get_raw_total(self):
        subtotal=self.get_raw_subtotal()
        #total=subtotal-descuentos+iva+delivery
        #return total
        return subtotal
    def get_total(self):
        total=self.get_raw_total()
        return "{:.2f}".format(total/100)


class Pago(models.Model):
    orden= models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='payments')
    metodo_pago = models.CharField(max_length=20, choices=(
        ('Paypal','Paypal'),
    ))
    tiempo= models.DateTimeField(auto_now_add=True)
    sucecesful=models.BooleanField(default=False)
    total=models.FloatField()
    raw_repuesta=models.TextField()

    def __str__(self):
      return self.reference_number  
    @property
    def reference_number(self):
        return f"PAGO-{self.orden}-{self.pk}"


def pre_save_product_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.title)


pre_save.connect(pre_save_product_receiver, sender=Producto)