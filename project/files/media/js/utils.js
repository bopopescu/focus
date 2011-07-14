function get_postal_from_zip(input_field, output_field) {

    $.getJSON('/get_postal_by_zip/' + input_field.val().trim() + "/",
            function(data) {
                output_field.text(data.postal);
            });
}

function set_postal_by_zip(input_field_id, outpud_field_id) {

    input_field = $('#' + input_field_id);
    output_fild = $("#" + outpud_field_id);
    get_postal_from_zip(input_field, output_fild);
    input_field.keyup(function() {
        get_postal_from_zip(input_field, output_fild);
    });

}