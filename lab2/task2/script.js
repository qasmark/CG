const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let color = '#000000';

function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
}
// добавить прозрачность дял png, исправить рисование
// избавиться от глобальных переменных
function draw(e) {
    if (!isDrawing) return;
    ctx.strokeStyle = color;
    ctx.lineCap = 'round';
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function stopDrawing() {
    isDrawing = false;
}

canvas.addEventListener('mouseenter', (e) => {
    if (e.buttons === 1) {
        startDrawing(e);
    }
});

function saveImage() {
    const dataUrl = canvas.toDataURL();
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = 'drawing.png';
    a.click();
}

document.getElementById('newBtn').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

document.getElementById('saveBtn').addEventListener('click', saveImage);

document.getElementById('colorPicker').addEventListener('input', (e) => {
    color = e.target.value;
});

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

document.getElementById('fileInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(file);
});