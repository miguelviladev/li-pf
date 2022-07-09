var image = "sadasdad";

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        image = input.files[0];
        reader.onload = function (e) {
            $('.image-area').html(`<img id="imageResult" src="${e.target.result}" alt="">`);
            $('.image-area').css('background-color', 'transparent');
            $('.image-area:hover').css('cursor', 'default');
            $('.image-area:hover').css('border-color', '#fff');
            $('.image-area').css('padding', '0');
            $('#upload-button').css('display', 'block');
        };
        reader.readAsDataURL(input.files[0]);
    }
};

const container = document.getElementsByTagName('main')[0];
container.addEventListener('click', function (e) {
    if (e.target.id == 'upload-button') {
        doUpload(e);
    };
});

async function doUpload(e) {
    e.preventDefault();
    const reader = new FileReader();
    reader.readAsDataURL(image);
    const name = document.getElementById('imagename').value;
    const collection = document.getElementById('collectionname').value;
    const token = localStorage.getItem('token');
    reader.addEventListener("load", async function(e) {
        const options = {
            method: 'POST',
            headers: {'Content-Type': 'text/html;charset=utf-8'},
            body: JSON.stringify({"token": token, "name": name, "collection": collection, "image": e.target.result})
        };
        const response = await (await fetch('/api/cromos/upload', options)).json();
        if (response.status == 'OK') {
            window.location.href = '/upload';
        } else  {
            alert('Error al subir el cromo');
        }
    });
};