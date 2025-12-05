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
            updateServerAjax(productId, qty);
        }

        row.querySelector(".qty-increase").addEventListener("click", () => {
            qtyInput.value = parseInt(qtyInput.value) + 1;
            handleChange();
        });

        row.querySelector(".qty-decrease").addEventListener("click", () => {
            let current = parseInt(qtyInput.value);
            if (current > 1) qtyInput.value = current - 1;
            handleChange();
        });

        qtyInput.addEventListener("change", handleChange);

        updateSubtotal();
    });
});


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

function updateServerAjax(productId, quantity) {
    fetch(`/cart/${productId}/update`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrftoken,
        },
        body: `quantity=${quantity}`
    })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .catch(err => console.error("Error updating cart:", err));
}
