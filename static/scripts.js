/*
Login
*/
document.getElementById('loginRegisterForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Az alapértelmezett form submit művelet megakadályozása

    // Felhasználónevet és jelszót lekérjük
    var username = document.getElementById('Felhasznev').value;
    var password = document.getElementById('Jelszo').value;

    // Ellenőrzés, hogy melyik gomb lett megnyomva (Belépés vagy Regisztráció)
    var action = event.submitter.className;
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


document.addEventListener('DOMContentLoaded', function () {
    // Initialize Flatpickr for date selection
    const calendarInput = document.getElementById('calendar-tomorrow');

    flatpickr(calendarInput, {
        minDate: new Date().fp_incr(1), // Minimum date (tomorrow)
        inline: true, // Display as inline calendar
        dateFormat: 'Y-m-d', // Date format to send to server
        onChange: function (selectedDates, dateStr, instance) {
            // Handle date change here
            console.log('Selected date:', dateStr);
            // Call function to send selected date to server
            sendDateToServer(dateStr);
        }
    });

    // Function to send selected date to server
    async function sendDateToServer(selectedDate) {
        console.log(selectedDate);
    };
    function getCurrentSelectedDate() {
        return selectedDate;
    };
});
