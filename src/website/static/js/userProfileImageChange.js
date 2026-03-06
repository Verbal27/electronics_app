function initProfileImageChange() {
    const fileInput = document.getElementById("profileImageInput");
    const iconButton = document.querySelector(".profile-image-change");

    if (!fileInput || !iconButton) {
        console.warn("Profile image input or button not found");
        return;
    }

    iconButton.addEventListener("click", function (e) {
        e.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileInput.closest("form").submit();
        }
    });
}

document.addEventListener("DOMContentLoaded", initProfileImageChange);
