const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function plot(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, 1, 1);
}

function drawLine(x0, y0, x1, y1, color) {
    const deltax = Math.abs(x1 - x0);
    const deltay = Math.abs(y1 - y0);
    const diry = (y1 - y0 > 0) ? 1 : -1;
    let error = 0;
    let deltaerr = deltay + 1;
    let y = y0;

    for (let x = x0; x <= x1; x++) {
        plot(x, y, color);
        error += deltaerr;
        if (error >= deltax + 1) {
            y += diry;
            error -= deltax + 1;
        }
    }
}

// Example usage
drawLine(100, 100, 110, 109, 'red');