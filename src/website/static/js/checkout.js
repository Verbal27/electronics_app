(function () {
    'use strict';

    window.addEventListener('load', function () {
        var forms = document.getElementsByClassName('needs-validation');

        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);

    document.addEventListener("DOMContentLoaded", function () {
        const paymentRadios = document.querySelectorAll('input[name="payment_method"]');
        const cardSection = document.querySelector('.card-details');

        function toggleCardSection() {
            const selected = document.querySelector('input[name="payment_method"]:checked');
            if (selected && (selected.value === '2' || selected.value === '3')) {
                cardSection.style.display = 'block';
            } else {
                cardSection.style.display = 'none';
            }
        }

        toggleCardSection();

        paymentRadios.forEach(radio => {
            radio.addEventListener('change', toggleCardSection);
        });
    });
})();
