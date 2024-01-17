from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CustomUserCreationForm, CustomAuthenticationForm
from lista_desejos.models import ListaDesejos, ItemListaDesejos
from loja.models import Produto

@login_required(login_url='login')
def profiles(request):

    user = request.user
    listas = ListaDesejos.objects.filter(user=user)
    total_qtd_all_lists = 0
    total_quantidade = 0
    lista_selecionada_id = request.session.get('ultima_lista_id')

    if lista_selecionada_id:
        lista_selecionada = ListaDesejos.objects.filter(id=lista_selecionada_id, user=user).first()
        if lista_selecionada:
            total_quantidade = sum(item.quantidade for item in lista_selecionada.itens.all())


    lista_com_produtos = []
    for lista in listas:
        itens = ItemListaDesejos.objects.filter(lista=lista)
        total_qtd_all_lists += sum(item.quantidade for item in itens)
        lista_com_produtos.append({'lista': lista, 'itens': itens})

    context = {
        'lista_com_produtos': lista_com_produtos,
        'total_qtd_all_lists': total_qtd_all_lists,
        'total_quantidade': total_quantidade
    }
    return render(request, 'users/perfil.html', context)


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('/')

    form = CustomAuthenticationForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Usuário não existe')
        
        # Verifica se username e senha corresponde a um usuário valido
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Cria uma session para o usuário
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha está incorreto')

    return render(request, 'users/login_register.html', {'form': form})

def logout_user(request):
    # Delete a session do usuário
    logout(request)
    messages.success(request, 'usuário desconectado')
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Usuário criado!')

            # loga o usuário assim que finalizar o cadastro
            login(request, user)

            return redirect('/')
        
        else:
            messages.error(request, 'Ocorreu um erro ao registrar')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)
