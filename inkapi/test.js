const ctx = canvas.getContext("2d");
const presenter = navigator.ink.requestPresenter({ presentationArea: canvas });
let style = { color: "black", diameter: 10 };
let aaa = false;


canvas.addEventListener("pointermove", (evt) => {
    if(aaa){
        const pointSize = 5;
        ctx.fillStyle = style.color;
        ctx.fillRect(evt.pageX, evt.pageY, pointSize, pointSize);
    }

});

window.addEventListener("pointerdown", () =>{
    aaa = true;
});

window.addEventListener("pointerup", () => {
    aaa = false;
})

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;