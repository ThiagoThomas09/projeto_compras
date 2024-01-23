from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from . models import Produto, Carrinho, ItemCarrinho
from lista_desejos.models import ListaDesejos
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail

def loja(request):
    produtos = Produto.objects.all()
    total_quantidade = 0
    lista_selecionada = None

    if request.user.is_authenticated:
        lista_selecionada_id = request.session.get('ultima_lista_id')

        # Obter o ID da lista selecionada
        if lista_selecionada_id:
            lista_selecionada = get_object_or_404(ListaDesejos, id=lista_selecionada_id, user=request.user)
        else:
            listas = ListaDesejos.objects.filter(user=request.user)
            lista_selecionada = listas.first() if listas.exists() else None
        
        if lista_selecionada:
            total_quantidade = sum(item.quantidade for item in lista_selecionada.itens.all())

    context = {'produtos': produtos,
               'total_quantidade': total_quantidade,
               'lista_selecionada': lista_selecionada}
    return render(request, 'loja/loja.html', context)

def cart(request):
    if request.user.is_authenticated:
        carrinho, created = Carrinho.objects.get_or_create(user=request.user, status_aberto=True)
        itens = carrinho.cart_items.all()

        total_carrinho = sum(item.get_total for item in itens)
        itens_carrinho = sum(item.quantidade for item in itens)

        context = {
        'carrinho': carrinho,
        'itens_carrinho': itens_carrinho,
        'total_carrinho': total_carrinho,
        }

        return render(request, 'loja/cart.html', context)
    else:
        return redirect('login')

    

def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho, created = Carrinho.objects.get_or_create(user=request.user, status_aberto=True)
    item, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)

    if not created:
        item.quantidade += 1
        item.save()
    
    return redirect('cart')

def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__user=request.user)
    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        carrinho = Carrinho.objects.get(user=request.user, status_aberto=True)
        if not carrinho.cart_items.exists():
            return redirect('loja')
        
        total_itens_cart = sum(item.quantidade for item in carrinho.cart_items.all())

        return render(request, 'loja/checkout.html', {'carrinho': carrinho, 'total_itens_cart': total_itens_cart})
    except Carrinho.DoesNotExist:
        return redirect('loja')

def confirmar_pedido(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        carrinho = Carrinho.objects.get(user=request.user, status_aberto=True)
        if not carrinho.cart_items.exists():
            return redirect('loja')

        # Fecha o carrinho
        carrinho.status_aberto = False
        carrinho.save()

        return redirect('profiles')
    except Carrinho.DoesNotExist:
        return redirect('loja')
    
def enviar_email_carrinho_aberto(user_email, carrinho):
    subject = 'Você tem um carrinho aberto!'
    message = f'Olá, percebemos que você ainda tem itens no seu carrinho. Não perca os produtos que você selecionou!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email,]
    send_mail(subject, message, email_from, recipient_list)
    carrinho.email_enviado = True
    carrinho.save()

def verificar_carrinhos_abertos():
    data_limite = timezone.now() - timedelta(minutes=1)
    carrinhos_abertos = Carrinho.objects.filter(
        status_aberto=True, 
        criado_em__lt=data_limite,
        email_enviado=False
    )
    
    for carrinho in carrinhos_abertos:
        enviar_email_carrinho_aberto(carrinho.user.email, carrinho)

