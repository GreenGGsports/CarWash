
/*
CARWASH
*/

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

var CarwashSelected = false;
document.addEventListener('DOMContentLoaded', () => {
    const boxContainer = document.getElementById('box'); // Fő konténer
    const template = document.getElementById('helyszinTemplate').content;

    // Ellenőrző változó az eseménykezelő hozzáadásának elkerülésére
    if (!boxContainer.eventListenerAdded) {
        // Event listener hozzáadása csak egyszer
        boxContainer.addEventListener('click', async (event) => {
            event.preventDefault(); // Esemény alapértelmezett működésének megakadályozása
            const button = event.target.closest('.keret'); // Legközelebbi keret keresése
            if (button) {
                const id = button.dataset.id;
                console.log(`Carwash selected: ID=${id}`);
                await sendSelectionToServer(id, '/carwash/select', [listServices, listExtras]);
                CarwashSelected = true;
            }
        });

        // Zászló beállítása
        boxContainer.eventListenerAdded = true;
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
                const clone = document.importNode(template, true); // Klónozás
                clone.querySelector('.keret').dataset.id = helyszin.id; // Button ID beállítása
                clone.querySelector('.MosokCim').textContent = helyszin.location; // Cím beállítása

                // Kép URL létrehozása
                const imageFolderPath = '/static/images/';
                const imageUrl = helyszin.image_name ? (imageFolderPath + helyszin.image_name) : "https://via.placeholder.com/335x100";

                // Kép beállítása
                clone.querySelector('.helyszin').src = imageUrl;

                // Hozzáadás a konténerhez
                boxContainer.appendChild(clone);
            });
        })
        .catch(error => console.error('Hiba történt GET kérés során:', error));
});


var ServiceSelected = false;
async function listServices() {
    const container = document.getElementById('CsomagokContainer');
    const template = document.getElementById('CsomagokTemplate').content;
    container.innerHTML = '';

    try {
        const response = await fetch('/service/list');

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        data.forEach(csomag => {
            const clone = document.importNode(template, true);
            clone.querySelector('.CsomagokBox').dataset.id = csomag.id;
            clone.querySelector('.csomag_nev').textContent = csomag.name;

            if (csomag.description) { // Only create description list if there's a description
                const descriptionList = csomag.description.split(';').map(item => item.trim());
                const ul = document.createElement('ul');
                ul.classList.add('leiras');

                descriptionList.forEach(item => {
                    if (item) { // Only add non-empty items
                        const li = document.createElement('li');
                        li.textContent = item;
                        li.classList.add('leiras_li');
                        ul.appendChild(li);
                    }
                });

                clone.querySelector('.CsomagokBox').appendChild(ul);
            }

            container.appendChild(clone);
        });

        if (!container.eventListenerAdded) {
            container.addEventListener('click', async (event) => {
                event.preventDefault();

                const box = event.target.closest('.CsomagokBox');
                if (box) {
                    const id = box.dataset.id;
                    console.log(`Service selected: ID=${id}`);
                    await sendSelectionToServer(id, '/service/select');
                    ServiceSelected = true;
                }
            });
            container.eventListenerAdded = true;
        }

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
    kulsoContainer.innerHTML = '';
    belsoContainer.innerHTML = '';
    try {
        const response = await fetch('/service/list_extra');

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);

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
var previouslySelectedDate = false
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
  
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',  // Kezdeti nézet beállítása (pl. havi nézet)
      height: '100%',  // Naptár magasságának beállítása
      width: '100%',   // Naptár szélességének beállítása
      dateClick: function (info) {
        // Remove class from previously selected date
        if (previouslySelectedDate) {
            previouslySelectedDate.classList.remove('selected-date');
          }
  
          // Log the selected date
          console.log('Selected date:', info.dateStr);
  
          // Add class to the currently clicked date
          info.dayEl.classList.add('selected-date');
  
          // Update the previously selected date reference
          previouslySelectedDate = info.dayEl;
        
        sendDateToServer(info.dateStr); // Küldjük el a kiválasztott dátumot a szervernek
      },
      // Egyéb beállítások
    });
  
    calendar.render();  // A naptár megjelenítése
  
    // Funkció a kiválasztott dátum küldésére a szervernek
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
        const min_date = new Date(result['min_date']);
        generateHourlyButtons(min_date);
        console.log(min_date);
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
    min_date.setHours(min_date.getHours()-2); // CET eltérés, nyári időszakban CEST 1 óra

    // 24 órás ciklus
    console.log('Bemeneti dátum:', date)
    console.log('Minimális dátum:', min_date)

    for (let hour = 9; hour <= 17; hour++) {
        // A gombhoz tartozó dátum létrehozása
        const buttonDate = new Date(min_date.getFullYear(), min_date.getMonth(), min_date.getDate(), hour);
        buttonDate.setHours(buttonDate.getHours()+2);   
        correctedButtonDate = buttonDate
        console.log(correctedButtonDate)

        const isFree = correctedButtonDate >= min_date;

        const button = document.createElement('button');
        button.classList.add('IdopontGomb', `free-${isFree}`);
        button.innerText = `${hour}:00`;
        button.dataset.free = isFree;

        // Helyes időzóna beállítása
        button.dataset.date = correctedButtonDate.toISOString();

        // Kattintási esemény
        button.addEventListener('click', function (event) {
            event.preventDefault();
            if (isFree)
                {
                const allButtons = document.querySelectorAll('.IdopontGomb');
                allButtons.forEach(btn => btn.classList.remove('selected'));
                this.classList.add('IdopontGomb', 'selected');
                selectedDate = button.dataset.date;
                console.log(`Kiválasztott időpont: ${correctedButtonDate.toISOString()}`);
                select_appointment(selectedDate);
                SlotSelected  = true;
            }
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
    pay_by_card = true
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

// Validálja az űrlapot és visszaadja a validált eredményt
function validateForm(form) {
    // Ellenőrizzük, hogy az űrlap érvényes-e
    if (!form.checkValidity()) {
        // Ha a form nem érvényes, jelentjük a validációs hibákat
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                // Ha a mező érvénytelen, hozzáadjuk az 'error' osztályt
                input.classList.add('error');
                console.error(`Érvénytelen mező: ${input.name} - ${input.validationMessage}`);
            } else {
                // Ha a mező érvényes, eltávolítjuk az 'error' osztályt
                console.log(`jóóóóóó mező: ${input.name} - ${input.validationMessage}`)
                input.classList.remove('error');
            }
        });
        return false;
    }
    return true;
}

