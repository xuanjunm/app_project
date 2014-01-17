$(document).ready(function() {
    $('#id_event_date').datepicker({
        minDate: 1,
    });
    $('#id_event_time').timepicker({
        showLeadingZero: false,
    });

    fetch_address_or_not();

    $('#id_fk_address').change(function() {
        fetch_address_or_not();
    });
});

function fetch_address_or_not() {
    if ($('#id_fk_address').val() == '') {
        $('#address_holder').html('<div class="alpha seven columns" '
                                  + 'id="address_wrapper"> No address has'
                                  + ' been selected.</div>');
    } else {
        fetch_address(generate_address_url());
    }
}

function generate_address_url() {
    return $('#address_holder').data('url').replace(/999/,
            $('#id_fk_address').val());
}

function fetch_address(url) {
    this.url = url;
    var ajax_this = this;
    $.ajax({
        timeout: 3000,
        type: 'GET',
        url: ajax_this.url,
        context: ajax_this,
        success: function(response) {
            $('#address_holder').html(response);
        }
    });
}
