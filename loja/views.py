from django.shortcuts import render

def loja(request):
    context = {}
    return render(request, 'loja/loja.html', context)

def wishlist(request):
    context = {}
    return render(request, 'loja/wishlist.html', context)
