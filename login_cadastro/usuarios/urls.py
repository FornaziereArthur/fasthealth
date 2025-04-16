from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('diagnostico/', views.diagnostico, name='diagnostico'),
    path('diagnostico/resultado/<int:diagnostico_id>/', views.resultado_diagnostico, name='resultado_diagnostico'),
    path('historico/', views.historico_diagnosticos, name='historico_diagnosticos'),
    path('perfil/inicial/', views.perfil_inicial, name='perfil_inicial'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/atualizar/', views.atualizar_perfil, name='atualizar_perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
] 