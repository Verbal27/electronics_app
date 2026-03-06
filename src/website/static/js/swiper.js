document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".mySwiper").forEach(function (el) {
        if (el.querySelectorAll(".swiper-slide").length <= 1) {
            return;
        }
        new Swiper(el, {
            slidesPerView: 5,
            spaceBetween: 8,
            watchOverflow: true,
            autoHeight: false,
            pagination: {
                el: el.querySelector(".swiper-pagination"),
                clickable: true,
            },
            breakpoints: {
                0: {slidesPerView: 2},
                576: {slidesPerView: 3},
                768: {slidesPerView: 4},
                992: {slidesPerView: 5}
            }
        });
    });
});
