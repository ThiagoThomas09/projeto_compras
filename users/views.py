from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def profiles(request):
    context = {}
    return render(request, 'users/perfil.html', context)


def login_user(request):

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
