let x = 300;
let y = 300;

let targetX;
let targetY;

function setup() {
  createCanvas(1000, 1000);
  background(220);
//   noStroke();
}

function draw() {
  // background(220);
  circle(x, y, 100)
  
  if(mouseIsPressed){
    x = x + (mouseX - targetX);
    y = y + (mouseY - targetY);
    
    // strokeWeight(10);
    // line(targetX, targetY, mouseX, mouseY);

    targetX = mouseX;
    targetY = mouseY;
  }else{
    targetX = mouseX;
    targetY = mouseY;
  }
}