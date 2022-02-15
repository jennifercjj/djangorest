from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from cart.models import Orden
from .forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfilView(LoginRequiredMixin,generic.TemplateView):
    template_name='profile.html'
    def get_context_data(self, **kwargs):
        context = super(ProfilView, self).get_context_data(**kwargs)
        context.update({
            "orders": Orden.objects.filter(user=self.request.user, ordenn=True)
        })
        return context

#vista del view



class HomeView(generic.TemplateView):
    template_name='index.html'
# vista de contacto
class ContactView(generic.FormView):
    form_class=ContactForm
    template_name='contact.html'
    def get_success_url(self):
            return reverse("contact")

    def form_valid(self,form): 
        messages.info(
            self.request,"Hemos recivimos su mensaje le respoderemos lo más pronto posible")
        nombre =form.cleaned_data.get('nombre')
        correo =form.cleaned_data.get('correo') 
        mensaje =form.cleaned_data.get('mensaje')

        full_message=f"""
            Mensaje recibido de {nombre} , {correo}
            ______________________________________

            Mensaje:
            
            {mensaje}
            
            """
        send_mail(
            subject="Mensaje recibido de sistema de contacto de Sabor y Sázon Restaurante",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super(ContactView, self).form_valid(form)
