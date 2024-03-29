from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from . models import ListaDesejos, ItemListaDesejos
from loja.models import Produto
from django.contrib import messages

def wishlist(request):
    #redireciona o usuário se ele tentar acessar diretamente a url da lista de desejos
    if not request.user.is_authenticated:
        return redirect('login')
    
    listas = ListaDesejos.objects.filter(user=request.user)

    if not listas.exists():
        return render(request, 'loja/wishlist.html', {'listas': None})
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

def criar_lista(request, produto_id=None):

    if request.method == 'POST':
        nome_lista = request.POST.get('nome_lista')
        if nome_lista:
            nova_lista = ListaDesejos.objects.create(user=request.user, nome=nome_lista)
            request.session['ultima_lista_id'] = nova_lista.id

            if produto_id:
                produto = get_object_or_404(Produto, id=produto_id)
                ItemListaDesejos.objects.create(lista=nova_lista, produto=produto, quantidade=1)

        return redirect('wishlist')
    
def adicionar_a_lista_de_desejos(request, produto_id, lista_id):
    if request.user.is_authenticated:
        produto = get_object_or_404(Produto, id=produto_id)

        lista_id = request.session.get('ultima_lista_id')
        if lista_id:
            lista = get_object_or_404(ListaDesejos, id=lista_id, user=request.user)
        else:
            lista = ListaDesejos.objects.filter(user=request.user).order_by('-id').first()
            if lista:
                # Salva a lista como a lista atual na sessão
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
            response_message = 'Produto adicionado à lista de desejos com sucesso!'
        else:
            messages.success(request, 'Produto adicionado à lista de desejos com sucesso!')

        origem = request.GET.get('origem', 'default')

        #Verifica se é uma requisição ajax
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': response_message})
        else:
            if origem == 'lista':
                return redirect('wishlist')
            else:
                return redirect('/')

def remover_da_lista_de_desejos(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(ItemListaDesejos, id=item_id, lista__user=request.user)
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            item.delete()
        return redirect('wishlist')
    
def verificar_produto_lista(request, produto_id):
    if request.user.is_authenticated:
        lista_id = request.session.get('ultima_lista_id')
        if lista_id:
            esta_na_lista = ItemListaDesejos.objects.filter(lista__id=lista_id, lista__user=request.user, produto__id=produto_id).exists()
        else:
            esta_na_lista = False

        return JsonResponse({'estaNaLista': esta_na_lista})
    else:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
    
def deletar_lista_desejos(request, lista_id):
    user = request.user
    lista = get_object_or_404(ListaDesejos, id=lista_id, user=user)

    lista_selecionada_id = request.session.get('ultima_lista_id')
    # Verifica se o ID da lista é o mesmo da lista armazenada na sessão
    if lista_id == lista_selecionada_id:
        lista.delete()
        listas = ListaDesejos.objects.filter(user=user)
        if listas.exists():
            request.session['ultima_lista_id'] = listas.last().id
            # Se ainda existir outras listas atualiza a sessao para o útlimo id da lista
        else:
            del request.session['ultima_lista_id']
            # Se n existir mais listas, remove da sessão o id da lista
    else:
        lista.delete()
        # Deleta a lista caso n esteja selecionada, por ex: deletar pela URL

    return redirect('wishlist')
