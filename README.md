# FastHealth - Sistema de Diagnóstico de Saúde Online

## 📋 Sobre o Projeto

O FastHealth é uma aplicação web desenvolvida com Django que permite aos usuários realizarem uma avaliação preliminar de saúde através de um sistema de diagnóstico baseado em sintomas. O sistema oferece recomendações médicas iniciais e sugestões de especialidades para consulta.

## ✨ Funcionalidades

- 👤 **Cadastro e autenticação de usuários** usando email e CPF
- 📝 **Perfil de saúde personalizado** com informações básicas do paciente
- 🩺 **Sistema de diagnóstico** baseado em sintomas relatados
- 📊 **Cálculo automático de IMC** com classificação de saúde
- 📜 **Histórico de diagnósticos** para acompanhamento contínuo
- 🔒 **Gestão de conta** com opções para atualização de dados e senha

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django (Python)
- **Banco de Dados**: SQLite
- **Frontend**: HTML, CSS, JavaScript (com Bootstrap para estilização)
- **Autenticação**: Sistema personalizado baseado em AbstractUser do Django

## 🧰 Modelos de Dados

- **Usuario**: Modelo personalizado com email como identificador principal
- **Diagnostico**: Armazena diagnósticos com base nos sintomas relatados
- **Sintoma**: Catálogo de sintomas e suas relações com possíveis doenças
- **PerfilPaciente**: Informações de saúde básicas do usuário com cálculo automático de IMC

## 🔍 Fluxo de Uso

1. Usuário se cadastra com email, nome e CPF
2. Após o login, preenche o perfil inicial de saúde
3. Na tela principal, pode acessar o diagnóstico para descrever sintomas
4. O sistema processa os sintomas e sugere possíveis condições médicas
5. O usuário recebe recomendações de especialidades médicas para consulta
6. Todos os diagnósticos ficam armazenados para consulta no histórico


