const login_button = document.getElementById('login-button');

login_button.addEventListener('click', doLogin);

async function doLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"username": username, "password": password})
    };
    const response = await fetch('/api/users/auth', options);
    const data = await response.json();
    alert(JSON.stringify(data));
};