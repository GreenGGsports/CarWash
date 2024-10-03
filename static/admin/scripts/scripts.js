$(document).ready(function() {
    // Automatically convert input to uppercase while typing
    $('#new_car_license_plate').on('input', function() {
        $(this).val($(this).val().toUpperCase());
    });

    $('#new_car_license_plate').autocomplete({
        source: function(request, response) {
            // Clear all fields before making the request
            clearFormFields();

            $.ajax({
                url: '/api/car/get_car_data',
                dataType: 'json',
                data: {
                    license_plate: request.term.toUpperCase() // Convert input to uppercase before sending
                },
                success: function(data) {
                    if (data.error) {
                        response([]);  // No data found, show empty list
                    } else {
                        // Populate form fields with the received data
                        $('#new_car_license_plate').val(data.new_car_license_plate);
                        $('#new_car_type').val(data.new_car_type);
                        $('#new_car_brand').val(data.new_car_brand);
                        $('#new_car_model').val(data.new_car_model);
                        $('#new_customer_forname').val(data.customer_forname);
                        $('#new_customer_lastname').val(data.customer_lastname);
                        $('#new_customer_phone_number').val(data.customer_phone_number);
                        
                        if (data.billing_name) {
                            $('#billing_name').val(data.billing_name);
                            $('#address').val(data.address);
                            $('#email').val(data.email);
                            $('#company_name').val(data.company_name);
                            $('#tax_ID').val(data.tax_ID);
                            $('#billing_required').prop('checked', true); // Mark billing required as checked
                        }

                        // Pass the data to autocomplete to show the license plate
                        response([{
                            label: data.new_car_license_plate,
                            value: data.new_car_license_plate
                        }]);
                    }
                },
                error: function() {
                    response([]);  // In case of an error, show an empty list
                }
            });
        },
        minLength: 3  // Trigger after typing at least 3 characters
    });

    // Function to clear form fields
    function clearFormFields() {
        $('#new_car_type').val('');
        $('#new_car_brand').val('');
        $('#new_car_model').val('');
        $('#new_customer_forname').val('');
        $('#new_customer_lastname').val('');
        $('#new_customer_phone_number').val('');
        $('#billing_name').val('');
        $('#address').val('');
        $('#email').val('');
        $('#company_name').val('');
        $('#tax_ID').val('');
        $('#billing_required').prop('checked', false);
    }

    // Fetch available slots based on carwash and reservation date
    function fetchAvailableSlots() {
        const carwashId = $('#carwash').val();
        const reservationDate = $('#reservation_date').val();

        if (carwashId && reservationDate) {
            $.ajax({
                url: '/booking/api/carwash/get_slots',  // Updated endpoint
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

                        $('#slot').html(slotOptions);  // Populate slot dropdown
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

    // Event listeners for carwash and date changes
    $('#carwash').on('change', fetchAvailableSlots);
    $('#reservation_date').on('change', fetchAvailableSlots);
});
