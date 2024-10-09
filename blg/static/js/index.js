$(document).ready(function() {
    $('.post').css('opacity', 0).each(function(i) {
        $(this).delay(i * 200).animate({ opacity: 1 }, 600); // Efecto de desvanecimiento
    });
});
