from django.shortcuts import render
from . models import Produto
from lista_desejos.models import ListaDesejos

def loja(request):
    produtos = Produto.objects.all()
    total_quantidade = 0
    lista_selecionada = None

    if request.user.is_authenticated:
        total_quantidade = ListaDesejos.get_total_quantidade(request.user)
        listas = ListaDesejos.objects.filter(user=request.user)
        lista_selecionada = listas.first() if listas.exists() else None

    context = {'produtos': produtos,
               'total_quantidade': total_quantidade,
               'lista_selecionada':lista_selecionada}
    return render(request, 'loja/loja.html', context)
