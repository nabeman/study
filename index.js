document.addEventListener('mousemove', getMouse);
let screenlog = document.querySelector('#screen-log')

let x = 0;
let y = 0;

// getTimeStamp();

function getMouse(e){
    x = e.screenX;
    y = e.screenY;

    screenlog.innerText = `
        Screen X/Y: ${e.screenX}, ${e.screenY}
    `

    console.log("x:" + x + "  y:" + y );
}

const cameraWidth = 300;
const cameraHeight = 400;

const cameraInit = () => {
    const video = document.getElementById("camera");

    const cameraSetting = {
        audio: false,
        video: {
            width: cameraWidth,
            height: cameraHeight,
            facingMode: "environment",
        }
    }

    navigator.mediaDevices.getUserMedia(cameraSetting)
        .then((mediaStream) => {
            video.srcObject = mediaStream;
        })
        .catch((err) => {
            console.log(err.toString());
        });
}
// setInterval(() => {
//     console.log("x:" + x + "  y:" + y );
// }, 500);

// function getTimeStamp(){
//     let time = Date.now();

//     console.log("x:" + x + "  y:" + y + "  time:" + time);

//     requestAnimationFrame(getTimeStamp);
// }
