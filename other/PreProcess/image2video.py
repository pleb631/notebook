# -*- coding: utf-8 -*-

import os
import sys
import glob
from tqdm import tqdm
import argparse
import numpy as np
import cv2


def img2video(image_dir, output_dir, fps):
    img_list = os.listdir(image_dir)

    # height, width, channels
    img_shape = cv2.imread(os.path.join(image_dir, img_list[0])).shape[:2]
    print(img_shape)

    # Define the codec and create VideoWriter object

    #fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    ##                                                                                   cv2.Size=(width, height)
    videoWriter = cv2.VideoWriter(os.path.join(output_dir, 'output.avi'), fourcc, fps, (img_shape[1], img_shape[0]))

    for i in tqdm(img_list):
        filename = os.path.join(image_dir, i)
        # print(filename)
        img = cv2.imread(filename)
        if img is None:
            continue
        # print(img.shape)
        videoWriter.write(img)

    # Release everything if job is finished
    videoWriter.release()


