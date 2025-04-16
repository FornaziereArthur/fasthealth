// Modal de Alteração de Senha
const modal = document.getElementById('alterarSenhaModal');
const abrirModal = document.getElementById('alterarSenha');
const fecharModal = document.querySelector('.close-modal');
const formSenha = document.getElementById('formAlterarSenha');

if (abrirModal) {
    abrirModal.addEventListener('click', () => {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        dropdown.classList.remove('show');
    });
}

if (fecharModal) {
    fecharModal.addEventListener('click', () => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
}

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});

if (formSenha) {
    formSenha.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const senhaAtual = document.getElementById('senhaAtual').value;
        const novaSenha = document.getElementById('novaSenha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;

        if (novaSenha !== confirmarSenha) {
            alert('As senhas não coincidem!');
            return;
        }

        try {
            const response = await fetch('/alterar-senha/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    senha_atual: senhaAtual,
                    nova_senha: novaSenha
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert('Senha alterada com sucesso!');
                modal.style.display = 'none';
                formSenha.reset();
            } else {
                alert(data.error || 'Erro ao alterar a senha.');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao processar a solicitação.');
        }
    });
}

// Função para obter o token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 