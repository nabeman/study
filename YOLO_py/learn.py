from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(data="./original_set/data.yaml", epochs=100)
metrics = model.val()
