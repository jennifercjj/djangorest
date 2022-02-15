from cart import models
from rest_framework import serializers
class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Producto
        fields=('title','image','descripcion','precio','creado') # Especifique los campos devueltos
