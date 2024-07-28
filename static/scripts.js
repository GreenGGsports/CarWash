/*
Login
*/
document.getElementById('loginRegisterForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Az alapértelmezett form submit művelet megakadályozása
    // Felhasználónevet és jelszót lekérjük
    var username = document.getElementById('Felhasznev').value;
    var password = document.getElementById('Jelszo').value;
    // Ellenőrzés, hogy melyik gomb lett megnyomva (Belépés vagy Regisztráció)
    var action = event.submitter.name;
    if (action === 'Belepes') {
        // Belépés gomb megnyomva
        loginOrRegister('/user/login', username, password);
    } else if (action === 'Regisztracio') {
        // Regisztráció gomb megnyomva
        loginOrRegister('/user/add_user', username, password);
    }
});

function loginOrRegister(url, username, password) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_name: username, password: password }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'logged_in') {
            alert('Belépés sikeres!');
            // Ide írd meg az utasításokat, amiket szeretnél a belépés után végezni
        } else if (data.status === 'success') {
            alert('Regisztráció sikeres!');
            // Ide írd meg az utasításokat, amiket szeretnél a regisztráció után végezni
        } else {
            alert('Sikertelen művelet!');
        }
    })
    .catch(error => {
        console.error('Hiba történt:', error);
        alert('Hiba történt a kérés során. Kérlek próbáld újra később.');
    });
}
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
                clone.querySelector('.cim').innerHTML = helyszin.location;
                // only for testing add logo
                clone.querySelector('.helyszin').src = "https://via.placeholder.com/335x100";
                container.appendChild(clone);
            });
        })
        .catch(error => console.error('Hiba történt GET kérés során:', error));
});

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

        kulsoContainer.innerHTML = '';
        belsoContainer.innerHTML = '';

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
            const response = await fetch('/reservation/set_date', {
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

function generateHourlyButtons(date) {
    console.log(date)
    const buttonContainer = document.querySelector('.IdopontLine');
    buttonContainer.innerHTML = ''; // Korábbi gombok törlése

    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    // 24 órás ciklus
    for (let hour = 9; hour <= 17; hour++) {
        const buttonDate = new Date(date.getFullYear(), date.getMonth(), date.getDate(), hour);
        const isFree = buttonDate >= now;

        const button = document.createElement('button');
        button.classList.add('IdopontGomb', `free-${isFree}`);
        button.innerText = `${hour}:00`;
        button.dataset.free = isFree;
        button.dataset.date = buttonDate.toISOString();

        // Kattintási esemény
        button.addEventListener('click', function() {
            event.preventDefault();
            selectedDate = buttonDate.toLocaleString()
            console.log(`Kiválasztott időpont: ${buttonDate.toLocaleString()}`);
            select_appointment(selectedDate)
        });

        buttonContainer.appendChild(button);
        async function select_appointment(selectedDate) {
            try {
                if (button.dataset.free){
                    const response = await fetch('/reservation/select_slot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ date: selectedDate })
                    });
                }
                if(!button.dataset.free){
                    console.log('appointment is not available')
                }
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
        
                console.log(selectedDate)
            } catch (error) {
                console.error('Hiba történt az adatküldés során:', error);
            }
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
                return res;
            }
        } catch (error) {
            console.error('Hiba történt:', error);
        }
    } else {
        console.log('Form hiba')
        // Ha a form nem érvényes, jelentjük a validációs hibákat
        const inputs = form.querySelectorAll('input, select, textarea');
        console.log(inputs)
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                // Ha a mező érvénytelen, hozzáadjuk az 'error' osztályt
                input.classList.add('error');
            } else {
                // Ha a mező érvényes, eltávolítjuk az 'error' osztályt
                input.classList.remove('error');
            }
        });
    }
}


document.getElementById('FoglalasButton').addEventListener('click', async function() {
    if (dateSelected() == false){
        console.log("date")
        throw "error date not selected"
    }
    const response = await fetch('/service/select_extras', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
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
    else if(pay_by_card){
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
        const response1 = await postForm(url1, formId1);
        console.log('response : ',response1)
        if (response1.ok) {
            finalize();
        } 

    }
    console.log(listSelectedExtras())
// parses JSON response into native JavaScript objects
    });
async function finalize(){
    console.log('finalize')
}
