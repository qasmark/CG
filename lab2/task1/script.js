const imageContainer = document.getElementById('imageContainer');
const imageView = document.getElementById('imageView');
const fileInput = document.getElementById('fileInput');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imageView.src = e.target.result;
            imageView.classList.remove('draggable');
        };
        reader.readAsDataURL(file);
    }
});

imageContainer.addEventListener('mousedown', (event) => {
    if (event.target === imageView) {
        imageView.classList.add('draggable');
        const offsetX = event.clientX - imageContainer.offsetLeft;
        const offsetY = event.clientY - imageContainer.offsetTop;

        const moveImage = (e) => {
            const x = e.clientX - offsetX;
            const y = e.clientY - offsetY;
            imageContainer.style.left = `${x}px`;
            imageContainer.style.top = `${y}px`;
        };

        const removeListeners = () => {
            imageView.classList.remove('draggable');
            document.removeEventListener('mousemove', moveImage);
            document.removeEventListener('mouseup', removeListeners);
        };

        document.addEventListener('mousemove', moveImage);
        document.addEventListener('mouseup', removeListeners);
    }
});

window.addEventListener('resize', () => {
    centerImage();
});

function centerImage() {
    const containerWidth = imageContainer.offsetWidth;
    const containerHeight = imageContainer.offsetHeight;
    const imageWidth = imageView.offsetWidth; // Используйте offsetWidth вместо width
    const imageHeight = imageView.offsetHeight; // Используйте offsetHeight вместо height

    const offsetX = (containerWidth - imageWidth) / 2;
    const offsetY = (containerHeight - imageHeight) / 2;

    imageContainer.style.left = `${offsetX}px`;
    imageContainer.style.top = `${offsetY}px`;
}