from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from users.forms import CustomAuthenticationForm

class TestLogin(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username='user test', password='123')
    
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login_register.html')
    
    def test_login_user(self):
        response = self.client.post(reverse('login'), {'username':'user test', 'password':'123'})
        self.assertRedirects(response, '/')

class TestLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user test', password='123')
        self.client.login(username='user test', password='123')

    def test_logout_user(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

class TestRegister(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login_register.html')
    
    
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username':'novo_user', 
            'email':'user@email.com',
            'password1': 'Testesenha123',
            'password2': 'Testesenha123',
        })
        
        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.count(), 1)

# Para validação do formnulário de autenticação
class TestCustomAuthenticationForm(TestCase):
    def test_form(self):
        self.user = User.objects.create_user(username='user test', password='123')
        form_data = {'username':'user test', 'password':'123'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())
