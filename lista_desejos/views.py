from django.shortcuts import render, get_object_or_404, redirect
from . models import ListaDesejos, ItemListaDesejos
from loja.models import Produto

def wishlist(request):
    #redireciona o usuário se ele tentar acessar diretamente a url da lista de desejos
    if not request.user.is_authenticated:
        return redirect('login')
    
    listas = ListaDesejos.objects.filter(user=request.user)

    if not listas.exists():
        lista_padrao = ListaDesejos.objects.create(user=request.user, nome='Minha Lista de Desejos')
        lista_selecionada_id = lista_padrao.id
    else:
        # session para manter a ultima lista selecionada pelo usuário
        lista_selecionada_id = request.GET.get('lista_id') or request.session.get('ultima_lista_id')

        if not lista_selecionada_id:
            lista_selecionada_id = listas.first().id
        else:
            lista_selecionada_id = int(lista_selecionada_id)

    lista_selecionada = get_object_or_404(ListaDesejos, id=lista_selecionada_id, user=request.user)
    request.session['ultima_lista_id'] = lista_selecionada_id

    itens_lista = lista_selecionada.itens.all()

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

def criar_lista(request):
    if request.method == 'POST':
        nome_lista = request.POST.get('nome_lista')
        if nome_lista:
            ListaDesejos.objects.create(user=request.user, nome=nome_lista)
        return redirect('wishlist')

def adicionar_a_lista_de_desejos(request, produto_id, lista_id):
    if request.user.is_authenticated:
        produto = get_object_or_404(Produto, id=produto_id)

        lista_id = request.session.get('ultima_lista_id')
        if lista_id:
            lista = get_object_or_404(ListaDesejos, id=lista_id, user=request.user)
        else:
            lista = ListaDesejos.objects.filter(user=request.user).first()
            if lista:
                # Salva a lista como a lista atual na sessão
                request.session['ultima_lista_id'] = lista.id
            else:
                # Cria uma nova lista se o usuário não tiver nenhuma
                lista = ListaDesejos.objects.create(user=request.user, nome='Minha Lista de Desejos')
                request.session['ultima_lista_id'] = lista.id

        # Responsável por adicionar o item na lista
        item_lista, created = ItemListaDesejos.objects.get_or_create(
            lista=lista, 
            produto=produto, 
            defaults={'quantidade': 1} 
        )

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
