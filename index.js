canvas.addEventListener('pointermove', getMouse);
canvas.addEventListener('pointerdown', start);
canvas.addEventListener('pointerup', stop);
const btn = document.getElementById("btn");
btn.addEventListener("click", change);
let screenlog = document.querySelector('#screen-log')
const ctx = canvas.getContext("2d");
let count = 0;
let RATE = 33.33333333333
//ペン先が触れているかどうかのフラグ
let FLAG = false;
const style = { color:"black", diameter: 10 }
let x = 0;
let y = 0;

setInterval(() => {
    screenlog.innerText = `
            Screen X/Y: ${x}, ${y}
        `
    if(FLAG && (x != 0 && y != 0)){
        const pointSize = 5;
        ctx.fillStyle = style.color;
        ctx.fillRect(x, y, pointSize, pointSize);
        console.log({"x": x, "y": y, "time":Time()});
        console.log(count);
        count++;
    }
}, RATE)

function getMouse(e){
    if(FLAG){
        x = e.pageX;
        y = e.pageY;

        // console.log(count);
        // count++;
    }
}

function start(){
    FLAG = true;
}

function stop(){
    FLAG = false;
}

function Time(){
    let ret;
    const now = Date.now();
    const msec = now % 1000;
    const sec = Math.floor(now/1000) % 60;
    const min = Math.floor(now/1000/60) & 60;
    const hours = Math.floor(now/1000/60/60) & 24;
    const days = Math.floor(now/1000/60/60/24);

    ret = String(hours) + ":" + String(min) + ":" + String(sec) + ":" + String(msec);
    return ret
}

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

function change(){
    const input = document.getElementById("rate");
    const tmp = input.Value;
    RATE = tmp;
}
// async function draw(){
//     const pointSize = 5;
//     ctx.fillStyle = "black";
//     ctx.fillRect(x, y, pointSize, pointSize);

//     await presenter.updateInkTrailStartPoint(evt, style);
// }

// const cameraWidth = 300;
// const cameraHeight = 400;

// const cameraInit = () => {
//     const video = document.getElementById("camera");

//     const cameraSetting = {
//         audio: false,
//         video: {
//             width: cameraWidth,
//             height: cameraHeight,
//             facingMode: "environment",
//         }
//     }

//     navigator.mediaDevices.getUserMedia(cameraSetting)
//         .then((mediaStream) => {
//             video.srcObject = mediaStream;
//         })
//         .catch((err) => {
//             console.log(err.toString());
//         });
// }
