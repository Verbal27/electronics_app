document.addEventListener("click", function (e) {
    const star = e.target.closest(".rating-widget .fa-star");
    if (!star) return;

    const widget = star.closest(".rating-widget");

    if (!widget) return;

    const ratingInput = widget.querySelector("input[name='rating']");
    if (!ratingInput) return;

    const value = Number(star.dataset.value);
    ratingInput.value = value;

    widget.querySelectorAll(".fa-star").forEach((s) => {
        const starValue = Number(s.dataset.value);
        s.classList.toggle("fa-solid", starValue <= value);
        s.classList.toggle("fa-regular", starValue > value);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("exampleModal");
    const triggerBtn = document.getElementById("open-review-btn");

    if (modal && triggerBtn) {
        modal.addEventListener("hidden.bs.modal", function () {
            triggerBtn.focus();
        });
    }
});