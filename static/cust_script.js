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
    const template = document.getElementById("GombBox");
    const buttonContainer = document.querySelector(".GombBox");
    buttonContainer.innerHTML = ""

    const slots = response['slots'];
    console.log(slots);

    slots.forEach(slot => {
        // Create a wrapper for the radio button and label
        // Create the radio button
        const radioButton = document.createElement('input');
        radioButton.type = 'radio';
        radioButton.name = 'timeSlot'; // Ensures only one can be selected
        radioButton.classList.add(`radio`);
        radioButton.classList.add(slot['available'])
        radioButton.value = slot['id'];
        radioButton.id = `slot-${slot['id']}`
        radioButton.dataset.free = slot['available'];

        // Create the label for the radio button
        const label = document.createElement('label');
        label.setAttribute("for", `slot-${slot['id']}`);
        label.classList.add('IdopontLabel');
        label.classList.add(slot['available'])
        label.innerText = `${slot['end_time_hours']}:${slot['end_time_minutes'].toString().padStart(2, '0')}`;
        // Append the radio button and label to the wrapper
        buttonContainer.appendChild(radioButton);
        buttonContainer.appendChild(label);

        // Append the wrapper to the container
    });
}

const checkbox = document.getElementById("billing-required");
// Checkbox eseménykezelő
checkbox.addEventListener('change', () => {
    const extraFields = document.getElementById("billing_data");
    if (checkbox.checked) {
        extraFields.classList.remove('hidden'); // Mezők megjelenítése
    } else {
        extraFields.classList.add('hidden'); // Mezők elrejtése
    }
});

const paymentmethod = document.getElementById("payment_method")
paymentmethod.addEventListener('change', () => {
    const extraFields = document.getElementById("billing_data");
    if (paymentmethod.value === "bankcard") {
        extraFields.classList.remove('hidden'); // Mezők megjelenítése
    } else {
        extraFields.classList.add('hidden'); // Mezők elrejtése
    }
});

function handle_errors(form){
    var isvalid = true
    var formData = new FormData(form);
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }

    if (formData.has("service")) {
        console.log("Service is set.");
        document.getElementById("serviceBox").classList.remove("error");
    } else {
        isvalid = false
        document.getElementById("serviceBox").classList.add("error");
    }
    if (formData.has("timeSlot")) {
        console.log("Slot is set.");
        document.getElementById("GombBox").classList.remove("error");
    }
    else
        isvalid = false
        document.getElementById("GombBox").classList.add("error");
    return isvalid
}
async  function create_reservation()
{
    form = document.getElementById("reservationForm")
    if (!handle_errors(form)){
        console.log("form is not valid")
        return
    }
    if (form.checkValidity()) {
        form.submit();  // Submit the form if valid
      } else {
        form.reportValidity(); // This triggers the browser's built-in validation messages
    }
}
