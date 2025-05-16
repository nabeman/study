from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("../runs/detect/train4/weights/best.pt")

    # results = model("images/pen_touch.jpg", save=True)
    results = model(0, show = True)

    for i in enumerate(results):
        print(i)