function bind_property_forms() {
    $(".house-form").click(function(event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            dataType: 'json',
            type: 'POST',
            url: '/game/property/action/'
        });
    });
}
