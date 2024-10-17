$(document).ready(function() {
    $('.post').css('opacity', 0).each(function(i) {
        $(this).delay(i * 200).animate({ opacity: 1 }, 600); // Efecto de desvanecimiento
    });
});



document.addEventListener("DOMContentLoaded", function() {
    // Seleccionamos todos los posts
    const posts = document.querySelectorAll('.post');

    // Función para revisar si el post está visible en la pantalla
    const isInViewport = (element) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };

    // Revisamos los posts al hacer scroll
    const checkPostsInView = () => {
        posts.forEach(post => {
            if (isInViewport(post)) {
                post.classList.add('animate'); // Añadimos la clase de animación
            }
        });
    };

    // Revisamos la visibilidad al cargar la página y cuando haya scroll
    window.addEventListener('scroll', checkPostsInView);
    window.addEventListener('load', checkPostsInView);
});




