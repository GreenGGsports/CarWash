function openModal() {
    document.getElementById("modal").style.display = "block"; // Megjeleníti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'none';
}

function closeModal() {
    document.getElementById("modal").style.display = "none"; // Elrejti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'block';
}

function openLoginModal() {
    document.getElementById("modal").style.display = "none"; 
    document.getElementById("login-modal").style.display = "block"; // Megjeleníti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'none';
}

function closeLoginModal() {
    document.getElementById("login-modal").style.display = "none"; // Elrejti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'block';
}

async function sendDateToServer(selectedDate) {
    try {
        const response = await fetch('/booking/api/carwash/get_slots2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date: selectedDate })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        
        generateHourlyButtons(result); // Assuming this function exists
        console.log('Server response:', result);
    } catch (error) {
        console.error('Hiba történt az adatküldés során:', error);
    }
}

// Function to run on document load
document.addEventListener('DOMContentLoaded', () => {
    // Get today's date in YYYY-MM-DD format
    const today = new Date().toISOString().split('T')[0];

    // Set today's date as the default value in the date input
    const dateInput = document.getElementById('dateInput');
    dateInput.value = today;

    // Call the function with today's date
    sendDateToServer(today);
});

// Event listener for date input change
document.getElementById('dateInput').addEventListener('change', (event) => {
    sendDateToServer(event.target.value);
});
function generateHourlyButtons(response) {
    const template = document.getElementById("idopontKeret")
    const buttonContainer = document.querySelector(".GombBox");

    const slots = response['slots'];
    console.log(slots);

    // Get the template content;
    console.log(template)
    slots.forEach(slot => {
        // Clone the template content

        // Customize the button content (e.g., using slot data)
        const button = document.createElement('button');
        button.classList.add('IdopontGomb', `free-${slot['available']}`);
        button.innerText = `${slot['end_time_hours']}:${slot['end_time_minutes'].toString().padStart(2, '0')}`;
        button.dataset.free = slot['available']
        buttonContainer.appendChild(button);
    });
}