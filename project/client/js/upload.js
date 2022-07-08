function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

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