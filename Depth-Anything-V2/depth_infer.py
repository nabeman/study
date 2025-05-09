import cv2
import torch
import os
import numpy as np
import matplotlib
import time

from depth_anything_v2.dpt import DepthAnythingV2
from record import Record

cmap = matplotlib.colormaps.get_cmap('Spectral_r')

encoder = 'vits'

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

start1 = time.perf_counter()
model = DepthAnythingV2(**{**model_configs[encoder]})
middle3 = time.perf_counter()
model.load_state_dict(torch.load(f"depth_anything_v2_{encoder}.pth", map_location = "cpu"))
middle4 = time.perf_counter()
model = model.to(DEVICE).eval()
# to(DEVICE): デバイス(GPU/CPU)を切り替える
# eval: 評価モードに切り替え
middle1 = time.perf_counter()
print("ライブラリの読み込み: {}".format(middle3 - start1))
print("モデルのロード: {}".format(middle4 - middle3))
print("デバイスの切り替え: {}".format(middle1 - middle4))
print("middle1までの実行時間: {}".format(middle1 - start1))

# raw_img = cv2.imread("C:\\Users\\tkmco\\study\\Depth-Anything-V2\\images\\image1.jpg")
raw_img = cv2.imread("./images/testimages/maue_25.jpg")
# with torch.no_grad():
middle2 = time.perf_counter()
print("middle2までの実行時間: {}".format(middle2 - middle1))

start = time.perf_counter()
depth = model.infer_image(raw_img)
end = time.perf_counter()
print("実行時間: {}".format(end - start))

depth_color = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
depth_color = depth_color.astype(np.uint8)
# カラー化
depth_color = (cmap(depth_color)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)

depth_color = cv2.resize(depth_color, None, fx=0.25, fy=0.25)

# if len(depth_color.shape) == 3:
# # 各ピクセルがグレースケールかどうかを確認
#     if np.all(depth_color[:,:,0] == depth_color[:,:,1]) and np.all(depth_color[:,:,1] == depth_color[:,:,2]):
#         print('この画像はグレースケールです。')
#     else:
#         print('この画像はカラー画像です。')
# else:
#     print('この画像は既にグレースケールです。')

# print(depth_color.shape)
depth = cv2.resize(depth, None, fx=0.25, fy=0.25)
def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(depth_color[x, y])
        print(x, y)
        print(depth[y, x])

# Record(317, 269, depth)
end1 = time.perf_counter()
print("最後の部分の実行時間: {}".format(end1 - end))
print("全体の実行時間: {}".format(end1 - start1))

cv2.imshow('depth', depth_color)
cv2.setMouseCallback('depth', onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()
    # cv2.imwrite('result.jpg', depth)