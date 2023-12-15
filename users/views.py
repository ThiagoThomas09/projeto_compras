from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from loja.models import Cliente
from . forms import CustomUserCreationForm

@login_required(login_url='login')
def profiles(request):
    context = {}
    return render(request, 'users/perfil.html', context)


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('/')


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

    return render(request, 'users/login_register.html')

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

            # Cria um objeto cliente associado com user para funcionar a lista
            Cliente.objects.create(user=user, nome=user.username)
            messages.success(request, 'Usuário criado!')

            # loga o usuário assim que finalizar o cadastro
            login(request, user)

            return redirect('/')
        
        else:
            messages.error(request, 'Ocorreu um erro ao registrar')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)
