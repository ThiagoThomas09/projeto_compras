from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('cart', views.cart, name='cart'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('checkout', views.checkout, name='checkout'),
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('adicionar_lista_ao_carrinho/<int:lista_id>/', views.adicionar_lista_ao_carrinho, name='adicionar_lista_ao_carrinho'),
]