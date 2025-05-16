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

def main():
    
    while True:
        ret, img = cap.read()

        # 深度画像の取得
        depth = model.infer_image(img)

        depth_color = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
        depth_color = depth_color.astype(np.uint8)
        # カラー化
        depth_color = (cmap(depth_color)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)

        cv2.imshow("Video", depth_color)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()