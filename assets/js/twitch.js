const avatar_images = [
    "/assets/images/avatars/bunny.png",
    "/assets/images/avatars/ice_fool.png",
    "/assets/images/avatars/panda.png",
    "/assets/images/avatars/80s.png",
    "/assets/images/avatars/base05.png",
    "/assets/images/avatars/base13.png",
    "/assets/images/avatars/country10.png",
    "/assets/images/avatars/country16.png",
    "/assets/images/avatars/pineapple.png",
    "/assets/images/avatars/pink.png",
    "/assets/images/avatars/rave06.png",
    "/assets/images/avatars/robot15.png",
    "/assets/images/avatars/rock03.png",
    "/assets/images/avatars/warrior4.png",
    "/assets/images/avatars/zoo8.png"
];

const scale = .7;
const width = 170;
const height = 220;
const scaledWidth = scale * width;
const scaledHeight = scale * height;
const cycleLoop = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

// image number, frame number, xcord, ycord
frameCount = 0;

avatars = [];

window.addEventListener('load', function () {
    canvas = document.getElementById('audience');
    ctx = canvas.getContext('2d');
    canvas.height = canvas.getBoundingClientRect().height;
    canvas.width = canvas.getBoundingClientRect().width;
    generateAvatars(1000);

    // for(i = 0; i <= 4; i++){
    //     randomAvatar = avatar_images[Math.floor(Math.random() * avatar_images.length)];
    //
    //
    // };
});


function generateAvatars(numOfAvatars) {
    for (i = 0; i < numOfAvatars; i++) {
        randomAvatar = Math.floor(Math.random() * avatar_images.length);
        calculatedHeight = (canvas.height - scaledHeight);
        if (i < (numOfAvatars * 1 / 8)) {
            locationy = getRandInteger(0, calculatedHeight * 1 / 8);
        } else if (i < (numOfAvatars * 2 / 8)) {
            locationy = getRandInteger(calculatedHeight * 1 / 8, calculatedHeight * 2 / 8);
        } else if (i < (numOfAvatars * 3 / 8)) {
            locationy = getRandInteger(calculatedHeight * 2 / 8, calculatedHeight * 3 / 8);
        } else if (i < (numOfAvatars * 4 / 8)) {
            locationy = getRandInteger(calculatedHeight * 3 / 8, calculatedHeight * 4 / 8);
        } else if (i < (numOfAvatars * 5 / 8)) {
            locationy = getRandInteger(calculatedHeight * 4 / 8, calculatedHeight * 5 / 8);
        } else if (i < (numOfAvatars * 6 / 8)) {
            locationy = getRandInteger(calculatedHeight * 5 / 8, calculatedHeight * 6 / 8);
        } else if (i < (numOfAvatars * 7 / 8)) {
            locationy = getRandInteger(calculatedHeight * 6 / 8, calculatedHeight * 7 / 8);
        } else if (i < (numOfAvatars * 8 / 8)) {
            locationy = getRandInteger(calculatedHeight * 7 / 8, calculatedHeight * 8 / 8);
        }

        locationx = (Math.random() * (canvas.width + 100)) - 100;
        frameNumber = getRandInteger(0,19)
        img = new Image();
        img.src = avatar_images[randomAvatar];
        avatars.push([randomAvatar, frameNumber, locationx, locationy, img]);
    }
    drawAvatar();
}


function step() {
    frameCount++;
    if (frameCount < 5) {
        window.requestAnimationFrame(step);
        return;
    }
    updateResolution();
    frameCount = 0;
    for (i in avatars) {
        avatars[i][1]++;
        if (avatars[i][1] >= cycleLoop.length) {
            avatars[i][1] = 0;
        }
        drawFrame(avatars[i][4], avatars[i][1], 0, avatars[i][2], avatars[i][3]); // img, frame number, frame sequence, stage x coord, stage y coord
    }
    window.requestAnimationFrame(step);
}

function init() {
    window.requestAnimationFrame(step);
}

function drawFrame(img, frameX, frameY, canvasX, canvasY) {
    ctx.drawImage(img,
        frameX * width, frameY * height, width, height,
        canvasX, canvasY, scaledWidth, scaledHeight);
}

function updateResolution() {
    canvas.height = canvas.getBoundingClientRect().height;
    canvas.width = canvas.getBoundingClientRect().width;
}

function drawAvatar() {
    updateResolution();
    for (i in avatars) {
        img = avatars[i][4];
        avatars[i][4] = img;
    }
    init();
}

function getRandInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


