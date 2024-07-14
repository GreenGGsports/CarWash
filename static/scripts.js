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

async function sendSelectionToServer(id, route, callback) {
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

        if (callback) callback(); // Callback végrehajtása, ha meg van adva
    } catch (error) {
        console.error('Hiba történt POST kérés során:', error);
    }
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
            container.addEventListener('click', async (event) => {
                event.preventDefault(); // Esemény alapértelmezett működésének megakadályozása
                const box = event.target.closest('.box');
                if (box) {
                    const id = box.dataset.id;
                    console.log(`Carwash selected: ID=${id}`);
                    await sendSelectionToServer(id, '/carwash/select', listServices);
                }
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
        // container.innerHTML = '';

        data.forEach(csomag => {
            const clone = document.importNode(template, true);
            clone.querySelector('.CsomagokBox').dataset.id = csomag.id;
            clone.querySelector('.csomag_nev').innerHTML = csomag.name;
            clone.querySelector('.leiras').innerHTML = csomag.description;
            container.appendChild(clone);
        });

        // Event listener hozzáadása a szolgáltatásokhoz
        container.addEventListener('click', async (event) => {
            event.preventDefault(); // Esemény alapértelmezett működésének megakadályozása

            const box = event.target.closest('.CsomagokBox');
            if (box) {
                const id = box.dataset.id;
                console.log(`Service selected: ID=${id}`);
                await sendSelectionToServer(id, '/service/select');
            }
        });

    } catch (error) {
        console.error('Hiba történt GET kérés során:', error);
    }
}

async function listServicesMock() {
    console.log('kurva anyád fukció betölt')
    const container = document.getElementById('CsomagokContainer'); // Update with actual services container ID
    const template = document.getElementById('CsomagokTemplate').content
    console.log('kurva anyád template betölt')
    try {
        // Hardcode-olt adatok helyett
        const mockData = [
            { id: 1, name: 'Szolgáltatás 1', description: 'Ez az első szolgáltatás leírása' },
            { id: 2, name: 'Szolgáltatás 2', description: 'Ez a második szolgáltatás leírása' },
            { id: 3, name: 'Szolgáltatás 3', description: 'Ez a harmadik szolgáltatás leírása' }
        ];
        console.log('kurva anyád')
        mockData.forEach(csomag => {
            const clone = document.importNode(template, true);
            clone.querySelector('.CsomagokBox').dataset.id = csomag.id;
            clone.querySelector('.csomag_nev').innerHTML = csomag.name;
            clone.querySelector('.leiras').innerHTML = csomag.description;
            container.appendChild(clone);
        });

        // Event listener hozzáadása a szolgáltatásokhoz
        container.addEventListener('click', async (event) => {
            event.preventDefault(); // Esemény alapértelmezett működésének megakadályozása

            const box = event.target.closest('.CsomagokBox');
            if (box) {
                const id = box.dataset.id;
                console.log(`Service selected: ID=${id}`);
                // Nem valós szerver hívás, csak console log
                console.log(`Mock server call: Selected service ID=${id}`);
            }
        });

    } catch (error) {
        console.error('Hiba történt mock adatok kezelése során:', error);
    }
}
