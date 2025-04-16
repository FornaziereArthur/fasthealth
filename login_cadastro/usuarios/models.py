from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado que usa email como identificador único.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'first_name']

    objects = UsuarioManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Diagnostico(models.Model):
    """
    Modelo para armazenar os diagnósticos realizados pelo sistema.
    """
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='diagnosticos')
    data_criacao = models.DateTimeField(auto_now_add=True)
    sintomas = models.TextField()
    doenca_sugerida = models.CharField(max_length=200)
    especialidade_recomendada = models.CharField(max_length=100)
    confianca_diagnostico = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Diagnóstico para {self.paciente.email} - {self.data_criacao.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['-data_criacao']

class Sintoma(models.Model):
    """
    Modelo para armazenar os sintomas mais comuns e suas relações com doenças.
    """
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    doencas_relacionadas = models.JSONField(default=dict)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Sintoma'
        verbose_name_plural = 'Sintomas'

class PerfilPaciente(models.Model):
    """
    Modelo para armazenar informações básicas de saúde do paciente.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso em kg")
    altura = models.DecimalField(max_digits=3, decimal_places=2, help_text="Altura em metros")
    tem_diabetes = models.BooleanField(default=False)
    tem_pressao_alta = models.BooleanField(default=False)
    doencas_diagnosticadas = models.TextField(blank=True, help_text="Liste outras doenças já diagnosticadas")
    data_atualizacao = models.DateTimeField(auto_now=True)

    @property
    def imc(self):
        """Calcula o IMC do paciente"""
        if self.peso and self.altura:
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        return None

    @property
    def classificacao_imc(self):
        """Retorna a classificação do IMC"""
        imc = self.imc
        if imc is None:
            return "Não calculado"
        elif imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        elif imc < 35:
            return "Obesidade Grau I"
        elif imc < 40:
            return "Obesidade Grau II"
        else:
            return "Obesidade Grau III"

    def __str__(self):
        return f"Perfil de {self.usuario.first_name}"

    class Meta:
        verbose_name = 'Perfil do Paciente'
        verbose_name_plural = 'Perfis dos Pacientes'
