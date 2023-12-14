from django.shortcuts import get_object_or_404, render, redirect
from . models import *

def loja(request):
    produtos = Produto.objects.all()

    total_quantidade = 0

    if request.user.is_authenticated:
        total_quantidade = ListaDesejos.get_total_qtd(request.user)

    context = {'produtos': produtos,
               'total_quantidade': total_quantidade,}
    return render(request, 'loja/loja.html', context)

def wishlist(request):
    valor_total = 0
    total_itens = 0
    total_quantidade = 0
    
    if request.user.is_authenticated:
        cliente = request.user.cliente
        itens_lista = ListaDesejos.objects.filter(user=request.user)
        valor_total, total_itens = ListaDesejos.get_list_total(request.user)
        total_quantidade = ListaDesejos.get_total_qtd(request.user)
    else:
        itens_lista = []

    context = {'itens_lista': itens_lista, 
               'valor_total': valor_total,
               'total_itens': total_itens,
               'total_quantidade': total_quantidade,}

    return render(request, 'loja/wishlist.html', context)

def adicionar_a_lista_de_desejos(request, produto_id):
    if request.user.is_authenticated:
        produto = get_object_or_404(Produto, id=produto_id)
        item_lista, created = ListaDesejos.objects.get_or_create(user=request.user, produto=produto)
        
        if created:
            item_lista.quantidade = 1
            item_lista.save()
        else:
            item_lista.quantidade += 1
            item_lista.save()

        return redirect('wishlist')

def remover_da_lista_de_desejos(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(ListaDesejos, id=item_id, user=request.user)
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            item.delete()
        return redirect('wishlist')
