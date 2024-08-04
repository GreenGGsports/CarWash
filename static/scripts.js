
/*
CARWASH
*/
document.addEventListener('DOMContentLoaded', function() {
    const showPopupButton = document.getElementById('show-popup-btn');
    const popupContainer = document.getElementById('popup-container');

    showPopupButton.addEventListener('click', function() {
        // AJAX kérés küldése a Flask szerverhez
        fetch('/get-popup')
            .then(response => response.json())
            .then(data => {
                // A HTML kód beillesztése a popup konténerbe
                popupContainer.innerHTML = data.html;

                // A popup megjelenítése
                popupContainer.style.display = 'block';
            })
            .catch(error => {
                console.error('Hiba a popup betöltésekor:', error);
            });
    });
});

// Popup bezárása
function closePopup() {
    const popupContainer = document.getElementById('popup-container');
    popupContainer.style.display = 'none';
}


async function sendSelectionToServer(id, route, callbacks) {
    try {
        const response = await fetch(route, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Sikeres POST kérés:', data);

        if (Array.isArray(callbacks)) {
            callbacks.forEach(callback => {
                if (typeof callback === 'function') {
                    callback(data); // Callback végrehajtása a válasz adatokkal
                }
            });
        }
    } catch (error) {
        console.error('Hiba történt POST kérés során:', error);
    }
}

var CarwashSelected = false
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('HelyszinekContainer');
    const template = document.getElementById('helyszinTemplate').content;

    // Ellenőrző változó
    if (!container.eventListenerAdded) {
        // Event listener hozzáadása csak egyszer
        container.addEventListener('click', async (event) => {
            event.preventDefault(); // Esemény alapértelmezett működésének megakadályozása
            const box = event.target.closest('.box');
            if (box) {
                const id = box.dataset.id;
                console.log(`Carwash selected: ID=${id}`);
                await sendSelectionToServer(id, '/carwash/select', [listServices, listExtras]);
                CarwashSelected = true
            }
        });

        // Zászló beállítása
        container.eventListenerAdded = true;
    }

    // GET kérés az összes helyszín lekérdezésére
    fetch('/carwash/list')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data.forEach(helyszin => {
                const clone = document.importNode(template, true);
                clone.querySelector('.box').dataset.id = helyszin.id;
                clone.querySelector('.MosokCim').textContent = helyszin.location;;
                // only for testing add logo
                clone.querySelector('.helyszin').src = "https://via.placeholder.com/335x100";
                container.appendChild(clone);
            });
        })
        .catch(error => console.error('Hiba történt GET kérés során:', error));
});

var ServiceSelected = false;
async function listServices() {
    const container = document.getElementById('CsomagokContainer'); // Update with actual services container ID
    const template = document.getElementById('CsomagokTemplate').content; // Update with actual service template ID

    try {
        const response = await fetch('/service/list');

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Meglévő szolgáltatások törlése (opcionális)
        container.innerHTML = '';

        data.forEach(csomag => {
            const clone = document.importNode(template, true);
            clone.querySelector('.CsomagokBox').dataset.id = csomag.id;
            clone.querySelector('.csomag_nev').innerHTML = csomag.name;
            clone.querySelector('.leiras').innerHTML = csomag.description;
            container.appendChild(clone);
        });

        if (!container.eventListenerAdded) {
        container.addEventListener('click', async (event) => {
            event.preventDefault(); // Esemény alapértelmezett működésének megakadályozása

            const box = event.target.closest('.CsomagokBox');
            if (box) {
                const id = box.dataset.id;
                console.log(`Service selected: ID=${id}`);
                await sendSelectionToServer(id, '/service/select');
                ServiceSelected = true
            }
        });
        }
        container.eventListenerAdded = true;

    } catch (error) {
        console.error('Hiba történt GET kérés során:', error);
    }
}

