$(document).ready( function() {
    /* event form date and time picker */
    $('#id_event_date').datetimepicker({
        pickTime: false,
        dateFormat: 'yyyy-mm-dd',
    });

    $('#id_event_time').datetimepicker({
        format: 'HH:mm:ss',
        pickDate: false,
        pick12HourFormat: false
    });

    $('#id_event_date').data('DateTimePicker').setMinDate(new Date());
    /* /event form date and time picker */
});
