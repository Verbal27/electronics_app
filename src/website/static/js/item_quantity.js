document.addEventListener("DOMContentLoaded", function () {

    function updateButtonState(input) {
        const increaseBtn = input.closest("div").querySelector(".qty-increase");
        const decreaseBtn = input.closest("div").querySelector(".qty-decrease");
        const value = parseInt(input.value) || 1;
        const maxQty = parseInt(input.dataset.max);
        const inCart = parseInt(input.dataset.inCart) || 0;

        const availableToAdd = maxQty - inCart;

        if (increaseBtn) increaseBtn.disabled = value >= availableToAdd;
        if (decreaseBtn) decreaseBtn.disabled = value <= 1;
    }

    document.querySelectorAll("input[name='quantity']").forEach(input => {
        updateButtonState(input);
    });

    document.querySelectorAll(".qty-decrease").forEach(btn => {
        btn.addEventListener("click", function () {
            const input = this.closest("div").querySelector("input[name='quantity']");
            let value = parseInt(input.value) || 1;

            if (value > 1) {
                input.value = value - 1;
            }

            updateButtonState(input);
        });
    });

    document.querySelectorAll(".qty-increase").forEach(btn => {
        btn.addEventListener("click", function () {
            const input = this.closest("div").querySelector("input[name='quantity']");
            const maxQty = parseInt(input.dataset.max);
            const inCart = parseInt(input.dataset.inCart) || 0;
            let value = parseInt(input.value) || 1;

            const availableToAdd = maxQty - inCart;

            if (value < availableToAdd) {
                input.value = value + 1;
            }

            updateButtonState(input);
        });
    });

});
