document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("input[name='quantity']");
    updateButtonState(input);
    initItemQuantity();
});

function initItemQuantity() {
    $(document).on("click", ".qty-btn", function (e) {
        e.preventDefault();

        const btn = e.target.closest(".qty-btn");
        const form = btn.closest(".product-detail-form");
        const quantityInput = form.querySelector("input[name='quantity']");

        if (!quantityInput) {
            console.error("Quantity input not found");
            return;
        }

        let value = parseInt(quantityInput.value) || 1;
        const maxQty = parseInt(quantityInput.dataset.max) || 0;
        const inCart = parseInt(quantityInput.dataset.inCart) || 0;

        const availableToAdd = maxQty - inCart;

        if (btn.classList.contains("qty-increase")) {
            if (value < availableToAdd) {
                value += 1;
            }
        }

        if (btn.classList.contains("qty-decrease")) {
            if (value > 1) {
                value -= 1;
            }
        }

        quantityInput.value = value;
        updateButtonState(quantityInput);
    });
}

function updateButtonState(input) {
    if (!input) return;

    const form = input.closest(".product-detail-form");
    const increaseBtn = form.querySelector(".qty-increase");
    const decreaseBtn = form.querySelector(".qty-decrease");

    const value = parseInt(input.value) || 1;
    const maxQty = parseInt(input.dataset.max) || 0;
    const inCart = parseInt(input.dataset.inCart) || 0;

    const availableToAdd = maxQty - inCart;

    if (increaseBtn) {
        increaseBtn.disabled = value >= availableToAdd;
    }

    if (decreaseBtn) {
        decreaseBtn.disabled = value <= 1;
    }
}
