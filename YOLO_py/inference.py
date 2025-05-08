from ultralytics import YOLO

model = YOLO("../runs/detect/train/weights/best.pt")

results = model("images/pen_touch.jpg", save=True)

for i in enumerate(results):
    print(i)