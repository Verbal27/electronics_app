function initUpdateCartQuantity() {

    $(document).on('click', '.qty-btn', function (e) {
        e.preventDefault();

        const btn = e.target.closest(".qty-btn");
        const updateUrl = btn.dataset.url;
        const form = btn.closest(".qty-form");
        const quantityInput = form.querySelector(".qtty");
        const productId = quantityInput.dataset.productId;
        const cartItem = btn.closest(".cart-item");
        const itemSubtotalEl = cartItem.querySelector(".item-subtotal");
        const cartSubtotalEl = document.querySelector(".total-price");
        const taxAmountEl = document.querySelector("[data-tax]");
        const cartGrandTotalEl = document.querySelector(".grand-total-price");

        if (!updateUrl || !productId) {
            console.error("Missing required data attributes");
            return;
        }

        fetch(updateUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then(res => res.json())

            .then(data => {

                quantityInput.value = data.quantity;

                let increase = $(".qty-increase");

                if (data.has_more) {
                    increase.prop("disabled", false);
                } else {
                    increase.prop("disabled", true);
                }

                if (itemSubtotalEl && data.new_subtotal) {
                    itemSubtotalEl.textContent = `$ ${data.new_subtotal}`;
                }

                if (cartSubtotalEl && data.cart_total) {
                    cartSubtotalEl.textContent = `$ ${data.cart_total}`;
                }

                if (taxAmountEl && data.tax) {
                    taxAmountEl.textContent = `$ ${data.tax}`;
                }

                if (cartGrandTotalEl && data.grand_total) {
                    cartGrandTotalEl.textContent = `$ ${data.grand_total}`;
                }
            })
            .catch(error => {
                console.error("Error updating cart:", error);

            });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    initUpdateCartQuantity();
});