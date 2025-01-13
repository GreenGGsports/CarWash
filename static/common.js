function exit(){
    console.log(window.location.href)
    window.location.href = "/";
}

function closeAllModals() {
    // Hide all modals
    document.getElementById("modal").style.display = "none";
    document.getElementById("login-modal").style.display = "none";
    document.getElementById("register-modal").style.display = "none";
    document.getElementById("LoginOrRegister").style.display = "none";
}

function openModal() {
    closeAllModals(); // Close all modals first
    document.getElementById("modal").style.display = "block"; // Show the default modal
}

function closeModal() {
    closeAllModals(); // Close all modals
}

function openLoginModal() {
    closeAllModals(); // Close all modals first
    document.getElementById("login-modal").style.display = "block"; // Show the login modal
}

function closeLoginModal() {
    document.getElementById("login-modal").style.display = "none"; // Hide the login modal
}

function openRegisterModal() {
    closeAllModals(); // Close all modals first
    document.getElementById("register-modal").style.display = "block"; // Show the register modal
}

function closeRegisterModal() {
    document.getElementById("register-modal").style.display = "none"; // Hide the register modal
}

function openLogRegModal() {
    closeAllModals(); // Close all modals first
    document.getElementById("LoginOrRegister").style.display = "flex"; // Show the login/register choice modal
}

function closeLogRegModal() {
    document.getElementById("LoginOrRegister").style.display = "none"; // Hide the login/register choice modal
}

function toContact() {
    const targetPath = "/"; // A főoldal útvonala

    // Ellenőrizzük, hogy a felhasználó a főoldalon van-e
    if (window.location.pathname === targetPath) {
        // Ha a főoldalon vagyunk, görgessünk az elemhez
        document.getElementById("modal").style.display = "none"; // Elrejti a modált
        scrollToContact();
    } else {
        // Ha nem a főoldalon vagyunk, átirányítunk a főoldalra
        // A cél elem elérése érdekében hash-t adunk hozzá az URL-hez
        window.location.href = targetPath + "#contact";
    }
}

// Görgetés a "Galéria" elemhez
function scrollToContact() {
    const galleryElement = document.getElementById('ContactCim'); // Kiválasztjuk az elemet
    if (galleryElement) {
        galleryElement.scrollIntoView({ behavior: "smooth", block: "start" }); // Simán odagörgetünk
    }
}

// Ha az URL-ben van hash (pl. #gallery), akkor görgetünk
window.addEventListener("load", () => {
    if (window.location.hash === "#contact") {
        scrollToContact();
    }
});

function toGallery() {
    const targetPath = "/"; // A főoldal útvonala

    // Ellenőrizzük, hogy a felhasználó a főoldalon van-e
    if (window.location.pathname === targetPath) {
        // Ha a főoldalon vagyunk, görgessünk az elemhez
        document.getElementById("modal").style.display = "none"; // Elrejti a modált
        scrollToGalery();
    } else {
        // Ha nem a főoldalon vagyunk, átirányítunk a főoldalra
        // A cél elem elérése érdekében hash-t adunk hozzá az URL-hez
        window.location.href = targetPath + "#galery";
    }
}

// Görgetés a "Galéria" elemhez
function scrollToGalery() {
    const galleryElement = document.getElementById('GaleryCim'); // Kiválasztjuk az elemet
    if (galleryElement) {
        galleryElement.scrollIntoView({ behavior: "smooth", block: "start" }); // Simán odagörgetünk
    }
}

// Ha az URL-ben van hash (pl. #gallery), akkor görgetünk
window.addEventListener("load", () => {
    if (window.location.hash === "#galery") {
        scrollToGalery();
    }
});

function toPrices() {
    const targetPath = "/"; // A főoldal útvonala

    // Ellenőrizzük, hogy a felhasználó a főoldalon van-e
    if (window.location.pathname === targetPath) {
        // Ha a főoldalon vagyunk, görgessünk az elemhez
        document.getElementById("modal").style.display = "none"; // Elrejti a modált
        scrollToPrices();
    } else {
        // Ha nem a főoldalon vagyunk, átirányítunk a főoldalra
        // A cél elem elérése érdekében hash-t adunk hozzá az URL-hez
        window.location.href = targetPath + "#prices";
    }
}

// Görgetés a "Galéria" elemhez
function scrollToPrices() {
    const galleryElement = document.getElementById('PricesCim'); // Kiválasztjuk az elemet
    if (galleryElement) {
        galleryElement.scrollIntoView({ behavior: "smooth", block: "start" }); // Simán odagörgetünk
    }
}

// Ha az URL-ben van hash (pl. #gallery), akkor görgetünk
window.addEventListener("load", () => {
    if (window.location.hash === "#prices") {
        scrollToPrices();
    }
});


async function toReservation(){
    const authenticated = await testAuthentication(); // Await the async result
    console.log(authenticated)
    if (authenticated) {
        window.location.href = '/Foglalás/';
    }

    else{
        openLogRegModal()
    }
}


async function testAuthentication() {
    try {
        const response = await fetch('/user/test-auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Request failed with status:', response.status);
            return false; // Request failed, consider user not authenticated
        }

        const data = await response.json();
        console.log('Authentication Test:', data);

        // Assuming the API returns an object with a success or authenticated field
        return data.status === "authenticated";
    } catch (error) {
        console.error('Error during authentication request:', error);
        return false; // Return false on network or unexpected error
    }
}




