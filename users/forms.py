from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
    label="Senha",
    strip=False,
    widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
    label="Confirmação da senha",
    strip=False,
    widget=forms.PasswordInput,
)
    
    
    class Meta:
        model = User
        fields = ['email', 'username']
        labels = {
            'username': 'Nome do usuário',
        }
        # Não é possível trocar o nome do campo da password aqui
        # pq ela n está no UserCreationForm, é definida como forms.CharField
