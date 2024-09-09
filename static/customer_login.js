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
        } else {
            messageElement.textContent = 'Login failed.';
            messageElement.style.color = 'red';
        }
    });
});

document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/user/add_user', {
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

