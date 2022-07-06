const register_button = document.getElementById('register-button');

register_button.addEventListener('click', doRegister);

async function doRegister(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"username": username, "password": password})
    };
    const response = await (await fetch('/api/users/auth', options)).json();
    if (response.authentication == 'OK') {
        alert('Login successful');
    } else  {
        alert('Login failed');
    }
};