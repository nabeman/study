const canvas = document.getElementById("canvas");

canvas.addEventListener('pointermove', getMouse);
canvas.addEventListener('pointerdown', start);
canvas.addEventListener('pointerup', stop);
let screenlog = document.querySelector('#screen-log')
const ctx = canvas.getContext("2d");
const presenter = navigator.ink.requestPresenter({ presentationArea: canvas });
let move_cnt = 0;

//ペン先が触れているかどうかのフラグ
let FLAG = false;
let count = 1;
const style = { color:"black", diameter: 10 }
let x = 0;
let y = 0;

setInterval(() => {
    screenlog.innerText = `
            Screen X/Y: ${x}, ${y}
        `
    console.log(Date.now());
}, 16.6666)

async function getMouse(e){
    if(FLAG){
        x = e.screenX;
        y = e.screenY;

        const pointSize = 5;
        ctx.fillStyle = "black";
        ctx.fillRect(x, y, pointSize, pointSize);
    
        await presenter.updateInkTrailStartPoint(e, style);

        console.log(count);
        count++;
    }
}

function start(){
    FLAG = true;
}

function stop(){
    FLAG = false;
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
