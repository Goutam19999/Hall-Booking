
const images = document.querySelectorAll('.slideshow-image');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentIndex = 0;
let intervalId;

function showImage(index) {
    images.forEach((img, i) => {
        img.style.display = (i === index) ? 'inline-block' : 'none';
    });
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(currentIndex);
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
}

function resetInterval() {
    clearInterval(intervalId);
    intervalId = setInterval(nextImage, 3000);
}

if (images.length > 0) {
    showImage(currentIndex);
    intervalId = setInterval(nextImage, 3000);

    nextBtn.addEventListener('click', () => {
        nextImage();
        resetInterval();
    });

    prevBtn.addEventListener('click', () => {
        prevImage();
        resetInterval();
    });
}