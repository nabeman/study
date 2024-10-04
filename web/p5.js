// https://editor.p5js.org/

let x = 300;
let y = 300;

let targetX;
let targetY;

let stroke_list = []

const MOVERANGE = 5

function setup() {
  createCanvas(1000, 1000);
  background(220);
//   noStroke();
}

function draw() {
  // background(220);
  // circle(x, y, 100)
  
  if(mouseIsPressed){
    x = x + (mouseX - targetX);
    y = y + (mouseY - targetY);
    
    strokeWeight(5);
    line(targetX, targetY, mouseX, mouseY);
    stroke_list.push([targetX, targetY, mouseX, mouseY]);

    targetX = mouseX;
    targetY = mouseY;
  }else{
    targetX = mouseX;
    targetY = mouseY;
  }
  
  if(keyIsPressed){
    let temporary_list = []
    switch(key){
      case "a":
        background(220);
        break;
      
      case "z":
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0], stroke_list[i][1], stroke_list[i][2], stroke_list[i][3]);
        }
        break;
      
      case "ArrowDown":
        background(220);
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0], stroke_list[i][1] + MOVERANGE, stroke_list[i][2], stroke_list[i][3] + MOVERANGE);
          temporary_list.push([stroke_list[i][0], stroke_list[i][1] + MOVERANGE, stroke_list[i][2], stroke_list[i][3] + MOVERANGE]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
        
      case "ArrowUp":
        background(220);
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0], stroke_list[i][1] - MOVERANGE, stroke_list[i][2], stroke_list[i][3] - MOVERANGE);
          temporary_list.push([stroke_list[i][0], stroke_list[i][1] - MOVERANGE, stroke_list[i][2], stroke_list[i][3] - MOVERANGE]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
        
      case "ArrowLeft":
        background(220);
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0] - MOVERANGE, stroke_list[i][1], stroke_list[i][2] - MOVERANGE, stroke_list[i][3]);
          temporary_list.push([stroke_list[i][0] - MOVERANGE, stroke_list[i][1], stroke_list[i][2] - MOVERANGE, stroke_list[i][3]]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
      
      case "ArrowRight":
        background(220);
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0] + MOVERANGE, stroke_list[i][1], stroke_list[i][2] + MOVERANGE, stroke_list[i][3]);
          temporary_list.push([stroke_list[i][0] + MOVERANGE, stroke_list[i][1], stroke_list[i][2] + MOVERANGE, stroke_list[i][3]]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
      
      default:
        break;
    }
  }
}