// POST kérést küld az űrlap adataival
async function postForm(url, form) {
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
            return jsonResponse;
        } else {
            console.error('Hiba a kérés során:', response.statusText);
            return null;
        }
    } catch (error) {
        console.error('Hiba történt:', error);
        return null;
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
    var pay_by_card = document.getElementById("fizetesi_mod").value == "bankkartya"

    const reservationForm = document.getElementById("foglalasForm")
    const billingForm = document.getElementById('szamlazasForm')

    const reservationUrl = '/reservation/add';
    const billingUrl = '/billing/add_billing'
    if(checkbox.checked){
        billing_required()
        console.log('billing requiered')
        is_valid_res = validateForm(reservationForm)
        is_valid_bill = validateForm(billingForm)
        if (is_valid_bill && is_valid_res){
            const response1 = await postForm(reservationUrl, reservationForm);
            const response2 = await postForm(billingUrl, billingForm);
            if (response1.ok && response2.ok) {
                showPopup();
            } 
            else {
                console.error('Egy vagy több kérés nem volt sikeres');
            }
        }
        else {return}

    }
    else if(pay_by_card){
        console.log('pay by card ')
        card_payment()     
        is_valid_res = validateForm(reservationForm)
        is_valid_bill = validateForm(billingForm)
        if (is_valid_bill && is_valid_res){
            const response1 = await postForm(reservationUrl, reservationForm);
            const response2 = await postForm(billingUrl, billingForm);
            if (response1.ok && response2.ok) {
                showPopup();
            } 
            else {
                console.error('Egy vagy több kérés nem volt sikeres');
            }
        }
        else {return}
        }

    else {
        console.log('Nincs számla start post')
        const response1 = await postForm(reservationUrl, reservationForm);
        console.log('response : ',response1)
        if (response1.status === 'success') {
            showPopup();
        } 

    }
// parses JSON response into native JavaScript objects
 });

 function showPopup() {
    // Display the popup overlay
    document.getElementById('popupOverlay').style.display = 'flex';

    // Make an API request to get the data
    fetch('/reservation/popup')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json(); // Parse the JSON data from the response
        })
        .then(data => {
            // Assuming the API returns a JSON object with keys matching your variables
            var hely = data.hely;
            var rendszam = data.rendszam;
            var csomag = data.csomag;
            var service_price = data.service_price;
            var extra = data.extra;
            var extra_price = data.extra_price;
            var idopont = data.idopont;  // This is the date string from the server
            var vegosszeg = data.vegosszeg;

            // Parse the date string into a Date object
            var dateObj = new Date(idopont);

            // Format the date as "YYYY-MM-DD HH:MM"
            var year = dateObj.getFullYear();
            var month = String(dateObj.getMonth() + 1).padStart(2, '0'); // Months are zero-based
            var day = String(dateObj.getDate()).padStart(2, '0');
            var hours = String(dateObj.getHours()).padStart(2, '0');
            var minutes = String(dateObj.getMinutes()).padStart(2, '0');

            // Combine the formatted parts
            var formattedDate = `${year}-${month}-${day} ${hours}:${minutes}`;

            // Assigning values to the popup elements
            document.getElementById('hely').innerText = hely;
            document.getElementById('rendszam').innerText = rendszam;
            document.getElementById('csomag').innerText = csomag;
            document.getElementById('service_price').innerText = service_price;
            document.getElementById('extra').innerText = extra;
            document.getElementById('extra_price').innerText = extra_price;
            document.getElementById('idopont').innerText = formattedDate;  // Display the formatted date
            document.getElementById('vegosszeg').innerText = vegosszeg;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Optionally, handle the error and display a user-friendly message
        });
}

// Function to hide the popup
function hidePopup() {
    document.getElementById('popupOverlay').style.display = 'none';
}


