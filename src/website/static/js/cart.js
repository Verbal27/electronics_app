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
        const cartCounts = document.querySelectorAll(".cart-count");
        const textCounter = document.getElementById("text-counter");

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

                let dt = data.data;

                quantityInput.value = dt.quantity;

                let increase = cartItem.querySelector(".qty-increase");

                if (dt.has_more) {
                    increase.disabled = false;
                } else {
                    increase.disabled = true;
                }

                if (itemSubtotalEl && dt.new_subtotal) {
                    itemSubtotalEl.textContent = `$ ${dt.new_subtotal}`;
                }

                if (cartSubtotalEl && dt.cart_total) {
                    cartSubtotalEl.textContent = `$ ${dt.cart_total}`;
                }

                if (taxAmountEl && dt.tax) {
                    taxAmountEl.textContent = `$ ${dt.tax}`;
                }

                if (cartGrandTotalEl && dt.grand_total) {
                    cartGrandTotalEl.textContent = `$ ${dt.grand_total}`;
                }

                if (cartCounts.length && dt.items_count !== undefined) {
                    cartCounts.forEach(el => {
                        el.textContent = dt.items_count;
                    });
                    textCounter.textContent = dt.items_count === 1 ? " item" : " items";
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
