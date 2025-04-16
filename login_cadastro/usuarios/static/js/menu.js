document.addEventListener('DOMContentLoaded', function() {
    // Elementos do menu
    const menuItems = document.querySelectorAll('.menu-item');
    const menuToggle = document.getElementById('menuToggle');
    const menuLateral = document.getElementById('menuLateral');
    const menuOverlay = document.getElementById('menuOverlay');

    // Função para abrir o menu
    function abrirMenu() {
        menuLateral.classList.add('menu-aberto');
        menuOverlay.classList.add('ativo');
        document.body.style.overflow = 'hidden';
    }

    // Função para fechar o menu
    function fecharMenu() {
        menuLateral.classList.remove('menu-aberto');
        menuOverlay.classList.remove('ativo');
        document.body.style.overflow = 'auto';
    }

    // Adiciona evento de clique para cada item do menu
    menuItems.forEach(item => {
        item.addEventListener('click', function(event) {
            const destino = this.getAttribute('href');
            
            // Se for o botão de alterar senha, não fecha o menu
            if (this.id === 'alterarSenhaBtn') {
                return;
            }
            
            // Previne o comportamento padrão para links com #
            if (destino === '#') {
                event.preventDefault();
                return;
            }
            
            // Fecha o menu antes de redirecionar
            fecharMenu();
        });
    });

    // Fecha o menu ao clicar no overlay
    menuOverlay.addEventListener('click', fecharMenu);

    // Toggle do menu ao clicar no botão
    menuToggle.addEventListener('click', function(event) {
        event.stopPropagation();
        if (menuLateral.classList.contains('menu-aberto')) {
            fecharMenu();
        } else {
            abrirMenu();
        }
    });

    // Fecha o menu ao pressionar a tecla ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && menuLateral.classList.contains('menu-aberto')) {
            fecharMenu();
        }
    });
}); 