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

document.addEventListener('DOMContentLoaded', function () {
    const shippingRadios = document.querySelectorAll('input[name="shipping"]');
    const shippingElem = document.getElementById('shipping-price');
    const grandTotalElem = document.getElementById('grand-total');

    if (!shippingElem || !grandTotalElem) return;

    const subtotal = parseFloat(grandTotalElem.dataset.subtotal || 0);
    const tax = parseFloat(grandTotalElem.dataset.tax || 0);

    function updateTotals(shippingPrice) {
        const taxRate = 0.08;
        const newTax = (subtotal + shippingPrice) * taxRate;
        shippingElem.textContent = `$ ${shippingPrice.toFixed(2)}`;
        document.getElementById('tax').textContent = `$ ${newTax.toFixed(2)}`;
        grandTotalElem.textContent = `$ ${(subtotal + shippingPrice + newTax).toFixed(2)}`;
    }

    const checkedRadio = document.querySelector('input[name="shipping"]:checked');
    if (checkedRadio) {
        updateTotals(parseFloat(checkedRadio.dataset.price || 0));
    }

    shippingRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            updateTotals(parseFloat(this.dataset.price || 0));
        });
    });
});
