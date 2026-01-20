(function () {
    'use strict';

    function initCheckout() {
        const form = document.getElementById('checkout-form');
        if (!form) return;

        const cardSection = form.querySelector('.card-details');
        const savedBlock = form.querySelector('#saved-address-block');
        const newBlock = form.querySelector('#new-address-block');

        const shippingPriceEl = document.getElementById('shipping-price');
        const taxEl = document.getElementById('tax');
        const grandTotalEl = document.getElementById('grand-total');

        const subtotal = parseFloat(grandTotalEl?.dataset.subtotal || 0);
        const taxRate = 0.08;

        function updatePaymentVisibility() {
            if (!cardSection) return;

            const selected = form.querySelector('input[name="payment_method"]:checked');
            const show = selected && selected.dataset.requiresCard === '1';
            cardSection.style.display = show ? 'block' : 'none';
        }

        function updateAddressVisibility() {
            if (!savedBlock || !newBlock) return;

            const selected = form.querySelector('input[name="address_mode"]:checked');
            const mode = selected?.value;

            savedBlock.style.display = mode === 'saved' ? 'flex' : 'none';
            newBlock.style.display = mode === 'saved' ? 'none' : 'flex';
        }

        function updateTotals(price) {
            if (!shippingPriceEl || !taxEl || !grandTotalEl) return;

            const shipping = parseFloat(price || 0);
            const tax = (subtotal + shipping) * taxRate;

            shippingPriceEl.textContent = `$ ${shipping.toFixed(2)}`;
            taxEl.textContent = `$ ${tax.toFixed(2)}`;
            grandTotalEl.textContent = `$ ${(subtotal + shipping + tax).toFixed(2)}`;
        }

        form.addEventListener('change', function (e) {
            const t = e.target;

            if (t.matches('input[name="payment_method"]')) {
                updatePaymentVisibility();
            }

            if (t.matches('input[name="address_mode"]')) {
                updateAddressVisibility();
            }

            if (t.matches('input[name="shipping"]')) {
                updateTotals(t.dataset.price);
            }
        });

        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });

        updatePaymentVisibility();
        updateAddressVisibility();

        const checkedShipping = form.querySelector('input[name="shipping"]:checked');
        if (checkedShipping) {
            updateTotals(checkedShipping.dataset.price);
        }
    }

    document.addEventListener('DOMContentLoaded', initCheckout);
})();
