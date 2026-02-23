document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".mySwiper").forEach(function (el) {
        new Swiper(el, {
            slidesPerView: 3,
            spaceBetween: 16,
            pagination: {
                el: el.querySelector(".swiper-pagination"),
                clickable: true,
            },
            breakpoints: {
                0: {slidesPerView: 1},
                576: {slidesPerView: 2},
                992: {slidesPerView: 3}
            }
        });
    });
});