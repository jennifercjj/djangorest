from django.urls import path
from . import views
app_name = 'cart'

urlpatterns=[
    path('',views.CartView.as_view(),name='summary'),
    path('Tienda/',views.ProductoListView.as_view(),name='product-list'),
    path('Tienda/<slug>/',views.ProductoDetailView.as_view(),name='product-detail'),
    path('incrementar-cantidad/<pk>/',views.AumentarcantidadView.as_view(),name='incrementar-cantidad'),
    path('disminuir-cantidad/<pk>/',views.DisminuirCantidadView.as_view(),name='disminuir-cantidad'),
    path('eliminar-cantidad/<pk>/',views.EliminarCantidadView.as_view(),name='eliminar-cantidad'),
    path('pagar/',views.PagarView.as_view(), name='pagar'),
    path('payment/',views.Payment.as_view(), name='payment'),
    path('gracias/',views.GraciasView.as_view(), name='gracias'),
    path('cofirm-orden/',views.ConfirmOrdenView.as_view(), name='cofirm-orden'),
    path('orders/<pk>',views.OrderDetailView.as_view(), name='order-detail'),
]