async function listExtras() {
    const kulsoContainer = document.getElementById('KulsoExtrakContainer');
    const belsoContainer = document.getElementById('BelsoExtrakContainer');
    const kulsoTemplate = document.getElementById('KulsoExtrakTemplate').content;
    const belsoTemplate = document.getElementById('BelsoExtrakTemplate').content;

    console.log('Templates and containers found');

    try {
        const response = await fetch('/service/list_extra');

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);
        kulsoContainer.innerHTML = '';
        belsoContainer.innerHTML = '';

        if (!Array.isArray(data) || data.length === 0) {
            console.log('No extras found');
            return; // Exit the function early since there's nothing to display
        }


        data.forEach(extra => {
            let container;
            let template;

            if (extra.type === 'exterior') {
                container = kulsoContainer;
                template = kulsoTemplate;
            } else if (extra.type === 'interior') {
                container = belsoContainer;
                template = belsoTemplate;
            }

            if (container && template) {
                const clone = document.importNode(template, true);
                console.log('Content cloneNode executed');

                // Set checkbox label text
                clone.querySelector('.checkbox-label').textContent = extra.name;
                console.log('.checkbox-label executed');

                // Set checkbox id attribute
                const checkboxId = `checkbox-${extra.id}`; // Assuming extra object has an id property
                clone.querySelector('.checkbox').id = checkboxId;

                container.appendChild(clone);
            }
        });
    } catch (error) {
        console.error('Hiba történt GET kérés során:', error);
    }
}
function listSelectedExtras() {
    const selectedExtras = [];

    const kulsoContainer = document.getElementById('KulsoExtrakContainer');
    const belsoContainer = document.getElementById('BelsoExtrakContainer');

    const checkboxes = kulsoContainer.querySelectorAll('.checkbox:checked');
    checkboxes.forEach(checkbox => {
        selectedExtras.push(checkbox.id.replace('checkbox-', ''));
    });

    const belsoCheckboxes = belsoContainer.querySelectorAll('.checkbox:checked');
    belsoCheckboxes.forEach(checkbox => {
        selectedExtras.push(checkbox.id.replace('checkbox-', ''));
    });
    return selectedExtras
}
let selectedDate;
function dateSelected() {
    return !!selectedDate;
} 
document.addEventListener('DOMContentLoaded', function () {
    // Initialize Flatpickr for date selection
    const calendarInput = document.getElementById('calendar-tomorrow');

    flatpickr(calendarInput, {
        minDate: new Date().fp_incr(0), // Minimum date (tomorrow)
        inline: true, // Display as inline calendar
        dateFormat: 'Y-m-d', // Date format to send to server
        onChange: function (selectedDates, dateStr, instance) {
            // Handle date change here
            console.log('Selected date:', dateStr);
            selectedDate = dateStr; // Store the selected date
            // Call function to send selected date to server
            sendDateToServer(dateStr);
        }
    });
    // Function to send selected date to server
    async function sendDateToServer(selectedDate) {
        try {
            const response = await fetch('/booking/set_date', {
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
            const min_date = new Date(result['min_date'])
            generateHourlyButtons(min_date)
            console.log(min_date)
            console.log('Server response:', result);
        } catch (error) {
            console.error('Hiba történt az adatküldés során:', error);
        }
    }


});

var SlotSelected = false;
function generateHourlyButtons(date) {
    const buttonContainer = document.querySelector(".GombBox");
    buttonContainer.innerHTML = ''; // Korábbi gombok törlése

    // A bemeneti dátum (például: datetime.datetime(2024, 7, 30, 9, 0)) UTC idő szerint
    const min_date = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours()));
    /// substract 2 hours bc of timezone mindfuck
    min_date.setHours(min_date.getHours() -4 )
    // 24 órás ciklus
    console.log('Bemeneti dátum:', date)
    console.log('Minimális dátum:', min_date)

    for (let hour = 9; hour <= 17; hour++) {
        // A gombhoz tartozó dátum létrehozása
        const buttonDate = new Date(min_date.getFullYear(), min_date.getMonth(), min_date.getDate(), hour);

        // Korrigált dátum (ha szükséges)
        const correctedButtonDate = new Date(buttonDate.getTime());

        const isFree = correctedButtonDate >= min_date;

        const button = document.createElement('button');
        button.classList.add('IdopontGomb', `free-${isFree}`);
        button.innerText = `${hour}:00`;
        button.dataset.free = isFree;

        // Helyes időzóna beállítása
        button.dataset.date = correctedButtonDate.toLocaleString(); // Megjeleníti a helyi időt

        // Kattintási esemény
        button.addEventListener('click', function (event) {
            event.preventDefault();
            selectedDate = correctedButtonDate.toLocaleString();
            console.log(`Kiválasztott időpont: ${correctedButtonDate.toLocaleString()}`);
            select_appointment(selectedDate);
            SlotSelected  = true;
        });

        buttonContainer.appendChild(button);
    }

    async function select_appointment(selectedDate) {
        try {
            const response = await fetch('/booking/select_slot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ date: selectedDate })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            console.log('Selected Date Sent:', selectedDate);
        } catch (error) {
            console.error('Hiba történt az adatküldés során:', error);
        }
    }
}

function billing_required() {
    // Az űrlap elem lekérése
    var form = document.getElementById('szamlazasForm');
    
    // A form elemeinek lekérése az 'id' attribútum alapján
    var ids = ['email', 'cegnev', 'keresztnev', 'adoszam', 'vezeteknev', 'cim', 'fizetesi_mod'];
    
    ids.forEach(function(id) {
        var element = form.querySelector('#' + id);
        if (element) {
            element.setAttribute('required', 'required');
        }
    });
}

function card_payment() {
    var form = document.getElementById('szamlazasForm');
    
    // A form elemeinek lekérése az 'id' attribútum alapján
    var ids = ['email', 'keresztnev', 'vezeteknev', 'cim', 'fizetesi_mod'];
    
    ids.forEach(function(id) {
        var element = form.querySelector('#' + id);
        if (element) {
            element.setAttribute('required', 'required');
        }
    });
}

var pay_by_card = false
document.getElementById('fizetesi_mod').addEventListener('change', function() {
    var selectedValue = this.value;
    if (selectedValue === 'bankkartya') {
        pay_by_card = true
        card_payment();
    }
    else ( pay_by_card = false)
});

async function postForm(url, formId) {
    const form = document.getElementById(formId);

    // Ellenőrizzük, hogy az űrlap érvényes-e
    if (form.checkValidity()) {
        // Gyűjtjük az összes form adatot
        const formData = new FormData(form);

        // Átalakítjuk a form adatait egy objektummá
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        // Küldjük a POST kérést
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formObject)
            });

            if (response.ok) {
                const jsonResponse = await response.json();
                console.log('Sikeres kérés:', jsonResponse);
                return response;
            } else {
                console.error('Hiba a kérés során:', response.statusText)
                return response;
            }
        } catch (error) {
            console.error('Hiba történt:', error);
        }
    } else {
        console.log('Form hiba');
        // Ha a form nem érvényes, jelentjük a validációs hibákat
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                // Ha a mező érvénytelen, hozzáadjuk az 'error' osztályt
                input.classList.add('error');
                console.error(`Érvénytelen mező: ${input.name} - ${input.validationMessage}`);
                console.log(input.classList)
            } else {
                // Ha a mező érvényes, eltávolítjuk az 'error' osztályt
                input.classList.remove('error');
            }
        });
    }
}

