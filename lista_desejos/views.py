from django.shortcuts import render, get_object_or_404, redirect
from . models import ListaDesejos, ItemListaDesejos
from loja.models import Produto

def wishlist(request):
    lista_selecionada_id = request.GET.get('lista_id')
    listas = ListaDesejos.objects.filter(user=request.user)


    if lista_selecionada_id:
        lista_selecionada_id = int(lista_selecionada_id)
        lista_selecionada = get_object_or_404(ListaDesejos, id=lista_selecionada_id, user=request.user)
    else:
        lista_selecionada = listas.first()

    itens_lista = lista_selecionada.itens.all() if lista_selecionada else []

    total_quantidade = sum(item.quantidade for item in itens_lista)
    valor_total = sum(item.get_total for item in itens_lista)

    context = {
        'listas': listas, 
        'lista_selecionada_id':lista_selecionada_id, 
        'lista_selecionada': lista_selecionada, 
        'itens_lista': itens_lista,
        'total_quantidade': total_quantidade,
        'valor_total': valor_total,
    }

    return render(request, 'loja/wishlist.html', context)

def adicionar_a_lista_de_desejos(request, produto_id, lista_id):
    if request.user.is_authenticated:
        produto = get_object_or_404(Produto, id=produto_id)

        lista = get_object_or_404(ListaDesejos, id=lista_id, user=request.user)
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
