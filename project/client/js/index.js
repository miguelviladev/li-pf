document.addEventListener('DOMContentLoaded', async function() {
    const a_button_action = document.getElementById('a-button-action');
    const button_action = document.getElementById('button-action');
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"token": localStorage.getItem('token')})
    };
    const response = await (await fetch('/api/users/valid', options)).json();
    if (response.authentication == 'ERROR') {
        a_button_action.setAttribute('href', '/signin');
        button_action.innerHTML = 'Autenticação <i class="fa-solid fa-key"></i>';
    } else  {
        a_button_action.setAttribute('href', '/gallery');
        button_action.innerHTML = 'Ver Galeria <i class="fa-solid fa-images"></i>';
    };
 }, false);