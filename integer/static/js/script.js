document.addEventListener('DOMContentLoaded', function() {
    let navigations = document.querySelector('.navigations');
    let toggle = document.querySelector('.toggle');

    toggle.onclick = function() {
        navigations.classList.toggle('active');
    }
});
