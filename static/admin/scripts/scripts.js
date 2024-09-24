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
                        $('#new_car_model').val(data.new_car_model);
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
    function fetchAvailableSlots() {
        const carwashId = $('#carwash').val();
        const reservationDate = $('#reservation_date').val();

        if (carwashId && reservationDate) {
            $.ajax({
                url: '/booking/api/carwash/get_slots',  // Frissített URL
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    carwash_id: carwashId,
                    date: reservationDate
                }),
                success: function(response) {
                    if (response.success) {
                        let slots = response.slots;
                        let slotOptions = '';

                        slots.forEach(function(slot) {
                            slotOptions += `<option value="${slot.id}">${slot.start_time} - ${slot.end_time}</option>`;
                        });

                        $('#slot').html(slotOptions);
                    } else {
                        alert('Hiba történt a slotok lekérdezésekor: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        }
    }

    // Eseményfigyelők a carwash és a dátum mezők változására
    $('#carwash').on('change', fetchAvailableSlots);
    $('#reservation_date').on('change', fetchAvailableSlots);
});
