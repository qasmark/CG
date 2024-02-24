function drawCartman() {
    const canvas = document.getElementById('cartman');
    const context = canvas.getContext('2d');

    // Head

    context.fillStyle = '#ffeec4';
    context.beginPath();
    context.ellipse(150, 148, 75, 60, 0, 0, 2 * Math.PI, false);
    context.fill();

    // Hat

    // Hat color
    context.beginPath();
    context.fillStyle = '#00b9c6';
    context.bezierCurveTo(75, 140, 85, 89, 140, 85);
    context.bezierCurveTo(140, 85, 190, 69, 225, 130);
    context.bezierCurveTo(225, 130, 150, 92, 75, 140);
    context.fill();
    // pon-pon
    context.beginPath();
    context.strokeStyle = '#ffe01d';
    context.lineWidth = '5';
    context.bezierCurveTo(225, 130, 150, 95, 75, 140);
    context.stroke();
    context.fillStyle = '#ffe01d';
    // pon-pon 2
    context.beginPath();
    context.ellipse(145, 85, 5, 20, -1.2 / 2 * Math.PI, 0, 2 * Math.PI, false);
    context.fill();
    context.beginPath();
    context.ellipse(150, 85, 5, 20, -1.1 / 2 * Math.PI, 0, 2 * Math.PI, false);
    context.fill();
    context.beginPath();
    context.ellipse(150, 85, 5, 20, 1 / 2 * Math.PI, 0, 2 * Math.PI, false);
    context.fill();
    context.beginPath();
    context.ellipse(150, 85, 5, 15, 1.3 / 2 * Math.PI, 0, 2 * Math.PI, false);
    context.fill();

    context.lineWidth = '1';

    // eyes
    context.beginPath();
    context.fillStyle = '#fff';
    context.ellipse(136, 143, 22, 17, 1.35 / 2 * Math.PI, 0, 2 * Math.PI, false);
    context.fill();
    context.beginPath();
    context.strokeStyle = '#c2c1c1';
    context.ellipse(136, 143, 22, 17, 1.35 / 2 * Math.PI, 1 / 2 * Math.PI, -1.5 / 2 * Math.PI, false);
    context.stroke();
    context.beginPath();
    context.fillStyle = '#fff';
    context.ellipse(173, 144, 22, 17, -1.2 / 2 * Math.PI, 0, 2 * Math.PI, false);
    context.fill();
    context.beginPath();
    context.strokeStyle = '#c2c1c1';
    context.ellipse(173, 144, 22, 17, -1.2 / 2 * Math.PI, 1 / 2 * Math.PI, -0.5 / 2 * Math.PI, true);
    context.stroke();
    context.beginPath();
    context.fillStyle = '#000';
    context.arc(164, 143, 2, 0, 2 * Math.PI, false);
    context.fill();
    context.beginPath();
    context.fillStyle = '#000';
    context.arc(142, 143, 2, 0, 2 * Math.PI, false);
    context.fill();

    // mouth

    context.beginPath();
    context.fillStyle = '#000';
    context.moveTo(140, 180);
    context.lineTo(165, 180);
    context.lineTo(160, 191);
    context.lineTo(147, 189);
    context.fill();

    // teeth

    context.beginPath();
    context.fillStyle = '#fff';
    context.rect(145, 181, 5, 3);
    context.fill();

    context.beginPath();
    context.fillStyle = '#fff';
    context.rect(151, 181, 5, 3);
    context.fill();

    context.beginPath();
    context.fillStyle = '#fff';
    context.rect(157, 181, 5, 3);
    context.fill();

    // fat

    context.beginPath();
    context.strokeStyle = '#000';
    context.lineWidth = '0.5';
    context.bezierCurveTo(141, 192, 158, 197, 171, 192);
    context.stroke();

    context.beginPath();
    context.strokeStyle = '#000';
    context.lineWidth = '0.5';
    context.bezierCurveTo(96, 182, 150, 226, 210, 177);
    context.stroke();

    // body

    context.beginPath();
    context.bezierCurveTo(79, 169, 58, 175, 50, 210);
    context.bezierCurveTo(50, 210, 69, 225, 66, 237);
    context.bezierCurveTo(66, 237, 110, 273, 190, 245);
    context.bezierCurveTo(190, 245, 210, 245, 230, 242);
    context.bezierCurveTo(230, 242, 240, 245, 246, 212);
    context.bezierCurveTo(246, 212, 249, 190, 238, 183);
    context.bezierCurveTo(238, 183, 232, 170, 220, 169);
    context.bezierCurveTo(220, 169, 160, 257, 79, 169);
    context.fillStyle = '#ff1c3c';
    context.fill();
    context.fillStyle = '#ffe01d';

    // left arm

    context.beginPath();
    context.bezierCurveTo(51, 215, 40, 180, 75, 200);
    context.bezierCurveTo(75, 200, 113, 220, 60, 220);
    context.bezierCurveTo(60, 220, 56, 217, 52, 215);
    context.fill();

    // right arm

    context.beginPath();
    context.bezierCurveTo(220, 204, 210, 217, 225, 213);
    context.bezierCurveTo(225, 213, 232, 218, 240, 218);
    context.bezierCurveTo(240, 218, 250, 212, 253, 212);
    context.bezierCurveTo(253, 212, 251, 204, 250, 190);
    context.bezierCurveTo(250, 190, 247, 189, 243, 188);
    context.bezierCurveTo(243, 188, 237, 189, 228, 190);
    context.bezierCurveTo(228, 190, 224, 196, 220, 204);
    context.fill();

    // sweater clasp

    context.beginPath();
    context.moveTo(160, 208);
    context.lineWidth = '0.2';
    context.lineTo(160, 253);
    context.stroke();
    context.fillStyle = '#000';

    // buttons

    context.beginPath();
    context.arc(155, 210, 1.5, 0, 2 * Math.PI, false);
    context.fill();

    context.beginPath();
    context.arc(157, 228, 1.5, 0, 2 * Math.PI, false);
    context.fill();

    context.beginPath();
    context.arc(155, 245, 1.5, 0, 2 * Math.PI, false);
    context.fill();

    // pants

    context.beginPath();
    context.bezierCurveTo(70, 240, 115, 265, 190, 245);
    context.bezierCurveTo(190, 245, 197, 245, 232, 242);
    context.bezierCurveTo(232, 242, 230, 245, 223, 261);
    context.bezierCurveTo(223, 261, 180, 250, 150, 261);
    context.bezierCurveTo(150, 261, 110, 250, 77, 260);
    context.bezierCurveTo(77, 260, 72, 250, 70, 240);
    context.fillStyle = '#804429';
    context.fill();

    // shoes

    context.beginPath();
    context.bezierCurveTo(70, 262, 100, 248, 150, 261);
    context.bezierCurveTo(150, 261, 190, 245, 230, 261);
    context.lineTo(70, 262);
    context.fillStyle = '#000';
    context.fill();
    context.stroke();
}


window.onload = drawCartman();