canvas.addEventListener('pointermove', getMouse);
canvas.addEventListener('pointerdown', start);
canvas.addEventListener('pointerup', stop);

const btn = document.getElementById("btn");
const startbtn = document.getElementById("start");

btn.addEventListener("click", change);
startbtn.addEventListener("click", getTime);

let screenlog = document.querySelector('#screen-log')
const ctx = canvas.getContext("2d");
let count = 0;
let RATE = 16.6666666666666
//ペン先が触れているかどうかのフラグ
let FLAG = false;
const style = { color:"black", diameter: 10 }
let x = 0;
let y = 0;
let json = []

setInterval(() => {
    screenlog.innerText = `
            Screen X/Y: ${x}, ${y}
        `
    if(FLAG && (x != 0 && y != 0)){
        const pointSize = 5;
        ctx.fillStyle = style.color;
        ctx.fillRect(x, y, pointSize, pointSize);
        json.push({"x": x, "y": y, "time":Time()});
        console.log({"x": x, "y": y, "time":Time()});
    };
}, RATE);

function getMouse(e){
    if(FLAG){
        x = e.pageX;
        y = e.pageY;
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

function getTime(){
    console.log(Date.now());
    eel.Capture();
}

eel.expose(MakeJson);
function MakeJson(){
    const fileName = "test.json";
    const link = document.createElement("a");
    link.href = "data:text/plain," + encodeURIComponent(JSON.stringify(json));
    link.download = fileName;
    link.click();
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
