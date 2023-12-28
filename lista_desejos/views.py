from django.shortcuts import render, get_object_or_404, redirect
from . models import ListaDesejos, ItemListaDesejos
from loja.models import Produto

def wishlist(request):
    listas = []
    valor_total = 0
    total_quantidade = 0
    
    if request.user.is_authenticated:
        listas = ListaDesejos.objects.filter(user=request.user)
        valor_total = sum(lista.get_list_total() for lista in listas)
        total_quantidade = sum(lista.get_total_qtd() for lista in listas)

    context = {'listas': listas, 
               'valor_total': valor_total,
               'total_quantidade': total_quantidade,}

    return render(request, 'loja/wishlist.html', context)

def adicionar_a_lista_de_desejos(request, produto_id):
    if request.user.is_authenticated:
        produto = get_object_or_404(Produto, id=produto_id)

        lista = ListaDesejos.objects.filter(user=request.user).first()
        if not lista:
            lista = ListaDesejos.objects.create(user=request.user, nome = 'Minha lista de desejos')
        
        item_lista, created = ItemListaDesejos.objects.get_or_create(lista=lista, produto=produto, defaults={'quantidade': 1} )

        if not created:
            item_lista.quantidade += 1
            item_lista.save()

        return redirect('wishlist')

def remover_da_lista_de_desejos(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(ItemListaDesejos, id=item_id, lista__user=request.user)
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            item.delete()
        return redirect('wishlist')
