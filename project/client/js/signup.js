const register_button = document.getElementById('register-button');
const copy_button = document.getElementById('copyButton');
const password_input = document.getElementById('password');

register_button.addEventListener('click', doRegister);
copy_button.addEventListener('click', doCopy);

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
        register_button.style.display = "none";
    } else  {
        alert('Registration failed');
    }
};

function doCopy() {
    navigator.clipboard.writeText(password_input.value);
}