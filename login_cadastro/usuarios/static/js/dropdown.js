document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const dropdownContent = document.getElementById('dropdownContent');

    // Função para abrir/fechar o dropdown
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownContent.classList.toggle('show');
    });

    // Fechar o dropdown quando clicar fora dele
    document.addEventListener('click', function(e) {
        if (!dropdownContent.contains(e.target) && !menuToggle.contains(e.target)) {
            dropdownContent.classList.remove('show');
        }
    });

    // Prevenir que cliques dentro do dropdown o fechem
    dropdownContent.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}); 