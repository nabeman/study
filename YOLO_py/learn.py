from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolo11n.pt")
    model.train(data="./original_set4/data.yaml", epochs=100)
    metrics = model.val()
