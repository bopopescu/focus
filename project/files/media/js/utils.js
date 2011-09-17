function get_postal_from_zip(input_field, output_field) {
    $.getJSON('/get_postal_by_zip/' + input_field.val().trim() + "/",
            function(data) {
                output_field.text(data.postal)
                $.ajaxSetup({ cache: false });
            });
}