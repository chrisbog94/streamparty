const scale = .7;
const width = 170;
const height = 220;
const scaledWidth = scale * width;
const scaledHeight = scale * height;
const cycleLoop = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

frameCount = 0;

// username, image_url, current_frame_number, frame_count, xcord, ycord, img_object, VIP_status
avatars = [];

function generateAvatar(username, avatar) {
    let i = avatars.length + 1;
    maxAvatars = 2000;
    locationy = 0;
    calculatedHeight = (canvas.height - scaledHeight);
    if (avatar[4] === 'PLEB') {
        console.log('PLEB');
        locationy = getRandInteger(calculatedHeight / 8, calculatedHeight * 6 / 8);
    } else if (avatar[4] === 'VIP') {
        console.log('VIP');
        locationy = getRandInteger(calculatedHeight * 7 / 8, calculatedHeight * 8 / 8);
    } else if (avatar[4] !== 'PLEB') {
        console.log('Regular');
        locationy = getRandInteger(calculatedHeight * 6 / 8, calculatedHeight * 7 / 8);
    }

    locationx = (Math.random() * (canvas.width - scaledWidth));
    frameNumber = getRandInteger(0, 5)
    img = new Image();
    img.src = avatar['0'];
    // username, image url, current frame number, frame count, xcord, ycord, img
    avatars.push([username, avatar['0'], frameNumber, avatar['3'], locationx, locationy, img, avatar['4']]);
    sortAvatars();
    return true;
}

function buildAudiance(streamer) {
    //https://tmi.twitch.tv/group/user/' + streamer + '/chatters

    console.log('requesting data from twitch');
    $.ajax({
        url: 'https://tmi.twitch.tv/group/user/' + streamer + '/chatters',
        data: {
            format: 'json'
        },
        error: function () {
            console.log('error');
        },
        dataType: 'jsonp',
        success: function (data) {
            console.log('received data from twitch')
            viewers = []
            for (group in data['data']['chatters']) {
                for (viewer in data['data']['chatters'][group]) {
                    viewers.push(data['data']['chatters'][group][viewer]);
                }
            }
            console.log('resolving ' + viewers.length + ' viewers')
            resolveViewers = []
            for (var i = 0, len = viewers.length; i < len; i++) {
                if (resolveViewers.length >= 10) {
                    getAvatars(resolveViewers);
                    resolveViewers = [];
                }
                resolveViewers.push(viewers[i]);
            }
        },
        type: 'GET'
    });
}

function sortAvatars() {
    avatars = avatars.sort(function (a, b) {
        return a[5] > b[5] ? 1 : -1;
    });
}

function getAvatars(usernames) {
    console.log(avatars.length);
    $.ajax({
        url: "/viewerlookup/",
        type: "POST",
        dataType: 'json',
        data: {'viewers': usernames},
        success: function (data) {
            // username, image url, current frame number, frame count, xcord, ycord, img
            for (returnedViewer in data) {
                generateAvatar(returnedViewer, data[returnedViewer]);
            }
        }
    });
};

function step() {
    frameCount++;
    if (frameCount < 5) {
        window.requestAnimationFrame(step);
        return;
    }
    updateResolution();
    frameCount = 0;
    for (i in avatars) {
        avatars[i][2]++;
        if (avatars[i][2] >= cycleLoop.length) {
            avatars[i][2] = 0;
        }
        drawFrame(avatars[i][6], avatars[i][2], 0, avatars[i][4], avatars[i][5]); // img, frame number, frame sequence, stage x coord, stage y coord
    }
    window.requestAnimationFrame(step);
}


// username, image url, current frame number, frame count, xcord, ycord, img

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


function getRandInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}