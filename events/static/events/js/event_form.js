$(document).ready(function() {
    $('#id_event_date').datepicker({
        minDate: 1,
    });
    $('#id_event_time').timepicker({
        showLeadingZero: false,
    });
});
