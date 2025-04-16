from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Usuario, Diagnostico, Sintoma, PerfilPaciente
import logging
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return render(request, 'home_nao_logado.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        senha = request.POST.get('password')
        
        try:
            user = authenticate(request, username=email, password=senha)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                
                # Verifica se o usuário já tem perfil
                try:
                    perfil = user.perfil
                    return redirect('home')
                except PerfilPaciente.DoesNotExist:
                    # Se não tem perfil, redireciona para o formulário
                    return redirect('perfil_inicial')
            else:
                messages.error(request, 'Email ou senha inválidos.')
        except Exception as e:
            logger.error(f"Erro no login: {str(e)}")
            messages.error(request, 'Erro ao fazer login. Tente novamente.')
            
    return render(request, 'login.html')

def cadastro(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            cpf = request.POST.get('cpf')
            senha = request.POST.get('password')
            confirma_senha = request.POST.get('confirm_password')
            
            # Log dos dados recebidos (sem a senha)
            logger.info(f"Tentativa de cadastro - Nome: {nome}, Email: {email}, CPF: {cpf}")
            
            # Validações básicas
            if not all([nome, email, cpf, senha, confirma_senha]):
                messages.error(request, 'Todos os campos são obrigatórios.')
                return render(request, 'cadastro.html')
            
            if senha != confirma_senha:
                messages.error(request, 'As senhas não coincidem.')
                return render(request, 'cadastro.html')
                
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Este email já está em uso.')
                return render(request, 'cadastro.html')
                
            if Usuario.objects.filter(cpf=cpf).exists():
                messages.error(request, 'Este CPF já está cadastrado.')
                return render(request, 'cadastro.html')
            
            # Criando o usuário usando o manager personalizado
            user = Usuario.objects.create_user(
                email=email,
                password=senha,
                first_name=nome,
                cpf=cpf
            )
            
            logger.info(f"Usuário criado com sucesso - Email: {email}")
            messages.success(request, 'Cadastro realizado com sucesso! Por favor, faça o login.')
            
            # Redirecionando para a tela de login
            return redirect('login')
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            messages.error(request, 'Erro ao criar usuário. Tente novamente.')
            
    return render(request, 'cadastro.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

@login_required
def diagnostico(request):
    """
    View para a página de diagnóstico onde o paciente descreve seus sintomas.
    """
    if request.method == 'POST':
        try:
            sintomas = request.POST.get('sintomas', '')
            
            # Aqui você implementaria a lógica de IA para análise dos sintomas
            # Por enquanto, vamos usar um exemplo simples
            doenca_sugerida = "Gripe"
            especialidade_recomendada = "Clínico Geral"
            confianca = 0.85
            
            # Criando o diagnóstico
            diagnostico = Diagnostico.objects.create(
                paciente=request.user,
                sintomas=sintomas,
                doenca_sugerida=doenca_sugerida,
                especialidade_recomendada=especialidade_recomendada,
                confianca_diagnostico=confianca
            )
            
            return redirect('resultado_diagnostico', diagnostico_id=diagnostico.id)
            
        except Exception as e:
            logger.error(f"Erro ao criar diagnóstico: {str(e)}")
            messages.error(request, 'Erro ao processar diagnóstico. Tente novamente.')
    
    return render(request, 'diagnostico.html')

@login_required
def resultado_diagnostico(request, diagnostico_id):
    """
    View para mostrar o resultado do diagnóstico.
    """
    try:
        diagnostico = Diagnostico.objects.get(id=diagnostico_id, paciente=request.user)
        return render(request, 'resultado_diagnostico.html', {'diagnostico': diagnostico})
    except Diagnostico.DoesNotExist:
        messages.error(request, 'Diagnóstico não encontrado.')
        return redirect('home')

@login_required
def historico_diagnosticos(request):
    """
    View para mostrar o histórico de diagnósticos do paciente.
    """
    diagnosticos = Diagnostico.objects.filter(paciente=request.user).order_by('-data_criacao')
    return render(request, 'historico_diagnosticos.html', {'diagnosticos': diagnosticos})

@login_required
def perfil_inicial(request):
    """
    View para o formulário inicial de perfil do paciente.
    """
    # Verifica se o usuário já tem perfil
    try:
        perfil = request.user.perfil
        return redirect('home')  # Se já tem perfil, redireciona para home
    except PerfilPaciente.DoesNotExist:
        pass

    if request.method == 'POST':
        try:
            peso = request.POST.get('peso')
            altura = request.POST.get('altura')
            tem_diabetes = request.POST.get('tem_diabetes') == 'on'
            tem_pressao_alta = request.POST.get('tem_pressao_alta') == 'on'
            doencas_diagnosticadas = request.POST.get('doencas_diagnosticadas', '')

            # Criando o perfil
            perfil = PerfilPaciente.objects.create(
                usuario=request.user,
                peso=peso,
                altura=altura,
                tem_diabetes=tem_diabetes,
                tem_pressao_alta=tem_pressao_alta,
                doencas_diagnosticadas=doencas_diagnosticadas
            )

            messages.success(request, 'Perfil criado com sucesso!')
            return redirect('home')

        except Exception as e:
            logger.error(f"Erro ao criar perfil: {str(e)}")
            messages.error(request, 'Erro ao criar perfil. Verifique os dados e tente novamente.')

    return render(request, 'perfil_inicial.html')

@login_required
def perfil_usuario(request):
    """
    View para exibir o perfil do usuário.
    """
    try:
        perfil = request.user.perfil
        # Calcula o IMC
        imc = perfil.peso / (perfil.altura ** 2)
        
        context = {
            'user': request.user,
            'perfil': perfil,
            'imc': imc
        }
        return render(request, 'perfil_usuario.html', context)
    except PerfilPaciente.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('perfil_inicial')

@login_required
def atualizar_perfil(request):
    """
    View para atualizar informações do perfil.
    """
    if request.method != 'POST':
        return redirect('perfil_usuario')

    try:
        perfil = request.user.perfil
        campo = request.POST.get('campo')
        valor = request.POST.get('valor')

        if not campo or not valor:
            messages.error(request, 'Dados inválidos para atualização.')
            return redirect('perfil_usuario')

        # Atualiza os campos baseado no tipo
        if campo == 'nome':
            nome_partes = valor.split()
            if len(nome_partes) > 0:
                request.user.first_name = nome_partes[0]
                request.user.last_name = ' '.join(nome_partes[1:]) if len(nome_partes) > 1 else ''
                request.user.save()
        
        elif campo == 'email':
            if Usuario.objects.filter(email=valor).exclude(id=request.user.id).exists():
                messages.error(request, 'Este email já está em uso.')
                return redirect('perfil_usuario')
            request.user.email = valor
            request.user.save()
        
        elif campo == 'peso':
            try:
                peso = float(valor)
                if 0 < peso <= 300:
                    perfil.peso = peso
                else:
                    messages.error(request, 'Peso inválido. Deve estar entre 0 e 300 kg.')
                    return redirect('perfil_usuario')
            except ValueError:
                messages.error(request, 'Peso deve ser um número válido.')
                return redirect('perfil_usuario')
        
        elif campo == 'altura':
            try:
                altura = float(valor)
                if 0 < altura <= 3:
                    perfil.altura = altura
                else:
                    messages.error(request, 'Altura inválida. Deve estar entre 0 e 3 metros.')
                    return redirect('perfil_usuario')
            except ValueError:
                messages.error(request, 'Altura deve ser um número válido.')
                return redirect('perfil_usuario')
        
        elif campo == 'diabetes':
            if valor.lower() == 'sim':
                perfil.tem_diabetes = True
            elif valor.lower() == 'não' or valor.lower() == 'nao':
                perfil.tem_diabetes = False
                perfil.tipo_diabetes = None
        
        elif campo == 'tipo_diabetes':
            if perfil.tem_diabetes:
                if valor in ['1', '2']:
                    perfil.tipo_diabetes = valor
                else:
                    messages.error(request, 'Tipo de diabetes inválido.')
                    return redirect('perfil_usuario')
        
        elif campo == 'pressao_alta':
            if valor.lower() == 'sim':
                perfil.tem_pressao_alta = True
            elif valor.lower() == 'não' or valor.lower() == 'nao':
                perfil.tem_pressao_alta = False
        
        elif campo == 'outras_doencas':
            perfil.doencas_diagnosticadas = valor

        perfil.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        
    except Exception as e:
        logger.error(f"Erro ao atualizar perfil: {str(e)}")
        messages.error(request, 'Erro ao atualizar perfil. Tente novamente.')

    return redirect('perfil_usuario')

@login_required
def alterar_senha(request):
    """
    View para alterar a senha do usuário.
    """
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        senha_atual = data.get('senha_atual')
        nova_senha = data.get('nova_senha')
        
        # Verifica se o usuário forneceu a senha atual correta
        if not request.user.check_password(senha_atual):
            return JsonResponse({'erro': 'Senha atual incorreta'}, status=400)
        
        # Verifica se a nova senha tem pelo menos 8 caracteres
        if len(nova_senha) < 8:
            return JsonResponse({'erro': 'A nova senha deve ter pelo menos 8 caracteres'}, status=400)
        
        # Altera a senha
        request.user.set_password(nova_senha)
        request.user.save()
        
        # Mantém o usuário logado após a alteração da senha
        login(request, request.user)
        
        return JsonResponse({'mensagem': 'Senha alterada com sucesso'})
        
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Dados inválidos'}, status=400)
    except Exception as e:
        logger.error(f"Erro ao alterar senha: {str(e)}")
        return JsonResponse({'erro': 'Erro ao alterar senha'}, status=500)