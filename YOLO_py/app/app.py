from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("../runs/detect/train7/weights/best.pt")

    results = model(0, stream = True)
    for r in results:
        for box, class_id in zip(r.boxes.xyxy, r.boxes.cls):
            class_name = r.names[int(class_id)]
            if class_name == "tip":
                x1 = box[0].item()
                y1 = box[1].item()
                x2 = box[2].item()
                y2 = box[3].item()


