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