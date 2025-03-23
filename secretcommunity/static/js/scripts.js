// static/js/script.js

// Função para inicializar a auto-ocultação de alertas
function initAlertAutohide() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert[data-autohide]');
        alerts.forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s ease-out';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        });
    }, 3000); // Oculta após 3 segundos
}



// Função principal para inicializar todos os scripts
function initAllScripts() {
    initAlertAutohide();
    initNavbarButtonAnimation();
}

// Executar a função principal quando o DOM estiver completamente carregado
document.addEventListener('DOMContentLoaded', initAllScripts);