from django.shortcuts import get_object_or_404, render
from . models import Produto
from lista_desejos.models import ListaDesejos

def loja(request):
    produtos = Produto.objects.all()
    total_quantidade = 0
    lista_selecionada = None

    if request.user.is_authenticated:
        total_quantidade = ListaDesejos.get_total_quantidade(request.user)
        lista_selecionada_id = request.session.get('ultima_lista_id')

        # Obter o ID da lista selecionada
        if lista_selecionada_id:
            lista_selecionada = get_object_or_404(ListaDesejos, id=lista_selecionada_id, user=request.user)
        else:
            listas = ListaDesejos.objects.filter(user=request.user)
            lista_selecionada = listas.first() if listas.exists() else None

    context = {'produtos': produtos,
               'total_quantidade': total_quantidade,
               'lista_selecionada': lista_selecionada}
    return render(request, 'loja/loja.html', context)
