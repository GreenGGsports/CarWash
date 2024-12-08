function openModal() {
    document.getElementById("modal").style.display = "block"; // Megjeleníti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'none';
}

function closeModal() {
    document.getElementById("modal").style.display = "none"; // Elrejti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'block';
}

function openLoginModal() {
    document.getElementById("modal").style.display = "none"; 
    document.getElementById("login-modal").style.display = "block"; // Megjeleníti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'none';
}

function closeLoginModal() {
    document.getElementById("login-modal").style.display = "none"; // Elrejti a modált
    document.querySelector('.FoglalasiFelulet').style.display = 'block';
}