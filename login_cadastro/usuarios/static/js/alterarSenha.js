document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const alterarSenhaBtn = document.getElementById('alterarSenhaBtn');
    const alterarSenhaModal = document.getElementById('alterarSenhaModal');
    const closeModalBtn = document.querySelector('.close-modal');
    const formAlterarSenha = alterarSenhaModal.querySelector('form');
    const senhaAtual = document.getElementById('senha-atual');
    const novaSenha = document.getElementById('nova-senha');
    const confirmarSenha = document.getElementById('confirmar-senha');

    // Elementos do dropdown
    const menuToggle = document.getElementById('menuToggle');
    const dropdownContent = document.getElementById('dropdownContent');

    // Função para mostrar mensagem de feedback
    function mostrarMensagem(mensagem, tipo) {
        const mensagemDiv = document.createElement('div');
        mensagemDiv.className = `mensagem-feedback ${tipo}`;
        mensagemDiv.textContent = mensagem;
        
        // Remove mensagem anterior se existir
        const mensagemAnterior = formAlterarSenha.querySelector('.mensagem-feedback');
        if (mensagemAnterior) {
            mensagemAnterior.remove();
        }
        
        formAlterarSenha.insertBefore(mensagemDiv, formAlterarSenha.firstChild);
        
        // Remove a mensagem após 5 segundos
        setTimeout(() => mensagemDiv.remove(), 5000);
    }

    // Toggle do dropdown ao clicar no ícone do usuário
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownContent.classList.toggle('show');
    });

    // Fechar dropdown ao clicar fora
    document.addEventListener('click', function(e) {
        if (!dropdownContent.contains(e.target) && !menuToggle.contains(e.target)) {
            dropdownContent.classList.remove('show');
        }
    });

    // Controle do Modal
    alterarSenhaBtn.addEventListener('click', function(event) {
        event.preventDefault();
        alterarSenhaModal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Bloqueia o scroll da página
        dropdownContent.classList.remove('show');
    });

    closeModalBtn.addEventListener('click', function() {
        alterarSenhaModal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaura o scroll da página
        formAlterarSenha.reset(); // Limpa o formulário
    });

    window.addEventListener('click', function(event) {
        if (event.target == alterarSenhaModal) {
            alterarSenhaModal.style.display = 'none';
            document.body.style.overflow = 'auto';
            formAlterarSenha.reset();
        }
    });

    // Validação e envio do formulário
    formAlterarSenha.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Validação das senhas
        if (novaSenha.value !== confirmarSenha.value) {
            mostrarMensagem('As senhas não coincidem!', 'erro');
            return;
        }

        if (novaSenha.value.length < 8) {
            mostrarMensagem('A nova senha deve ter pelo menos 8 caracteres!', 'erro');
            return;
        }

        // Obter o token CSRF
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(formAlterarSenha.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    senha_atual: senhaAtual.value,
                    nova_senha: novaSenha.value,
                    confirmar_senha: confirmarSenha.value
                })
            });

            const data = await response.json();

            if (response.ok) {
                mostrarMensagem('Senha alterada com sucesso!', 'sucesso');
                setTimeout(() => {
                    alterarSenhaModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    formAlterarSenha.reset();
                }, 2000);
            } else {
                mostrarMensagem(data.erro || 'Erro ao alterar a senha!', 'erro');
            }
        } catch (error) {
            mostrarMensagem('Erro ao processar a requisição!', 'erro');
            console.error('Erro:', error);
        }
    });
}); 