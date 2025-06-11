import cv2
import torch
import os
import sys
import numpy as np
import matplotlib

# YOLO
from ultralytics import YOLO

sys.path.append(os.getcwd())

from depth_anything_v2.dpt import DepthAnythingV2

cmap = matplotlib.colormaps.get_cmap('Spectral_r')

encoder = 'vits'

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

model = DepthAnythingV2(**{**model_configs[encoder]})
model.load_state_dict(torch.load(f"depth_anything_v2_{encoder}.pth", map_location = "cpu"))
model = model.to(DEVICE).eval()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def main():
    yolo_model = YOLO("../runs/detect/train7/weights/best.pt")
    tip_point = []
    touch_flag = False
    # mask = None
    while True:
        ret, img = cap.read()
        # new_mask = np.zeros((img.shape[0], img.shape[1]))
        # 深度画像の取得
        depth = model.infer_image(img)

        results = yolo_model(img, stream = True)
        x1, y1, x2, y2 = [], [], [], []
        pen_x, pen_y = None
        for r in results:
            classes = r.boxes.cls.to('cpu').detach().numpy().copy()
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
        
        if not x1 == []: #ペン先が検出された場合ペン先周りの深度のばらつき(標準偏差)を計算
            std = np.std(depth[(int(y1)-30):(int(y2)+30), (int(x1)-30):(int(x2)+30)])
            if std < 0.4: # ペン先が接触していた場合 (深度のばらつきが閾値以下)
                touch_flag = True
            else:
                touch_flag = False   
        else:
            touch_flag = False

        # ペン先の座標をストロークごとに保存する処理, 深度も保存
        if touch_flag:
            if len(tip_point) != 0:
                tip_point[len(tip_point)-1].append([int(x2), int(y2), depth[int(y2), int(x2)]+1])
            else:
                tip_point.append([])
                tip_point[0].append([int(x2), int(y2), depth[int(y2), int(x2)]+1])
        else:
            if len(tip_point) != 0:
                tip_point.append([])
        
        # ストロークの描画
        for i in tip_point:
            if len(i) > 1: #接触点が2つ以上保存された場合
                for j in range(len(i)-1):
                    if i[j][2] > depth[i[j][1], i[j][0]]:
                        cv2.line(img, (i[j][0], i[j][1]), (i[j+1][0], i[j+1][1]), (255, 0, 0), thickness=1)
            elif len(i) == 1:
                cv2.circle(img, (i[0][0], i[0][1]), 1, (255, 0, 0), thickness=1)

        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            tip_point = []

if __name__ == "__main__":
    main()


# 接触判定とペン先検出は独立させる
# 接触(p) -> 非接触(q) -> 接触(r)となる場合
# pr間に線は引かない

# 接触を細かくしてみる
# 閾値は0.4 これを細かくして変化を確かめる
# 簡単に変化を確認するためのインタフェースを実装してもいいかも

# スマホで動くかどうかを確かめる

# ペン先を誤認識した場合の処理
# 精度を上げる
# 接触判定処理

# 実験
# メモ帳的な使い勝手、文字入力機能？、他の手書き文字アプリとの差を調べる、GoogleKeepみたいなやつ、
# UI、実行速度、ユースケース、

# やること
# 1. ペン先検出の精度を上げる
# 2. 誤認識に対する処理  
# 3. 机に張り付く、固定されるような表示方法
# 4. オクルージョンの実装 ok
# 5. 軌跡に深度情報を付与 ok

# 軌跡に深度情報を付与（始点と終点）

# android用にKotlin/Javaを使って書き換える、Unity, Kyveも試す？
# DepthAnything と OpenCVをKotlinを使って書く
# Android Studioを試す
# Pythonコードをもとに書き換える