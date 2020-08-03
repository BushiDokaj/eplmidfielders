$(document).ready(function () {
    $('.scroll_table').DataTable({
    "paging": false,
    "searching": false,
    "info": false,
    "scrollX": true,
    "scrollY": 300
    });
    $('.dataTables_length').addClass('bs-select');
});