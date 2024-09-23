// script.js

$(document).ready(function() {
    // Automatically convert input to uppercase while typing
    $('#new_car_license_plate').on('input', function() {
        $(this).val($(this).val().toUpperCase());
    });

    $('#new_car_license_plate').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/api/car/get_car_data',
                dataType: 'json',
                data: {
                    license_plate: request.term.toUpperCase() // Convert input to uppercase before sending
                },
                success: function(data) {
                    if (data.error) {
                        response([]);
                    } else {
                        // Populate form fields
                        $('#new_car_license_plate').val(data.new_car_license_plate);
                        $('#new_car_type').val(data.new_car_type);
                        $('#new_car_brand').val(data.new_car_brand);
                        $('#new_customer_forname').val(data.customer_forname);
                        $('#new_customer_lastname').val(data.customer_lastname);
                        $('#new_customer_phone_number').val(data.customer_phone_number);
                        response([{
                            label: data.new_car_license_plate,
                            value: data.new_car_license_plate
                        }]);
                    }
                },
                error: function() {
                    response([]);
                }
            });
        },
        minLength: 3
    });
});
