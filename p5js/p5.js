// https://editor.p5js.org/
let x = 300;
let y = 300;

let targetX;
let targetY;

let stroke_list = []

const MOVERANGE = 5
const PLUS_RATIO = 0.07;
const MINUS_RATIO = 0.07;
const THETA = 2;
const canvas = document.getElementById("canvas")

function setup() {
  createCanvas(window.innerWidth, window.innerHeight, canvas);
  frameRate(120)
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
        clear();
        break;
      
      case "z":
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0], stroke_list[i][1], stroke_list[i][2], stroke_list[i][3]);
        }
        break;
      
      case "ArrowDown":
        clear();
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0], stroke_list[i][1] + MOVERANGE, stroke_list[i][2], stroke_list[i][3] + MOVERANGE);
          temporary_list.push([stroke_list[i][0], stroke_list[i][1] + MOVERANGE, stroke_list[i][2], stroke_list[i][3] + MOVERANGE]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
        
      case "ArrowUp":
        clear();
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0], stroke_list[i][1] - MOVERANGE, stroke_list[i][2], stroke_list[i][3] - MOVERANGE);
          temporary_list.push([stroke_list[i][0], stroke_list[i][1] - MOVERANGE, stroke_list[i][2], stroke_list[i][3] - MOVERANGE]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
        
      case "ArrowLeft":
        clear();
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0] - MOVERANGE, stroke_list[i][1], stroke_list[i][2] - MOVERANGE, stroke_list[i][3]);
          temporary_list.push([stroke_list[i][0] - MOVERANGE, stroke_list[i][1], stroke_list[i][2] - MOVERANGE, stroke_list[i][3]]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
      
      case "ArrowRight":
        clear();
        for(let i = 0; i < stroke_list.length; i++){
          line(stroke_list[i][0] + MOVERANGE, stroke_list[i][1], stroke_list[i][2] + MOVERANGE, stroke_list[i][3]);
          temporary_list.push([stroke_list[i][0] + MOVERANGE, stroke_list[i][1], stroke_list[i][2] + MOVERANGE, stroke_list[i][3]]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        break;
      
      case "-":
        clear();
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
        clear();
        //重心を求める center of gravitiy(cog)
        for(let i = 0; i < stroke_list.length; i++){
          let center_x = (stroke_list[i][0] + stroke_list[i][2]) / 2;
          let center_y = (stroke_list[i][1] + stroke_list[i][3]) / 2;
          center_point = [center_point[0] + center_x, center_point[1] + center_y];
        }
        cog = [center_point[0] / stroke_list.length, center_point[1] / stroke_list.length];
        console.log(cog)

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
        
      case "r":
        clear();
        rad = THETA * (Math.PI / 180)
        //ストロークの中心を求める
        for(let i = 0; i < stroke_list.length; i++){
          let center_x = (stroke_list[i][0] + stroke_list[i][2]) / 2;
          let center_y = (stroke_list[i][1] + stroke_list[i][3]) / 2;
          center_point = [center_point[0] + center_x, center_point[1] + center_y];
        }
        cog = [center_point[0] / stroke_list.length, center_point[1] / stroke_list.length];
        
        //原点に移動させる
        for(let i = 0; i < stroke_list.length; i++){
            let x_1 = stroke_list[i][0] - cog[0];
            let y_1 = stroke_list[i][1] - cog[1];
          
            let x_2 = stroke_list[i][2] - cog[0];
            let y_2 = stroke_list[i][3] - cog[1];
          
            // let rotate_matrix = [[Math.cos(rad), -Math.sin(rad)],[Math.sin(rad), Math.cos(rad)]];
            let rx_1 = (x_1 * Math.cos(rad) - y_1 * Math.sin(rad)) + cog[0];
            let ry_1 = (x_1 * Math.sin(rad) + y_1 * Math.cos(rad)) + cog[1];
            let rx_2 = (x_2 * Math.cos(rad) - y_2 * Math.sin(rad)) + cog[0];
            let ry_2 = (x_2 * Math.sin(rad) + y_2 * Math.cos(rad)) + cog[1];
          
            line(rx_1, ry_1, rx_2, ry_2);
            // console.log([x_1, y_1, x_2, y_2])
            temporary_list.push([rx_1, ry_1, rx_2, ry_2]);
        }
        stroke_list = temporary_list;
        temporary_list = [];
        center_point = [0, 0];
        break;
        
      case "e":
        clear();
        rad = -THETA * (Math.PI / 180)
        //ストロークの中心を求める
        for(let i = 0; i < stroke_list.length; i++){
          let center_x = (stroke_list[i][0] + stroke_list[i][2]) / 2;
          let center_y = (stroke_list[i][1] + stroke_list[i][3]) / 2;
          center_point = [center_point[0] + center_x, center_point[1] + center_y];
        }
        cog = [center_point[0] / stroke_list.length, center_point[1] / stroke_list.length];
        
        //原点に移動させる
        for(let i = 0; i < stroke_list.length; i++){
            let x_1 = stroke_list[i][0] - cog[0];
            let y_1 = stroke_list[i][1] - cog[1];
          
            let x_2 = stroke_list[i][2] - cog[0];
            let y_2 = stroke_list[i][3] - cog[1];
          
            // let rotate_matrix = [[Math.cos(rad), -Math.sin(rad)],[Math.sin(rad), Math.cos(rad)]];
            let rx_1 = (x_1 * Math.cos(rad) - y_1 * Math.sin(rad)) + cog[0];
            let ry_1 = (x_1 * Math.sin(rad) + y_1 * Math.cos(rad)) + cog[1];
            let rx_2 = (x_2 * Math.cos(rad) - y_2 * Math.sin(rad)) + cog[0];
            let ry_2 = (x_2 * Math.sin(rad) + y_2 * Math.cos(rad)) + cog[1];
          
            line(rx_1, ry_1, rx_2, ry_2);
            // console.log([x_1, y_1, x_2, y_2])
            temporary_list.push([rx_1, ry_1, rx_2, ry_2]);
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