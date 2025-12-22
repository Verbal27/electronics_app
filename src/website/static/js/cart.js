document.addEventListener("DOMContentLoaded", function () {
    const tax_rate = 0.08;

    function updateCartTotal() {
        let subtotal = 0;

        document.querySelectorAll(".item-subtotal").forEach(sub => {
            subtotal += parseFloat(sub.dataset.subtotal) || 0;
        });

        const totalDisplay = document.querySelector(".total-price");
        if (totalDisplay) totalDisplay.textContent = "$ " + subtotal.toFixed(2);

        const tax = subtotal * tax_rate;
        const taxDisplay = document.querySelector("[data-tax]");
        if (taxDisplay) taxDisplay.textContent = "$ " + tax.toFixed(2);

        const grandTotalDisplay = document.querySelector(".grand-total-price");
        if (grandTotalDisplay) grandTotalDisplay.textContent = "$ " + (subtotal + tax).toFixed(2);
    }

    document.querySelectorAll('.stock-label').forEach(el => {
        const stock = el.textContent.trim();

        el.classList.remove("text-success", "text-warning", "text-danger");

        if (stock === "In Stock") {
            el.classList.add("text-success");
        } else if (stock === "Low Stock") {
            el.classList.add("text-warning");
        } else {
            el.classList.add("text-danger");
        }
    });


    document.querySelectorAll(".cart-item").forEach(row => {
        const qtyInput = row.querySelector(".qtty");
        const subtotalEl = row.querySelector(".item-subtotal");
        const priceEl = row.querySelector(".item-price");
        const form = row.querySelector(".qty-form");
        const productId = row.dataset.itemId;

        function updateSubtotal() {
            const qty = parseInt(qtyInput.value) || 1;
            const price = parseFloat(priceEl.dataset.price) || 0;
            const subtotal = qty * price;

            subtotalEl.textContent = "$ " + subtotal.toFixed(2);
            subtotalEl.dataset.subtotal = subtotal.toFixed(2);

            updateCartTotal();
        }

        function handleChange() {
            const qty = parseInt(qtyInput.value) || 1;
            updateSubtotal();

            const maxAvailable = parseInt(qtyInput.dataset.max) || Infinity;
            const increaseBtn = row.querySelector(".qty-increase");
            if (qty < maxAvailable) {
                increaseBtn.disabled = false;
            }

            updateServerAjax(qty, form);
        }

        row.querySelector(".qty-increase").addEventListener("click", (e) => {
            const current = parseInt(qtyInput.value) || 1;
            const requested = current + 1;

            checkStockAndUpdate(productId, requested, e.target, () => {
                qtyInput.value = requested;
                handleChange();
            });
        });

        row.querySelector(".qty-decrease").addEventListener("click", (e) => {
            let current = parseInt(qtyInput.value);
            if (current > 1) {
                qtyInput.value = current - 1;
                handleChange();
            }
        });

        updateSubtotal();
    });
});

function checkStockAndUpdate(productId, requestedQty, button, onSuccess) {
    const csrftoken = getCookie("csrftoken");
    const stockcheckurl = `/cart/${productId}/check-stock/`;
    const qtyInput = document.querySelector(".qtty");


    fetch(stockcheckurl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({quantity: requestedQty})
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                qtyInput.dataset.max = data.max_available; // store max
                onSuccess();
                button.disabled = false;
            } else {
                qtyInput.dataset.max = data.max_available;
                button.disabled = true;
                alert(`Only ${data.max_available} available in stock.`);
            }
        })
        .catch(err => console.error("Error checking stock:", err));
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

function updateServerAjax(quantity, form) {
    const updateUrl = form.dataset.updateUrl;

    fetch(updateUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({quantity})
    })
        .then(response => {
            if (!response.ok) throw new Error(`Network response was not ok (${response.status})`);
            return response.json();
        })
        .then(data => {
            console.log("Cart updated:", data);
        })
        .catch(err => console.error("Error updating cart:", err));
}
