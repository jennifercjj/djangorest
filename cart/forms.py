from django import forms
from django.contrib.auth import get_user_model
from .models import Bebidavariacion, Direccion, ordenIten ,Producto

User = get_user_model()


class AddToCartForm(forms.ModelForm):
    bebida=forms.ModelChoiceField(queryset=Bebidavariacion.objects.none())
    class Meta:
        model=ordenIten
        fields=['cantidad','bebida']

    def __init__(self, *args, **kwargs):
        product_id=kwargs.pop('producto_id')   
        producto=Producto.objects.get(id=product_id)
        super().__init__(*args, **kwargs)
        self.fields['bebida'].queryset=producto.avalible_bebida.all()
class AdressForm(forms.Form):

    direccion_de_envio_1=forms.CharField(required=False)
    direccion_de_envio_2=forms.CharField(required=False)
    cuidad_de_envio=forms.CharField(required=False)

    direccion_de_facturacion_1=forms.CharField(required=False)
    direccion_de_facturacion_2=forms.CharField(required=False)
    cuidad_de_facturacion=forms.CharField(required=False)

    selecionar_direccion_de_envio=forms.ModelChoiceField(
        Direccion.objects.none(),required=False
    )
    selecionar_direccion_de_facturacion=forms.ModelChoiceField(
        Direccion.objects.none(),required=False
    )
    def __init__(self,*args,**kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)
        user = User.objects.get(id=user_id)

        direccion_de_envio_qs=Direccion.objects.filter(
            user=user,
            addres_type='S'
        )
        direccion_de_Fcacturacion_qs=Direccion.objects.filter(
            user=user,
            addres_type='B'
        )

        self.fields['selecionar_direccion_de_envio'].queryset= direccion_de_envio_qs
        self.fields['selecionar_direccion_de_facturacion'].queryset= direccion_de_Fcacturacion_qs
    def clean(self):
        data = self.cleaned_data
        selecionar_direccion_de_envio=data.get('selecionar_direccion_de_envio',None)
        if selecionar_direccion_de_envio is None:
            if not data.get('direccion_de_envio_1',None):
                self.add_error("direccion_de_envio_1","Por favor complete este campo")

            if not data.get('direccion_de_envio_2',None):
                self.add_error("direccion_de_envio_2","Por favor complete este campo")

            if not data.get('cuidad_de_envio',None):
                self.add_error("cuidad_de_envio","Por favor complete este campo")

        selecionar_direccion_de_facturacion=data.get('selecionar_direccion_de_facturacion',None)
        if selecionar_direccion_de_facturacion is None:
            if not data.get("direccion_de_facturacion_1",None):
                self.add_error("direccion_de_facturacion_1","Por favor complete este campo")

            if not data.get('direccion_de_facturacion_2',None):
                self.add_error("direccion_de_facturacion_2","Por favor complete este campo")
                
            if not data.get('cuidad_de_envio',None):
                self.add_error("cuidad_de_facturacion","Por favor complete este campo")    
 
