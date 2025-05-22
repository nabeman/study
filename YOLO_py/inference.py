from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("../runs/detect/train7/weights/best.pt")

    # results = model("images/pen_touch.jpg", save=True)
    results = model(0, show=True, stream=True)

    for r in results:
        for box, class_id in zip(r.boxes.xyxy, r.boxes.cls):
            class_name = r.names[int(class_id)]
            if class_name == "tip":
                print(f"Box coordinates: {box}, Object: {class_name}")
                aaa = box[0].item()
                print(f"coordinates: {aaa}")
    
        # print("cls: {}, xyxy: {}, xywh: {}, class_names: {}".format(r.boxes.cls, r.boxes.xyxy, r.boxes.xywh, r.names))
    # for i in enumerate(results):
    #     print(i)