from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from Users.views import *
from unittest.mock import patch, MagicMock
from Users.models import MembroEquipe 
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpRequest
from django.shortcuts import redirect

User = get_user_model() 

class Login_Testcase(TestCase):
    
    def setUp(self):
        # Cria um usuário do tipo MembroEquipe
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('login') 
    
    def test_login_page_loads_correctly(self):
        """Testa se a página de login carrega corretamente."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Verifica se a página foi carregada com sucesso
        self.assertTemplateUsed(response, 'login.html')  # Verifica se o template correto foi usado

    def test_login_with_valid_credentials(self):
        """Testa o login com credenciais válidas."""
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Verifica o código de status 302
        self.assertRedirects(response, '/home/')  # Verifica se o redirecionamento está correto
   
    def test_login_with_invalid_credentials(self):
        """Testa o login com credenciais inválidas."""
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpassword'})
        # Verifica se o login falhou
        self.assertEqual(response.status_code, 200)  # Verifica se a página de login é carregada novamente
        self.assertTemplateUsed(response, 'login.html')  # Verifica se o template de login foi usado novamente

    def test_login_without_credentials(self):
        """Testa o login sem enviar credenciais."""
        response = self.client.post(self.url, {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)  # Verifica se a página é recarregada com status 200
        self.assertTemplateUsed(response, 'login.html')  # Verifica se o template correto é usado


class IsSuperUserFunction_Testcase(TestCase):
    
    def setUp(self):
        """Configuração dos testes: cria usuários com diferentes permissões."""
        # Usuário com permissão de superusuário
        self.superuser = get_user_model().objects.create_user(
            username='superuser', 
            password='superpassword', 
            is_superuser=True
        )
        
        # Usuário sem permissão de superusuário
        self.regular_user = get_user_model().objects.create_user(
            username='regularuser', 
            password='regularpassword', 
            is_superuser=False
        )
    
    def test_is_superuser_with_superuser(self):
        """Verifica se a função retorna True para superusuário."""
        self.assertTrue(isSuperUser(self.superuser))  # A função deve retornar True
    
    def test_is_superuser_with_regular_user(self):
        """Verifica se a função retorna False para usuário regular."""
        self.assertFalse(isSuperUser(self.regular_user))  # A função deve retornar False


class RegisterViewTest(TestCase):

    def setUp(self):
        """Configuração dos testes: Criação de superusuário e usuário regular"""
        self.superuser = get_user_model().objects.create_superuser(
            username='superuser', password='superpassword'
        )
        self.regular_user = get_user_model().objects.create_user(
            username='regularuser', password='regularpassword'
        )
        self.url = reverse('register')  # URL da view de registro

    def test_register_page_for_regular_user(self):
        """Testa se um usuário regular é redirecionado para o login."""
        self.client.login(username='regularuser', password='regularpassword')  # Login como usuário regular
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Espera um redirecionamento (status 302)
        self.assertRedirects(response, '/login/?next=/register/')  # Espera o redirecionamento para /login/?next=/register/

    def test_register_page_without_login(self):
        """Testa se um usuário não autenticado é redirecionado para o login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Espera um redirecionamento (status 302)
        self.assertRedirects(response, '/login/?next=/register/')  # Espera o redirecionamento para /login/?next=/register/

