# Copyright (c) OpenMMLab. All rights reserved.
import copy
import os.path as osp
import os
import numpy as np
from pathlib import Path
from .base_dataset import BaseDataset
from ..builder import DATASETS
from itertools import chain
import mmcv
import cv2
from core import compute_fp_matrix

def imshow_bboxes(img,
                  bboxes,
                  labels=None,
                  colors='green',
                  text_color='white',
                  thickness=1,
                  font_scale=0.5,
                  show=True,
                  win_name='',
                  wait_time=0,
                  out_file=None):
    """Draw bboxes with labels (optional) on an image. This is a wrapper of
    mmcv.imshow_bboxes.

    Args:
        img (str or ndarray): The image to be displayed.
        bboxes (ndarray): ndarray of shape (k, 4), each row is a bbox in
            format [x1, y1, x2, y2].
        labels (str or list[str], optional): labels of each bbox.
        colors (list[str or tuple or :obj:`Color`]): A list of colors.
        text_color (str or tuple or :obj:`Color`): Color of texts.
        thickness (int): Thickness of lines.
        font_scale (float): Font scales of texts.
        show (bool): Whether to show the image.
        win_name (str): The window name.
        wait_time (int): Value of waitKey param.
        out_file (str, optional): The filename to write the image.

    Returns:
        ndarray: The image with bboxes drawn on it.
    """

    # adapt to mmcv.imshow_bboxes input format
    bboxes = np.split(
        bboxes, bboxes.shape[0], axis=0) if bboxes.shape[0] > 0 else []
    if not isinstance(colors, list):
        colors = [colors for _ in range(len(bboxes))]
    colors = [mmcv.color_val(c) for c in colors]
    assert len(bboxes) == len(colors)

    img = mmcv.imshow_bboxes(
        img,
        bboxes,
        colors,
        top_k=-1,
        thickness=thickness,
        show=False,
        out_file=None)

    if labels is not None:
        if not isinstance(labels, list):
            labels = [labels for _ in range(len(bboxes))]
        assert len(labels) == len(bboxes)

        for bbox, label, color in zip(bboxes, labels, colors):
            if label is None:
                continue
            bbox_int = bbox[0, :4].astype(np.int32)
            # roughly estimate the proper font size
            text_size, text_baseline = cv2.getTextSize(label,
                                                       cv2.FONT_HERSHEY_DUPLEX,
                                                       font_scale, thickness)
            text_x1 = bbox_int[0]
            text_y1 = max(0, bbox_int[1] - text_size[1] - text_baseline)
            text_x2 = bbox_int[0] + text_size[0]
            text_y2 = text_y1 + text_size[1] + text_baseline
            cv2.rectangle(img, (text_x1, text_y1), (text_x2, text_y2), color,
                          cv2.FILLED)
            cv2.putText(img, label, (text_x1, text_y2 - text_baseline),
                        cv2.FONT_HERSHEY_DUPLEX, font_scale,
                        mmcv.color_val(text_color), thickness)

    if show:
        mmcv.imshow(img, win_name, wait_time)
    if out_file is not None:
        mmcv.imwrite(img, out_file)
    return img



def img2label_path(img_path):
    """Define label paths as a function of image paths."""
    sa, sb = f"{os.sep}images{os.sep}", "labels"
    return os.path.join(
        img_path.rsplit(sa, 1)[0], sb, img_path.rsplit(sa, 1)[1].rsplit(".", 1)[0] + ".txt"
    )


def read_txt(txt_path):
    """读取txt文件

    Args:
        txt_path: str, txt文件路径

    Returns:
        txt_data: list, txt文件内容
    """
    txt_file = open(txt_path, "r", encoding="UTF-8")
    txt_data = []
    for line in txt_file.readlines():
        txt_data.append(line.replace("\n", ""))

    return txt_data


@DATASETS.register_module()
class DetDataset(BaseDataset):
    """Base dataset.

    Args:
        data_prefix (str): the prefix of data path
        pipeline (list): a list of dict, where each element represents
            a operation defined in `mmcls.datasets.pipelines`
        ann_file (str | None): the annotation file. When ann_file is str,
            the subclass is expected to read from the ann_file. When ann_file
            is None, the subclass is expected to read according to data_prefix
        test_mode (bool): in train mode or test mode
    """


    def __init__(
        self,
        data_root,
        pipeline,
        ann_file=None,
        **kwargs,
    ):
        super(DetDataset, self).__init__(data_root, pipeline, ann_file,**kwargs)

    def _load_annotations(self):
        infos = []
        image_list = sorted(
            chain(*[Path(self.data_root).rglob(f"*{f}") for f in self.img_formats])
        )
        for img_path in image_list:
            print(img_path)
            label_path = img2label_path(str(img_path))
            boxes = read_txt(label_path)
            infos.append({"image_path": str(img_path), "boxes": boxes})
        return infos
    
    
    def show_result(self,results,out_dir,**kwargs):

        if isinstance(results, dict):
            results = [results]

        for result in results:
            pred = result['result'][0]
            boxes = pred[:,:4]
            image_path = result['image_path']
            img = cv2.imread(image_path)
            result = f'{out_dir}/{os.path.basename(image_path)}'
            imshow_bboxes(img,boxes,out_file=result,show=False)
    
    def evaluate(self,result,**kwargs):
        return 0