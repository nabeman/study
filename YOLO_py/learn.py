from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(data="./original_set4/data.yaml", epochs=300)
metrics = model.val()
