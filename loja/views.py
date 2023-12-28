from django.shortcuts import render
from . models import Produto
from lista_desejos.models import ListaDesejos

def loja(request):
    produtos = Produto.objects.all()
    total_quantidade = 0

    if request.user.is_authenticated:
        total_quantidade = ListaDesejos.get_total_quantidade(request.user)

    context = {'produtos': produtos,
               'total_quantidade': total_quantidade,}
    return render(request, 'loja/loja.html', context)
