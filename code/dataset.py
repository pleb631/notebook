import glob
import cv2
import shutil
import random
import numpy as np

from functools import reduce
from .FileUtils import *
from .ImageVideoUtils import *
from .Convertion import is_xyxy_valid

def filter_similar_image(image_dir_path, save_image_dir_path, threshold=5):
    '''感知哈希算法去除相似图像。如果不相同的数据位小于等于5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片。
    每张图片计算哈希值，计算两两图像的汉明距离，记录小于阈值的图像对，遍历删除相似图像，得到最终需要保留的图像，保存在同级目录'filtered_images/'下

    Args:
        image_dir_path: str, 需要进行筛选的图像路径
        save_image_dir_path: str, 筛选过的图像保存路径
        threshold: int, 汉明距离阈值
    '''
    # 计算图像哈希值
    def avhash(image):
        if not isinstance(image, Image.Image):
            image = Image.open(image)
        image = image.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, image.getdata()) / 64.
        return reduce(lambda x, y_z : x | y_z[1] << y_z[0], enumerate(map(lambda i: 0 if i < avg else 1, image.getdata())), 0)

    # 计算哈希值汉明距离
    def hamming(h1, h2):
        h, d = 0, h1 ^ h2
        while d:
            h += 1
            d &= d - 1
        return h

    image_names = glob.glob(f'{image_dir_path}/*.jpg')

    print('Caculating hash value of images...')
    image_hash_list = []
    for index, image_name in enumerate(image_names):
        print(index, image_name)
        if not is_valid_jpg(image_name):
            image_names.remove(image_name)
            continue
        h_value = avhash(image_name)
        image_hash_list.append((image_name, h_value))

    print('Caculating hamming distance...')
    hamming_list = np.zeros(shape=(len(image_hash_list), len(image_hash_list)))
    for index_i in range(len(image_hash_list)):
        for index_j in range(index_i + 1, len(image_hash_list)):
            hamming_list[index_i, index_j] = hamming(image_hash_list[index_i][1], image_hash_list[index_j][1])

    print('Deleting duplicates')
    remaining_list = image_names.copy()
    for index_i in range(len(image_hash_list)):
        for index_j in range(index_i + 1, len(image_hash_list)):
            if hamming_list[index_i, index_j] <= threshold and (image_hash_list[index_j][0] in remaining_list):
                print('delete %d %s' % (index_j, image_hash_list[index_j][0]))
                remaining_list.remove(image_hash_list[index_j][0])

    print('Copying remaining images...')
    for index in range(len(remaining_list)):
        print('keep %s' % (remaining_list[index]))
        os.makedirs(save_image_dir_path, exist_ok=True)
        print(remaining_list[index], os.path.join(save_image_dir_path, os.path.basename(remaining_list[index])))
        shutil.copyfile(remaining_list[index], os.path.join(save_image_dir_path, os.path.basename(remaining_list[index])))


