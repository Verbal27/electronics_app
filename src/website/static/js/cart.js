document.addEventListener("DOMContentLoaded", function () {
    const TAX_RATE = 0.08;

    function updateCartTotal() {
        let subtotal = 0;

        document.querySelectorAll(".item-subtotal").forEach(el => {
            subtotal += parseFloat(el.dataset.subtotal) || 0;
        });

        const totalEl = document.querySelector(".total-price");
        if (totalEl) {
            totalEl.textContent = "$ " + subtotal.toFixed(2);
        }

        const tax = subtotal * TAX_RATE;
        const taxEl = document.querySelector("[data-tax]");
        if (taxEl) {
            taxEl.textContent = "$ " + tax.toFixed(2);
        }

        const grandTotalEl = document.querySelector(".grand-total-price");
        if (grandTotalEl) {
            grandTotalEl.textContent = "$ " + (subtotal + tax).toFixed(2);
        }
    }

    document.querySelectorAll(".stock-label").forEach(el => {
        const text = el.textContent.trim();
        el.classList.remove("text-success", "text-warning", "text-danger");

        if (text === "In Stock") el.classList.add("text-success");
        else if (text === "Low Stock") el.classList.add("text-warning");
        else el.classList.add("text-danger");
    });

    document.querySelectorAll(".cart-item").forEach(row => {
        const qtyInput = row.querySelector(".qtty");
        const priceEl = row.querySelector(".item-price");
        const subtotalEl = row.querySelector(".item-subtotal");
        const form = row.querySelector(".qty-form");
        const increaseBtn = row.querySelector(".qty-increase");
        const decreaseBtn = row.querySelector(".qty-decrease");
        const productId = row.dataset.itemId;

        function updateSubtotal() {
            const qty = parseInt(qtyInput.value, 10) || 1;
            const price = parseFloat(priceEl.dataset.price) || 0;
            const subtotal = qty * price;

            subtotalEl.textContent = "$ " + subtotal.toFixed(2);
            subtotalEl.dataset.subtotal = subtotal.toFixed(2);

            updateCartTotal();
        }

        function syncServer() {
            updateServerAjax(parseInt(qtyInput.value, 10) || 1, form);
        }

        increaseBtn.addEventListener("click", () => {
            const current = parseInt(qtyInput.value, 10) || 1;
            const requested = current + 1;

            checkStockAndUpdate(
                productId,
                requested,
                increaseBtn,
                () => {
                    qtyInput.value = requested;
                    updateSubtotal();
                    syncServer();
                },
                form
            );
        });

        decreaseBtn.addEventListener("click", () => {
            const current = parseInt(qtyInput.value, 10) || 1;
            if (current <= 1) return;

            qtyInput.value = current - 1;
            increaseBtn.disabled = false;
            updateSubtotal();
            syncServer();
        });

        updateSubtotal();
    });
});

function checkStockAndUpdate(productId, requestedQty, button, onSuccess, form) {
    fetch(form.dataset.checkUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({quantity: requestedQty}),
    })
        .then(res => res.json())
        .then(({success, max_available}) => {
            if (!success) {
                button.disabled = true;
                alert(`Only ${max_available} available in stock.`);
                return;
            }

            onSuccess();
            button.disabled = requestedQty >= max_available;
        })
        .catch(err => console.error("Stock check failed:", err));
}

function updateServerAjax(quantity, form) {
    fetch(form.dataset.updateUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({quantity}),
    })
        .then(res => {
            if (!res.ok) throw new Error(res.status);
            return res.json();
        })
        .catch(err => console.error("Cart update failed:", err));
}

function getCookie(name) {
    let value = null;
    if (document.cookie) {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                value = decodeURIComponent(cookie.slice(name.length + 1));
            }
        });
    }
    return value;
}
