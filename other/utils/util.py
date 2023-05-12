# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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

import os
import warnings
import cv2
import numpy as np
import torch



def get_files(root_path):
    res = []
    for root, dirs, files in os.walk(root_path, followlinks=True):
        for f in files:
            if f.endswith(('.jpg', '.png', '.jpeg', 'JPG')):
                res.append(os.path.join(root, f))
    return res


def get_image_list(image_path):
    """Get image list"""
    valid_suffix = [
        '.JPEG', '.jpeg', '.JPG', '.jpg', '.BMP', '.bmp', '.PNG', '.png'
    ]
    image_list = []
    image_dir = None
    if os.path.isfile(image_path):
        image_dir = None
        if os.path.splitext(image_path)[-1] in valid_suffix:
            image_list.append(image_path)
        else:
            image_dir = os.path.dirname(image_path)
            with open(image_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if len(line.split()) > 1:
                        raise RuntimeError(
                            'There should be only one image path per line in `image_path` file. Wrong line: {}'
                            .format(line))
                    image_list.append(os.path.join(image_dir, line))
    elif os.path.isdir(image_path):
        image_dir = image_path
        for root, dirs, files in os.walk(image_path):
            for f in files:
                if '.ipynb_checkpoints' in root:
                    continue
                if os.path.splitext(f)[-1] in valid_suffix:
                    image_list.append(os.path.join(root, f))
        image_list.sort()
    else:
        raise FileNotFoundError(
            '`image_path` is not found. it should be an image file or a directory including images'
        )

    if len(image_list) == 0:
        raise RuntimeError('There are not image file in `image_path`')

    return image_list, image_dir


def mkdir(path):
    sub_dir = os.path.dirname(path)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)







class VideoWriter:
    """
    Video writer.

    Args:
        path (str): The path to save a video.
        fps (int): The fps of the saved video.
        frame_size (tuple): The frame size (width, height) of the saved video.
        is_color (bool): Whethe to save the video in color format.
    """

    def __init__(self, path, fps, frame_size, is_color=True):
        self.is_color = is_color

        ppmatting.utils.mkdir(path)
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.cap_out = cv2.VideoWriter(
            filename=path,
            fourcc=fourcc,
            fps=fps,
            frameSize=frame_size,
            isColor=is_color)

    def write(self, frames):
        """ 
        Save frames.

        Args:
            frames(Tensor|numpy.ndarray): If `frames` is a tensor, it's shape should be like [N, C, H, W].
                If it is a ndarray, it's shape should be like [H, W, 3] or [H, W]. The value is in [0, 1].
        """
        if isinstance(frames, torch.Tensor):
            if frames.ndim != 4:
                raise ValueError(
                    'The frames should have the shape like [N, C, H, W], but it is {}'.
                    format(frames.shape))
            n, c, h, w = frames.shape
            if not (c == 1 or c == 3):
                raise ValueError(
                    'the channels of frames should be 1 or 3, but it is {}'.
                    format(c))
            if c == 1 and self.is_color:
                frames = frames.repeat(1,3,1,1)

            frames = (frames.permute(
                (0, 2, 3, 1)).numpy() * 255).astype('uint8')
            for i in range(n):
                frame = frames[i]
                self.cap_out.write(frame)
        else:
            frames = (frames * 255).astype('uint8')
            self.cap_out.write(frames)

    def release(self):
        self.cap_out.release()