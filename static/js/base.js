$(document).ready( function() {
    /* event form date and time picker */
/*    $('#id_event_date').datetimepicker({
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

function formGroupWithError(target) {
    var exception_array = ['#id_event_type_0', '#id_event_type_1',
                           '#id_user_gender_0', '#id_user_gender_1'];

    $(target).parent().addClass('has-error');
    
    if (jQuery.inArray(target, exception_array) < 0) {
        $(target).parent().addClass('has-feedback');
        feedback = '<span class="glyphicon glyphicon-remove form-control-feedback"></span>';
        $(target).parent().append(feedback);
    }
}

function formGroupWithRequired(target) {
    $(target).attr('placeholder', 'Required');
}
