function initItemQuantity() {
    $(document).on("click", ".qty-btn", function (e) {
        e.preventDefault();

        const btn = e.target.closest(".qty-btn");
        const form = btn.closest(".product-detail-form");
        const quantityInput = form.querySelector("input[name='quantity']");
        const buyNowQty = document.querySelector(
            'form[action*="buynow"] input[name="quantity"]'
        );

        if (!quantityInput) {
            console.error("Quantity input not found");
            return;
        }

        let value = parseInt(quantityInput.value) || 1;
        const maxQty = parseInt(quantityInput.dataset.max) || 0;
        const inCart = parseInt(quantityInput.dataset.inCart) || 0;

        const availableToAdd = maxQty - inCart;

        if (btn.classList.contains("qty-increase") && value < availableToAdd) {
            value += 1;
        }

        if (btn.classList.contains("qty-decrease") && value > 1) {
            value -= 1;
        }

        quantityInput.value = value;

        if (buyNowQty) {
            buyNowQty.value = value;
        }

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

function initProductTabs() {
    const buttons = document.querySelectorAll(".btn-tab");
    const sections = document.querySelectorAll(".tab-content");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.dataset.target;

            sections.forEach(section => {
                section.classList.add("d-none");
                section.classList.remove("d-flex");
            });

            buttons.forEach(b => b.classList.remove("active"));

            const activeSection = document.getElementById(targetId);
            if (activeSection) {
                activeSection.classList.remove("d-none");
                activeSection.classList.add("d-flex");
            }

            btn.classList.add("active");
        });
    });
}

function initProductGallery() {
    const mainImage = document.querySelector(".product-detail-primary");
    const thumbnails = document.querySelectorAll(".gallery-thumb");

    if (!mainImage || !thumbnails.length) return;

    thumbnails.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            const newSrc = thumb.dataset.full;

            if (!newSrc) return;

            mainImage.src = newSrc;

            thumbnails.forEach(t => t.classList.remove("active"));
            thumb.classList.add("active");
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("input[name='quantity']");
    updateButtonState(input);
    initItemQuantity();
    initProductTabs();
    initProductGallery();
});
