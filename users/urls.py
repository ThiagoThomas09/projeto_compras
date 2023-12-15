from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('cadastro/', views.register_user, name='register'),

    path('minha-conta', views.profiles, name='profiles'),
]