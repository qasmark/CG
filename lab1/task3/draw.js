const canvas = document.getElementById('circle');
const ctx = canvas.getContext('2d');
const centerX = canvas.width / 2;
const centerY = canvas.height / 2;
const radius = 5;
const color = 'blue';

function drawCircle() {
    let x = radius;
    let y = 0;
    let err = 0;

    while (x >= y) {
        drawPixel(centerX + x, centerY + y);
        drawPixel(centerX + y, centerY + x);
        drawPixel(centerX - y, centerY + x);
        drawPixel(centerX - x, centerY + y);
        drawPixel(centerX - x, centerY - y);
        drawPixel(centerX - y, centerY - x);
        drawPixel(centerX + y, centerY - x);
        drawPixel(centerX + x, centerY - y);

        if (err <= 0) {
            y += 1;
            err += 2 * y + 1;
        }
        if (err > 0) {
            x -= 1;
            err -= 2 * x + 1;
        }
    }
}

function drawPixel(x, y) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, 1, 1);
}

drawCircle();