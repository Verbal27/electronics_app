toastr.options = {
    closeButton: true,
    progressBar: true,
    positionClass: "toast-top-right",
    timeOut: "3000",
    showMethod: "fadeIn",
    hideMethod: "fadeOut"
};

document.addEventListener("DOMContentLoaded", function () {
    const el = document.getElementById("django-messages");
    if (!el) return;

    let messages;
    try {
        messages = JSON.parse(el.textContent);
    } catch (e) {
        console.error("Invalid django-messages JSON", e);
        return;
    }

    messages.forEach(function (msg) {
        let level = msg.level || "info";
        level = level.split(" ")[0];

        if (typeof toastr[level] === "function") {
            toastr[level](msg.text);
        } else {
            toastr.info(msg.text);
        }
    });
});
