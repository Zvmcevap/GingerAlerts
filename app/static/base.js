document.addEventListener('DOMContentLoaded', () => {
    let dropdown = document.querySelector('.dropdown');
    dropdown.addEventListener('click', function (event) {
        event.stopPropagation();
        dropdown.classList.toggle('is-active');
    });

    let dropdownTexts = document.querySelector('.dropdown-texts');
    dropdownTexts.addEventListener('click', function (event){
        dropdownTexts.classList.toggle('is-active')
    })
});