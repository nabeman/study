from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(data="./original_set2/data.yaml", epochs=300)
metrics = model.val()
