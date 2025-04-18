import cv2
import torch
import os
import numpy as np
import matplotlib

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

# raw_img = cv2.imread("C:\\Users\\tkmco\\study\\Depth-Anything-V2\\images\\image1.jpg")
raw_img = cv2.imread("./images/image2.jpg")
# with torch.no_grad():
depth = model.infer_image(raw_img)

depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
depth = depth.astype(np.uint8)
# カラー化
depth = (cmap(depth)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)

depth = cv2.resize(depth, None, fx=0.5, fy=0.5)

if len(depth.shape) == 3:
# 各ピクセルがグレースケールかどうかを確認
    if np.all(depth[:,:,0] == depth[:,:,1]) and np.all(depth[:,:,1] == depth[:,:,2]):
        print('この画像はグレースケールです。')
    else:
        print('この画像はカラー画像です。')
else:
    print('この画像は既にグレースケールです。')

cv2.imshow('depth', depth)
cv2.waitKey(0)
cv2.destroyAllWindows()
    # cv2.imwrite('result.jpg', depth)