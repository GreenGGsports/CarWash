window.addEventListener('load', function() {
    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/user/login', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('login-message');
            if (data.status === 'logged_in') {
                messageElement.textContent = 'Login successful!';
                messageElement.style.color = 'green';
                
                // Ha van redirect_url a válaszban, irányítsuk át a felhasználót
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;  // Átirányítjuk
                }
            } else {
                messageElement.textContent = 'Login failed.';
                messageElement.style.color = 'red';
            }
        })
        .catch(error => {
            console.error("Error during login:", error);
        });
    });

    // Regisztráció és logout kódja változatlanul marad
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();
        document.getElementById("LoginOrRegister").style.display = "none"
        const formData = new FormData(this);
        fetch('/user/register', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('register-message');
            if (data.status === 'success') {
                messageElement.textContent = 'Registration successful!';
                messageElement.style.color = 'green';
            } else {
                messageElement.textContent = 'Registration failed.';
                messageElement.style.color = 'red';
            }
        });
    });

    document.getElementById('logout-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/user/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('logout-message');
            if (data.status === 'logged_out') {
                messageElement.textContent = 'Logout successful!';
                messageElement.style.color = 'green';
            } else {
                messageElement.textContent = 'Logout failed.';
                messageElement.style.color = 'red';
            }
        });
    });
});
