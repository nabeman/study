// https://editor.p5js.org/

let x = 300;
let y = 300;

let targetX;
let targetY;

let stroke_list = []

const MOVERANGE = 5
const PLUS_RATIO = 0.1;
const MINUS_RATIO = 0.1;

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
    let center_point = [0, 0];
    let cog = [];
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
      
      case "-":
        background(200);
        //重心を求める center of gravitiy(cog)
        for(let i = 0; i < stroke_list.length; i++){
          let center_x = (stroke_list[i][0] + stroke_list[i][2]) / 2;
          let center_y = (stroke_list[i][1] + stroke_list[i][3]) / 2;
          center_point = [center_point[0] + center_x, center_point[1] + center_y];
        }
        cog = [center_point[0] / stroke_list.length, center_point[1] / stroke_list.length];

        for(let i = 0; i < stroke_list.length; i++){
          let x_1 = stroke_list[i][0] + (cog[0] - stroke_list[i][0]) * (MINUS_RATIO);
          let y_1 = stroke_list[i][1] + (cog[1] - stroke_list[i][1]) * (MINUS_RATIO);
          
          let x_2 = stroke_list[i][2] + (cog[0] - stroke_list[i][2]) * (MINUS_RATIO);
          let y_2 = stroke_list[i][3] + (cog[1] - stroke_list[i][3]) * (MINUS_RATIO);
          
          line(x_1, y_1, x_2, y_2);
          temporary_list.push([x_1, y_1, x_2, y_2]);
        }

        stroke_list = temporary_list;
        temporary_list = [];
        center_point = [0, 0]
        break;
      
      case ";":
        background(200);
        //重心を求める center of gravitiy(cog)
        for(let i = 0; i < stroke_list.length; i++){
          let center_x = (stroke_list[i][0] + stroke_list[i][2]) / 2;
          let center_y = (stroke_list[i][1] + stroke_list[i][3]) / 2;
          center_point = [center_point[0] + center_x, center_point[1] + center_y];
        }
        cog = [center_point[0] / stroke_list.length, center_point[1] / stroke_list.length];

        for(let i = 0; i < stroke_list.length; i++){
          let x_1 = stroke_list[i][0] - (cog[0] - stroke_list[i][0]) * (PLUS_RATIO);
          let y_1 = stroke_list[i][1] - (cog[1] - stroke_list[i][1]) * (PLUS_RATIO);
          
          let x_2 = stroke_list[i][2] - (cog[0] - stroke_list[i][2]) * (PLUS_RATIO);
          let y_2 = stroke_list[i][3] - (cog[1] - stroke_list[i][3]) * (PLUS_RATIO);
          
          line(x_1, y_1, x_2, y_2);
          temporary_list.push([x_1, y_1, x_2, y_2]);
        }

        stroke_list = temporary_list;
        temporary_list = [];
        center_point = [0, 0];
        break;
        
      default:
        break;
    }
  }
}