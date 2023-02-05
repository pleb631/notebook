# -*- coding: utf-8 -*-
#!/usr/bin/python
#test_copyfile.py

import os,shutil,glob,cv2
import pathlib

def get_images_list(image_dir, postfix=['*.jpg'], basename=False):
    '''
    获得文件列表
    :param image_dir: 图片文件目录
    :param postfix: 后缀名，可是多个如，['*.jpg','*.png']
    :param basename: 返回的列表是文件名（True），还是文件的完整路径(False)
    :return:
    '''
    images_list = []
    for format in postfix:
        image_format = os.path.join(image_dir, format)
        image_list = glob.glob(image_format)
        if not image_list == []:
            images_list += image_list
    images_list = sorted(images_list)
    if basename:
        images_list = get_basename(images_list)
    return images_list


def get_basename(file_list):
    """
    get files basename
    :param file_list:
    :return:
    """
    dest_list = []
    for file_path in file_list:
        basename = os.path.basename(file_path)
        dest_list.append(basename)
    return dest_list


def draw_img(img, box, clr, message):
    '''Draw bounding box on image'''
    x1, y1, x2, y2 = map(int, box) # map appley the first parameter function to the second parameter
    cv2.rectangle(img, (x1,y1), (x2,y2), clr, 1)
    cv2.putText(img, message, (x1-10,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, clr, 1)
    return img