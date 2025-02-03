function toggleSearch() {
    let searchContainer = document.querySelector(".search-container");
    let searchInput = document.getElementById("searchInput");

    // Alternar la clase "active" para mostrar/ocultar
    searchContainer.classList.toggle("active");

    if (searchContainer.classList.contains("active")) {
        searchInput.focus(); // Enfocar cuando se abre
    } else {
        searchInput.value = ""; // Limpiar cuando se cierra
    }
}

function validateSearch() {
    let searchInput = document.getElementById("searchInput");

    if (searchInput.value.trim() === "") {
        alert("Por favor, escribe algo antes de buscar.");
        return false;
    }

    return true;
}
