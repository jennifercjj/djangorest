import json
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Direccion, Orden, Producto,ordenIten,Pago
from .utlis import get_or_set_or_session
from .forms import  AddToCartForm,AdressForm
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse




class ProductoListView(generic.ListView):
    template_name='cart/product_list.html'
    queryset=Producto.objects.all()

class ProductoDetailView(generic.FormView):

    template_name='cart/product_detail.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Producto, slug=self.kwargs["slug"])
    
    def get_success_url(self):
        return reverse("cart:summary") 

    def get_form_kwargs(self):
        kwargs= super(ProductoDetailView,self).get_form_kwargs()
        kwargs["producto_id"]=self.get_object().id
        return kwargs


    def form_valid(self, form ):
        order= get_or_set_or_session(self.request)
        producto=self.get_object()
        
        iten_filter= order.items.filter(
            producto=producto,
            bebida=form.cleaned_data['bebida']
        )

        if iten_filter.exists():
            item= iten_filter.first()
            item.cantidad += int(form.cleaned_data['cantidad'])
            item.save()
        else:
            new_item = form.save(commit=False)
            new_item.producto = producto
            new_item.order = order
            new_item.save()
        return super(ProductoDetailView, self).form_valid(form)


    def get_context_data(self,**kwargs):
        context = super(ProductoDetailView, self).get_context_data(**kwargs)
        context['producto'] = self.get_object()
        return context

class CartView(generic.TemplateView):
    template_name='cart/cart.html'
    def get_context_data(self, *args, **kwargs):
        context= super(CartView,self).get_context_data(**kwargs)
        context["orden"]=get_or_set_or_session(self.request)
        return context

class AumentarcantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item=get_object_or_404(ordenIten,id=kwargs['pk'])
        order_item.cantidad += 1
        order_item.save()
        return redirect("cart:summary")    

class DisminuirCantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item=get_object_or_404(ordenIten,id=kwargs['pk'])
        if order_item.cantidad<=1:
            order_item.delete()
        else:
            order_item.cantidad -= 1        
            order_item.save()
        return redirect("cart:summary")    

class EliminarCantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item=get_object_or_404(ordenIten,id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:summary")       

class PagarView(generic.FormView):

    template_name= 'cart/pagar.html'
    form_class =AdressForm

    def get_success_url(self):
        return reverse("cart:payment")

    def form_valid(self, form):
        orden=get_or_set_or_session(self.request)
        selecionar_direccion_de_envio=form.cleaned_data.get('selecionar_direccion_de_envio')
        selecionar_direccion_de_facturacion=form.cleaned_data.get('selecionar_direccion_de_facturacion')

        
        if selecionar_direccion_de_facturacion:
            orden.facturacion_direccion=selecionar_direccion_de_facturacion
        else:
            direccion=Direccion.objects.create(
                addres_type='B',
                user=self.request.user,
                direccion_line_1=form.cleaned_data['direccion_de_facturacion_1'],
                direccion_line_2=form.cleaned_data['direccion_de_facturacion_2'],
                cuidad=form.cleaned_data['cuidad_de_facturacion'],
            )
            orden.facturacion_direccion = direccion

        if selecionar_direccion_de_envio :
            orden.envio_direccion=selecionar_direccion_de_envio
        else:
            direccion=Direccion.objects.create(
                addres_type='S',
                user=self.request.user,
                direccion_line_1=form.cleaned_data['direccion_de_envio_1'],
                direccion_line_2=form.cleaned_data['direccion_de_envio_2'],
                cuidad=form.cleaned_data['cuidad_de_envio'],
            )
            orden.envio_direccion = direccion
    
        orden.save()



        messages.info(self.request,"Has agregado correctamente tus direcciones")
        return super(PagarView,self).form_valid(form)

    def get_form_kwargs(self,*args,**kwargs):
        kwargs=super(PagarView,self).get_form_kwargs()
        kwargs["user_id"]=self .request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context= super(PagarView,self).get_context_data(**kwargs)
        context["orden"]=get_or_set_or_session(self.request)
        return context
    
class Payment(generic.TemplateView):
    template_name='cart/payment.html'
    def get_context_data(self, **kwargs):
        context= super(Payment,self).get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"]=settings.PAYPAL_CLIENT_ID
        context['orden']=get_or_set_or_session(self.request)
        context['CALLBACK_URL']=reverse('cart:cofirm-orden')
        return context

class ConfirmOrdenView(generic.View):
    def post(self, request,*args, **kwargs):
        orden=get_or_set_or_session(request)
        body= json.loads(request.body)
        pago=Pago.objects.create(
            orden=orden,
            sucecesful=True,
            raw_repuesta=json.dump(body),
            total=float(body["purchase_units"][0]["amount"]["value"]),
            metodo_pago = 'Paypal'
        )
        pago.save()
        orden.ordenn=True
        orden.orden_fecha=datetime.date.today()
        orden.save()
        return reverse('cart:gracias'),JsonResponse({"data":"Success"})
        

    



class GraciasView(generic.TemplateView):
    template_name='cart/gracias.html'

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'order.html'
    queryset = Orden.objects.all()
    context_object_name = 'order'