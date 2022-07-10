const container = document.getElementsByTagName("main")[0];
container.addEventListener('click', function (e) {
    if (e.target.id == 'keep-button' || e.target.id == 'keep-icon') {
        doKeepImg(e);
    };
    if (e.target.id == 'copy-button' || e.target.id == 'copy-icon') {
        doTransferImg(e);
    };
});

async function doKeepImg(e) {
    e.preventDefault();
    alert('Imagem salva com sucesso!');
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "token": localStorage.getItem('token'), "id": window.location.href.substring(window.location.href.lastIndexOf('/') + 1), "username": "" })
    };
    const response = await (await fetch('/api/cromos/claim', options)).json();
    //const response = await (await fetch('/api/users/auth', options)).json();
    //if (response.authentication == 'OK') {
    //    writeToken(response.token);
    //} else {
    //    document.getElementById('username').classList.add('is-invalid');
    //    document.getElementById('password').classList.add('is-invalid');
    //}
};

async function doTransferImg(e) {
    e.preventDefault();
    alert('Imagem salva com sucesso!');
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "token": localStorage.getItem('token'), "id": window.location.href.substring(window.location.href.lastIndexOf('/') + 1), "username": document.getElementById("utilizador").value })
    };
    const response = await (await fetch('/api/cromos/claim', options)).json();
    //const response = await (await fetch('/api/users/auth', options)).json();
    //if (response.authentication == 'OK') {
    //    writeToken(response.token);
    //} else {
    //    document.getElementById('username').classList.add('is-invalid');
    //    document.getElementById('password').classList.add('is-invalid');
    //}
};