from django.shortcuts import render
from . models import *

def loja(request):
    produtos = Produto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'loja/loja.html', context)

def wishlist(request):
    valor_total = 0
    total_itens = 0

    if request.user.is_authenticated:
        cliente = request.user.cliente
        itens_lista = ListaDesejos.objects.filter(user=request.user)
        valor_total, total_itens = ListaDesejos.get_list_total(request.user)
    else:
        itens_lista = []

    context = {'itens_lista': itens_lista, 
               'valor_total': valor_total,
               'total_itens': total_itens,}

    return render(request, 'loja/wishlist.html', context)
