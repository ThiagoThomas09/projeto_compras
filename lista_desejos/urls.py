from django.urls import path
from . import views

urlpatterns = [
    path('lista-desejos', views.wishlist, name='wishlist'),
    path('criar-lista/', views.criar_lista, name='criar_lista'),

    # Para inserir o produto ao criar a lista
    path('criar_lista/<int:produto_id>/', views.criar_lista, name='criar_lista_com_produto'),
    path('adicionar/<int:lista_id>/<int:produto_id>/', views.adicionar_a_lista_de_desejos, name='adicionar_a_lista'),

    path('remover/<int:item_id>/', views.remover_da_lista_de_desejos, name='remover_da_lista'),

    path('verificar_produto_lista/<int:produto_id>/', views.verificar_produto_lista, name='verificar_produto_lista'),
    path('deletar_lista/<int:lista_id>/', views.deletar_lista_desejos, name='deletar_lista')

]