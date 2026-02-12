document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (e) {
        const toggleBtn = e.target.closest(".show-hide-btn");
        if (!toggleBtn) return;

        e.preventDefault();

        const wrapper = toggleBtn.closest(".password-wrapper");
        if (!wrapper) return;

        const input = wrapper.querySelector("input.password-field");
        if (!input) return;

        const icon = toggleBtn.querySelector("i");
        if (!icon) return;

        if (input.type === "password") {
            input.type = "text";
            icon.classList.replace("fa-eye", "fa-eye-slash");
        } else {
            input.type = "password";
            icon.classList.replace("fa-eye-slash", "fa-eye");
        }
    });
});
