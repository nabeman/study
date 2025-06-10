import cv2
import torch
import os
import sys
import numpy as np
import matplotlib

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

TEST = False

def main():
    img = cv2.imread("app/testimage1.jpg")
    
    if TEST:
        print("test")
        cv2.line(img, (760, 1600), (960, 1600), (255, 0, 0), thickness=3)
        cv2.line(img, (810, 1650), (1010, 1650), (255, 0, 0), thickness=3)
        cv2.line(img, (760, 1600), (810, 1650), (255, 0, 0), thickness=3)
        cv2.line(img, (960, 1600), (1010, 1650), (255, 0, 0), thickness=3)
        
        cv2.line(img, (760, 1800), (960, 1800), (255, 0, 0), thickness=3)
        cv2.line(img, (810, 1850), (1010, 1850), (255, 0, 0), thickness=3)
        cv2.line(img, (760, 1800), (810, 1850), (255, 0, 0), thickness=3)
        cv2.line(img, (960, 1800), (1010, 1850), (255, 0, 0), thickness=3)

        cv2.line(img, (760, 1600), (760, 1800), (255, 0, 0), thickness=3)
        cv2.line(img, (810, 1650), (810, 1850), (255, 0, 0), thickness=3)
        cv2.line(img, (960, 1600), (960, 1800), (255, 0, 0), thickness=3)
        cv2.line(img, (1010, 1650), (1010, 1850), (255, 0, 0), thickness=3)
    else:
        depth = model.infer_image(img)
        z_s = depth[1600, 960]
        z_e = depth[2000, 960]
        start = screen_to_camera(960, 1600, z_s*10000)
        end = screen_to_camera(960, 2000, z_e*10000)
        print(z_s, z_e)
        start = [int(start[0]), int(start[1])]
        end = [int(end[0]), int(end[1])]
        cv2.line(img, start, end, (255, 0, 0), thickness=2)
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def screen_to_camera(x_screen, y_screen, z):
    _fx, _fy = K[0, 0], K[1, 1]
    _cx, _cy = K[0, 2], K[1, 2]

    # カメラ座標への変換
    x_camera = (x_screen - _cx) * z / _fx
    y_camera = (y_screen - _cy) * z / _fy
    return np.array([x_camera, y_camera])

# 焦点距離
f = 5
w_mm = 1 / (1.73 * 25.4) # イメージセンササイズ 1/1.73 インチ, 1インチ = 25.4mm
fx = f * (960/w_mm)
fy = f * (1280/w_mm)
# fy = fx

# 光学中心距離
cx = 960
cy = 1280
# カメラ行列
K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])

if __name__ == "__main__":
    main()
