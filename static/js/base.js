$(document).ready( function() {
    /* event form date and time picker */
    /*$('#id_event_date').datepicker({
        format: "yyyy-mm-dd",
        startDate: "+0d",
        autoclose: true,
        todayHighlight: true,
    });
*/

    $('#id_event_date').datetimepicker({
        pickTime: false,
        dateFormat: 'yyyy-mm-dd',
    });

    $('#id_event_time').datetimepicker({
        pickDate: false,
    });

    $('#id_event_date').data('DateTimePicker').setMinDate(new Date());
    /* /event form date and time picker */
});

function formGroupWithError(target) {
    var exception_array = ['#id_event_type_0', '#id_event_type_1'];

    $(target).parent().addClass('has-error');
    
    if (jQuery.inArray(target, exception_array) < 0) {
        $(target).parent().addClass('has-feedback');
        feedback = '<span class="glyphicon glyphicon-remove form-control-feedback"></span>';
        $(target).parent().append(feedback);
    }
}

