document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = '/reservation/autofill';

    async function getReservationAutofill() {
        try {
            const response = await fetch(apiUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_ACCESS_TOKEN' // Optional: if you have authorization
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Data:', data);

            // Optionally, you can call a function to handle the fetched data
            handleAutofillData(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }


    // Call the function when the document is loaded
    getReservationAutofill();
});

function fill_data(data){
    document.getElementById()
}
