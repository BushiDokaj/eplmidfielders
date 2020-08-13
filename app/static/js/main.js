$(document).ready(function () {
    
    $('.scroll_table').DataTable({
        "paging": false,
        "searching": false,
        "info": false,
        "scrollX": true,
        "scrollY": 300
    });

    $('.dataTables_length').addClass('bs-select');

    var prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    // if (currentScrollPos < 1500 && prevScrollpos > currentScrollPos) {
    //     $('.smart-scroll').removeClass('scrolled-down').addClass('scrolled-up');
    //     $('.smart-scroll').addClass('nav-shadow');
    // } else 
    if (currentScrollPos < 600) {
        $('.smart-scroll').removeClass('scrolled-down').addClass('scrolled-up');
        $('.smart-scroll').addClass('nav-shadow');
    } else {
        $('.smart-scroll').removeClass('scrolled-up').addClass('scrolled-down');
        $('.smart-scroll').removeClass('nav-shadow');
    }
    prevScrollpos = currentScrollPos;
    };
});