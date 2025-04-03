from ultralytics import YOLO

model = YOLO("../runs/detect/train3/weights/best.pt")

results = model("temp/pen_sample.mp4", save=True)

for i in enumerate(results):
    print(i)