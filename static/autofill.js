document.addEventListener("DOMContentLoaded", function() {
    async function fetchAndFillData() {
        console.log("Fetching data from the server...");
        
        try {
            let response = await fetch('/reservation_autofill/get_data');
            console.log("Received response:", response);

            if (!response.ok) throw new Error('Network response was not ok.');

            let data = await response.json();
            console.log("Parsed data:", data);

            if (data.error) {
                console.error("Error in data:", data.error);
                return;
            }

            // Autofill reservation form
            if (data.reservation) {
                console.log("Filling reservation data:", data.reservation);
                document.querySelector('[name="car_brand"]').value = data.reservation.car_brand || '';
                document.querySelector('[name="telefon"]').value = data.reservation.telefon || '';
                document.querySelector('[name="license_plate"]').value = data.reservation.license_plate || '';
                document.querySelector('[name="car_type"]').value = data.reservation.car_type || '';
                document.querySelector('[name="parking_spot"]').value = data.reservation.parking_spot || '';
                document.querySelector('[name="keresztnev2"]').value = data.reservation.keresztnev2 || '';
                document.querySelector('[name="vezeteknev2"]').value = data.reservation.vezeteknev2 || '';
            } else {
                console.log("No reservation data found.");
            }

            // Autofill billing form
            if (data.billing) {
                console.log("Filling billing data:", data.billing);
                document.querySelector('[name="vezeteknev"]').value = data.billing.vezeteknev || '';
                document.querySelector('[name="keresztnev"]').value = data.billing.keresztnev || '';
                document.querySelector('[name="email"]').value = data.billing.email || '';
                document.querySelector('[name="cim"]').value = data.billing.cim || '';
                document.querySelector('[name="cegnev"]').value = data.billing.cegnev || '';
                document.querySelector('[name="adoszam"]').value = data.billing.adoszam || '';
            } else {
                console.log("No billing data found.");
            }
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    // Call the function to fetch and fill data
    fetchAndFillData();
});