# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from scipy.ndimage import distance_transform_edt




def extract_bboxes(mask):
    """Compute bounding boxes from masks.
    mask: [height, width, num_instances]. Mask pixels are either 1 or 0.

    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([mask.shape[-1], 4], dtype=np.int32)
    for i in range(mask.shape[-1]):
        m = mask[:, :, i]
        # Bounding box.
        horizontal_indicies = np.where(np.any(m, axis=0))[0]
        vertical_indicies = np.where(np.any(m, axis=1))[0]
        if horizontal_indicies.shape[0]:
            x1, x2 = horizontal_indicies[[0, -1]]
            y1, y2 = vertical_indicies[[0, -1]]
            # x2 and y2 should not be part of the box. Increment by 1.
            x2 += 1
            y2 += 1
        else:
            # No mask for this instance. Might happen due to
            # resizing or cropping. Set bbox to zeros
            x1, x2, y1, y2 = 0, 0, 0, 0
        x1 = max(x1, 0)
        y1 = max(y1, 0)
        y2 = mask.shape[0] - 1 if y2 >= mask.shape[0] else y2
        x2 = mask.shape[1] - 1 if x2 >= mask.shape[1] else x2
        boxes[i] = np.array([y1, x1, y2, x2])
    return boxes.astype(np.int32)


def mask_to_onehot(mask, num_classes):
    """
    Convert a mask (H, W) to onehot (K, H, W).

    Args:
        mask (np.ndarray): Label mask with shape (H, W)
        num_classes (int): Number of classes.

    Returns:
        np.ndarray: Onehot mask with shape(K, H, W).
    """
    _mask = [mask == i for i in range(num_classes)]
    _mask = np.array(_mask).astype(np.uint8)
    return _mask


def onehot_to_binary_edge(mask, radius):
    """
    Convert a onehot mask (K, H, W) to a edge mask.

    Args:
        mask (np.ndarray): Onehot mask with shape (K, H, W)
        radius (int|float): Radius of edge.

    Returns:
        np.ndarray: Edge mask with shape(H, W).
    """
    if radius < 1:
        raise ValueError("`radius` should be greater than or equal to 1")
    num_classes = mask.shape[0]

    edge = np.zeros(mask.shape[1:])
    # pad borders
    mask = np.pad(mask, ((0, 0), (1, 1), (1, 1)), mode="constant", constant_values=0)
    for i in range(num_classes):
        dist = distance_transform_edt(mask[i, :]) + distance_transform_edt(
            1.0 - mask[i, :]
        )
        dist = dist[1:-1, 1:-1]
        dist[dist > radius] = 0
        edge += dist

    edge = np.expand_dims(edge, axis=0)
    edge = (edge > 0).astype(np.uint8)
    return edge


def mask_to_binary_edge(mask, radius, num_classes):
    """
    Convert a segmentic segmentation mask (H, W) to a binary edge mask(H, W).

    Args:
        mask (np.ndarray): Label mask with shape (H, W)
        radius (int|float): Radius of edge.
        num_classes (int): Number of classes.

    Returns:
        np.ndarray: Edge mask with shape(H, W).
    """
    mask = mask.squeeze()
    onehot = mask_to_onehot(mask, num_classes)
    return onehot_to_binary_edge(onehot, radius)


def savePalette(label, save_path):
    bin_colormap = np.random.randint(0, 255, (256, 3))  # 可视化的颜色
    bin_colormap[0, :] = [0, 0, 0]
    bin_colormap = bin_colormap.astype(np.uint8)
    visualimg = Image.fromarray(label, "P")
    palette = bin_colormap  # long palette of 768 items
    visualimg.putpalette(palette)
    visualimg.save(save_path, format="PNG")


def segMaskB2I(mask_path, save_path):
    """
    Convert a segmentic segmentation mask (H, W) to instances with different colors via edge detection

    Args:
        mask_path (str): mask_path
        save_path (str): save_path
    """
    img = np.asarray(Image.open(mask_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("src", img)
    cv2.waitKey()
    mask = np.zeros_like(img)
    results = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2_v = cv2.__version__.split(".")[0]
    contours = results[1] if cv2_v == "3" else results[0]  # 边界
    hierarchys = results[2] if cv2_v == "3" else results[1]  # 隶属信息
    areas = {i: cv2.contourArea(contours[i]) for i in range(len(contours))}
    sorted(areas.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)  # 面积升序
    # 开始填充
    color = 1
    for idx in areas:
        contour = contours[idx]
        hierarchy = hierarchys[0][idx]
        # print(hierarchy)
        if hierarchy[-1] == -1:  # 输入子轮廓
            cv2.fillPoly(mask, [contour], color)
            color += 1
        else:
            cv2.fillPoly(mask, [contour], 0)
    # 显示
    # cv2.drawContours(mask, contours, -1, (125,125,125), 1)
    # cv2.imshow('src',mask)
    # cv2.waitKey()
    _savePalette(mask, save_path)









if __name__ == "__main__":
    b = np.ones((30, 30))
    a = np.zeros(((128, 128)))
    a[30:60, 30:60] = b
    out = onehot_to_binary_edge(a[np.newaxis, :, :], 1).squeeze() * 255
    import cv2

    cv2.imshow("img", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
