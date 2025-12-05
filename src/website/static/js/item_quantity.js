document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".qty-decrease").forEach(btn => {
        btn.addEventListener("click", function () {
            let input = this.parentElement.querySelector("input[name='quantity']");
            let value = parseInt(input.value);
            if (value > 1) input.value = value - 1;
        });
    });

    document.querySelectorAll(".qty-increase").forEach(btn => {
        btn.addEventListener("click", function () {
            let input = this.parentElement.querySelector("input[name='quantity']");
            let value = parseInt(input.value);
            input.value = value + 1;
        });
    });

});