function submitForm() {
    const appointment = document.getElementById('appointment').value;
    const licensePlate = document.getElementById('license_plate').value;
    const name = document.getElementById('name').value;
    const phoneNumber = document.getElementById('phone_number').value;
    const brand = document.getElementById('brand').value;
    const type = document.getElementById('type').value;
    const companyId = parseInt(document.getElementById('company_id').value);
    const serviceId = parseInt(document.getElementById('service_id').value);
    const parkingSpot = document.getElementById('parking_spot').value;

    const data = {
        appointment: appointment,
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