from ultralytics import YOLO
import numpy

if __name__ == "__main__":
    model = YOLO("../runs/detect/train7/weights/best.pt")

    results = model(0, stream = True)
    for r in results:
        classes = r.boxes.cls.to('cpu').detach().numpy().copy()
        x1, y1, x2, y2 = [], [], [], []
        pen_x, pen_y = None
        if 0 in classes: 
            for box, class_id in zip(r.boxes.xyxy, r.boxes.cls):
                class_name = r.names[int(class_id)]
                count = 0
                if class_name == "tip":
                    x1.append(box[0].item())
                    y1.append(box[1].item())
                    x2.append(box[2].item())
                    y2.append(box[3].item())
                elif class_name == "pen":
                    pen_x = (box[0].item() + box[2].item()) / 2
                    pen_y = box[3].item()
        if len(x1) > 1:
            distance_list = [None, None]
            for i in range(len(x1)):
                tip_center_x = (x1[i] + x2[i]) / 2
                tip_center_y = (y1[i] + y2[i]) / 2
                distance = (pen_x - tip_center_x) ** 2 + (pen_y - tip_center_y) ** 2
                if distance_list[0] == None or distance_list[0] > distance:
                    distance_list = [distance, i]
            x1 = x1[distance_list[1]]
            y1 = y1[distance_list[1]]
            x2 = x2[distance_list[1]]
            y2 = y2[distance_list[1]]




