from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
    label="Senha",
    strip=False,
    widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
    )

    password2 = forms.CharField(
    label="Confirmação da senha",
    strip=False,
    widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}),
)
    
    
    class Meta:
        model = User
        fields = ['email', 'username']
        labels = {
            'username': 'Nome do usuário',
        }
        # Não é possível trocar o nome do campo da password aqui
        # pq ela n está no UserCreationForm, é definida como forms.CharField
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

# Customizar o formulário de login
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nome de usuário'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Senha'})