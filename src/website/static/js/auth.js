document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (e) {
        const toggleBtn = e.target.closest(".show-hide-btn");
        if (!toggleBtn) return;

        e.preventDefault();

        const wrapper = toggleBtn.closest(".password-wrapper");
        if (!wrapper) return;

        const input = wrapper.querySelector("input.password-field");
        if (!input) return;

        if (input.type === "password") {
            input.type = "text";
            toggleBtn.classList.replace("fa-eye", "fa-eye-slash");
        } else {
            input.type = "password";
            toggleBtn.classList.replace("fa-eye-slash", "fa-eye");
        }
    });
});
