document.querySelectorAll('.reaction-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();  // Prevenir la acción predeterminada (no recargar la página)

        const postId = this.getAttribute('data-post-id');
        const reaction = this.getAttribute('data-reaction');

        if (!postId || !reaction) {
            console.error('Error: Los atributos data-post-id o data-reaction no están definidos correctamente.');
            return;
        }

        // Realizar la solicitud AJAX
        fetch(`/react-to-post/${postId}/${reaction}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Asegúrate de incluir el token CSRF
            }
        })
        .then(response => response.json())
        .then(data => {
            // Actualizar los contadores de reacciones sin recargar la página
            document.getElementById('like-count-' + postId).textContent = data.likes_count;
            document.getElementById('love-count-' + postId).textContent = data.loves_count;
            document.getElementById('dislike-count-' + postId).textContent = data.dislikes_count;
        })
        .catch(error => console.error('Error al reaccionar:', error));
    });
});
