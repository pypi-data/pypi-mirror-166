document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', init);
    M.AutoInit();
});

function animateCSS(element, animation, prefix = 'animate__') {
    // We create a Promise and return it
    new Promise((resolve, reject) => {
        const animationName = `${prefix}${animation}`;
        const node = document.querySelector(element);
        node.classList.add(`${prefix}animated`, animationName, 'animate__slow');

        // When the animation ends, we clean the classes and resolve the Promise
        function handleAnimationEnd(event) {
            event.stopPropagation();
            node.classList.remove(`${prefix}animated`, animationName, 'animate__slow');
            resolve('Animation ended');
        }

        node.addEventListener('animationend', handleAnimationEnd, {once: true});
    });
}

function animateSlides() {
    const carouselSlide = document.querySelector('.carousel-item.active');
    // Animate slide transition
    carouselSlide.classList.contains('active') ? animateCSS('.carousel-item.active', 'fadeIn') : null;
    // Animate the Logo
    carouselSlide.querySelector('.carousel-logo.animate') ? animateCSS('.carousel-item.active .logo', 'bounce') : null;
    // Animate the main Image
    carouselSlide.querySelector('.product-image') ? animateCSS('.carousel-item.active .product-image', 'tada') : null;
    // Animate the text
    carouselSlide.querySelector('.carousel-text') ? animateCSS('.carousel-item.active .carousel-text', 'bounceIn') : null;
}

const elems = document.querySelectorAll('.carousel.carousel-slider');
const instance = M.Carousel.init(elems, {
    duration: 0,
    numVisible: 1,
    onCycleTo: animateSlides,
});

const carousel = document.querySelector('.carousel.carousel-slider');
const carouselInstance = M.Carousel.getInstance(carousel);
const carouselAutoplay = parseInt(carousel.dataset.autoplayInterval) * 1000 || 5000;

let interval;

function autoPlayCarousel() {
    if (carousel.dataset.autoplay === 'true') {
        interval = setInterval(() => {
            carouselInstance.next();
        }, carouselAutoplay);
    }
}

function init() {
    autoPlayCarousel();
}