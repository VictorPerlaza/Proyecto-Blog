
        // Añadir la clase "form-control" a todos los inputs y selects del formulario
        document.querySelectorAll('.post-form input, .post-form select, .post-form textarea').forEach(function(element) {
            element.classList.add('form-control');
        });