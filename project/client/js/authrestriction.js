async function verify() {
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"token": localStorage.getItem('token')})
    };
    const response = await (await fetch('/api/users/valid', options)).json();
    if (response.authentication == 'OK') {
        window.location.href = '/';
    };
};

verify();