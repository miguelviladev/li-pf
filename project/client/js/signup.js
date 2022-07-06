const register_button = document.getElementById('register-button');

register_button.addEventListener('click', doRegister);

async function doRegister(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"username": username})
    };
    const response = await (await fetch('/api/users/create', options)).json();
    if (response.creation == 'OK') {
        document.getElementById("password").value = response.password;
    } else  {
        alert('Registration failed');
    }
};