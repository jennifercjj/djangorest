#va toda la  de nuestros formularios 
from django import forms

class ContactForm(forms.Form):
    nombre= forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'placeholder': "Tu nombre"
    }))
    correo= forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Tu Correo electronico"
    }))
    mensaje= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Tu Mensaje"
    }))