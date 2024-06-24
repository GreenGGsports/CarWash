document.getElementById('appointmentDate').addEventListener('change', function() {
    const selectedDate = this.value;
    fetch('/reservation/list_appointments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ date: selectedDate })
    })
    .then(response => response.json())
    .then(appointments => {
        const appointmentOptions = document.getElementById('appointmentOptions');
        appointmentOptions.innerHTML = ''; // Clear previous options
        appointments.forEach(appointment => {
            const option = document.createElement('div');
            option.className = 'appointment-option';
            option.innerHTML = `
                <input type="radio" name="appointment_id" value="${appointment.id}" required>
                <label>${appointment.start} - ${appointment.end}</label>
            `;
            appointmentOptions.appendChild(option);
        });
    })
    .catch(error => {
        console.error('Error fetching appointments:', error);
    });
});

function submitForm() {
    const selectedAppointmentId = document.querySelector('input[name="appointment_id"]:checked').value;
    const appointmentDate = document.getElementById('appointmentDate').value; // Get appointment date
    const licensePlate = document.getElementById('license_plate').value;
    const name = document.getElementById('name').value;
    const phoneNumber = document.getElementById('phone_number').value;
    const brand = document.getElementById('brand').value;
    const type = document.getElementById('type').value;
    const companyId = parseInt(document.getElementById('company_id').value);
    const serviceId = parseInt(document.getElementById('service_id').value);
    const parkingSpot = document.getElementById('parking_spot').value;

    const data = {
        appointmentDate: appointmentDate, // Include appointment date
        appointment_id: selectedAppointmentId,
        license_plate: licensePlate,
        name: name,
        phone_number: phoneNumber,
        brand: brand,
        type: type,
        company_id: companyId,
        service_id: serviceId,
        parking_spot: parkingSpot
    };

    fetch('/reservation/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle success response here
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error here
    });
}
