document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("#additional-form");
    if (!form) return;

    const url = form.dataset.url;

    form.addEventListener("change", function (e) {

        const input = e.target;

        if (!input.classList.contains("custom-tumbler")) return;

        const formData = new FormData();
        formData.append("field", input.name);
        formData.append("value", input.checked);

        input.disabled = true;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                input.checked = !input.checked;
            }
        })
        .catch(() => {
            input.checked = !input.checked;
        })
        .finally(() => {
            input.disabled = false;
        });
    });
});
