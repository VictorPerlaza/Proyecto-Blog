document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll('#floating-messages .alert');
    messages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = '0'; // Comienza a desvanecerse
            setTimeout(() => {
                message.remove(); // Elimina el mensaje del DOM después del desvanecimiento
            }, 500); // Tiempo de desvanecimiento
        }, 3000); // Tiempo antes de comenzar a desvanecerse (en milisegundos)
    });
});    