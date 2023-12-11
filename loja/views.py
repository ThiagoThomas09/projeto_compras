from django.shortcuts import render
from . models import *

def loja(request):
    produtos = Produto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'loja/loja.html', context)

def wishlist(request):
    context = {}
    return render(request, 'loja/wishlist.html', context)
