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

function sendSelectionToServer(id, route, callback) {
    fetch(route, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Sikeres POST kérés:', data);
        if (callback) callback();  // Callback végrehajtása, ha meg van adva
    })
    .catch(error => console.error('Hiba történt POST kérés során:', error));
}
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('HelyszinekContainer');
    const template = document.getElementById('helyszinTemplate').content;

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

            // Event listener hozzáadása a helyszínekhez
            container.addEventListener('click', (event) => {
                const box = event.target.closest('.box');
                if (box) {
                    const id = box.dataset.id;
                    console.log(`Carwash selected: ID=${id}`);
                    sendSelectionToServer(id, '/carwash/select', listServices);
                }
            });
        })
        .catch(error => console.error('Hiba történt GET kérés során:', error));
});

function listServices() {
    const container = document.getElementById('CsomagokContainer'); // Update with actual services container ID
    const template = document.getElementById('CsomagokTemplate').content; // Update with actual service template ID

    // GET kérés az összes szolgáltatás lekérdezésére
    fetch('/service/list')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            container.innerHTML = ''; // Meglévő szolgáltatások törlése
            data.forEach(csomag => {
                const clone = document.importNode(template, true);
                clone.querySelector('.CsomagokBox').dataset.id = csomag.id;
                clone.querySelector('.csomag_nev').innerHTML = csomag.name;
                clone.querySelector('.leiras').innerHTML = csomag.description;
                // only for testing add logo
                clone.querySelector('.helyszin').src = "https://via.placeholder.com/335x100";
                container.appendChild(clone);
            });

            // Event listener hozzáadása a szolgáltatásokhoz
            container.addEventListener('click', (event) => {
                const box = event.target.closest('.CsomagokBox');
                if (box) {
                    const id = box.dataset.id;
                    console.log(`Service selected: ID=${id}`);
                    sendSelectionToServer(id, '/service/select');
                }
            });
        })
        .catch(error => console.error('Hiba történt GET kérés során:', error));
}