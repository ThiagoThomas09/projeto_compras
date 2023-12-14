from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('lista-desejos', views.wishlist, name='wishlist'),
    path('adicionar/<int:produto_id>/', views.adicionar_a_lista_de_desejos, name='adicionar_a_lista'),

    path('remover/<int:item_id>/', views.remover_da_lista_de_desejos, name='remover_da_lista'),

]