from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('lista-desejos', views.wishlist, name='wishlist'),
]