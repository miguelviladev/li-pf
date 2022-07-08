/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.image-area').html(`<img id="imageResult" src="${e.target.result}" alt="">`);
            $('.image-area').css('background-color', 'transparent');
            $('.image-area:hover').css('cursor', 'default');
            $('.image-area').css('padding', '0');
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

$(function () {
    $('#new-button').on('click', function () {
        collectionName.style.display = 'block';
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
 ========================================== */
var input = document.getElementById('upload');
var infoArea = document.getElementById('upload-label');
var collectionName = document.getElementById('collection-label');

input.addEventListener('change', showFileName);

function showFileName(event) {
    var input = event.srcElement;
    var fileName = input.files[0].name;
    infoArea.style.display = 'block';
    document.getElementById('ImageName').value = fileName;
    document.getElementById('upload-button').disabled = false;

}