function check_reservation() {
    if (!CarwashSelected)
        {
            carwashElement = document.getElementById("HelyszinekContainer")
            if (carwashElement) {
                carwashElement.classList.add("error");
                
            }
        return false
        }
    if (!ServiceSelected) {
        serviceElement = document.getElementById("CsomagokContainer")
            if (serviceElement) {
                serviceElement.classList.add("error");
            }
        return false
    }

    if (!SlotSelected || dateSelected() == false){
        console.log('Slot not selected')
        console.log(SlotSelected)
        console.log(dateSelected())
        slotElement = document.getElementById("IdopontContainer")
        if (slotElement) {
            slotElement.classList.add("error")
        }
        return false
    }

    else {
        return true
    }

}
document.getElementById('FoglalasButton').addEventListener('click', async function() {
    if (!check_reservation()){ return; }

    const response = await fetch('/service/select_extras', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({extra_ids: listSelectedExtras()}) // body data type must match "Content-Type" header
      });
    var checkbox = document.getElementById('ker_szamlat');
    const formId1 = "foglalasForm"
    const url1 = '/reservation/add';
    if(checkbox.checked){
        billing_required()
        console.log('billing requiered')
        const formId2 = 'szamlazasForm';
        const url2 = '/billing/add_billing'
        const response1 = await postForm(url1, formId1);
        const response2 = await postForm(url2, formId2);
    
        if (response1.ok && response2.ok) {
            finalize();
        } 
        else {
            console.error('Egy vagy több kérés nem volt sikeres');
        }
    }
    else if(pay_by_card){
        console.log('pay by card ')
        const formId2 = 'szamlazasForm';
        const url2 = '/reservation/add_billing'            
        const response1 = await postForm(url1, formId1);
        const response2 = await postForm(url2, formId2);

        if (response1.ok && response2.ok) {
                finalize();
            } 
        else {
                console.error('Egy vagy több kérés nem volt sikeres');
            }
        }
    else {
        console.log('Nincs számla start post')
        const response1 = await postForm(url1, formId1);
        console.log('response : ',response1)
        if (response1.ok) {
            finalize();
        } 

    }
// parses JSON response into native JavaScript objects
 });

 async function finalize() {
    console.log('finalize');
    try {
        // AJAX kérés küldése a Flask szerverhez a popup tartalmának lekéréséhez
        const response = await fetch('/reservation/popup');
        console.log(response);
        
        if (response.ok) {
            const data = await response.json();
            const popupContainer = document.getElementById('popup');
            console.log('response', data);
            
            // A HTML kód beillesztése a popup konténerbe
            popupContainer.innerHTML = data.html;

            // A popup megjelenítése
            popupContainer.style.display = 'block';

            // Popup bezárása eseménykezelő beállítása
            const closeButton = document.getElementById('closePopup');
            if (closeButton) {
                closeButton.addEventListener('click', closePopup);
            }
        } else {
            console.error('Hiba a popup tartalom lekérésekor:', response.statusText);
        }
    } catch (error) {
        console.error('Hiba történt:', error);
    }
}

// Popup bezárása
function closePopup() {
    const popupContainer = document.getElementById('popup');
    if (popupContainer) {
        popupContainer.style.display = 'none';
    }
}
