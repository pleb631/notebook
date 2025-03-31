# Copyright (c) OpenMMLab. All rights reserved.
# This file add snake case alias for coco api

import warnings

import pycocotools
from pycocotools.coco import COCO as _COCO
from pycocotools.cocoeval import COCOeval as _COCOeval
import cv2
import numpy as np
class COCO(_COCO):
    """This class is almost the same as official pycocotools package.

    It implements some snake case function aliases. So that the COCO class has
    the same interface as LVIS class.
    """

    def __init__(self, annotation_file=None):
        if getattr(pycocotools, '__version__', '0') >= '12.0.2':
            warnings.warn(
                'mmpycocotools is deprecated. Please install official pycocotools by "pip install pycocotools"',  # noqa: E501
                UserWarning)
        super().__init__(annotation_file=annotation_file)
        self.img_ann_map = self.imgToAnns
        self.cat_img_map = self.catToImgs

    def get_ann_ids(self, img_ids=[], cat_ids=[], area_rng=[], iscrowd=None):
        return self.getAnnIds(img_ids, cat_ids, area_rng, iscrowd)

    def get_cat_ids(self, cat_names=[], sup_names=[], cat_ids=[]):
        return self.getCatIds(cat_names, sup_names, cat_ids)

    def get_img_ids(self, img_ids=[], cat_ids=[]):
        return self.getImgIds(img_ids, cat_ids)

    def load_anns(self, ids):
        return self.loadAnns(ids)

    def load_cats(self, ids):
        return self.loadCats(ids)

    def load_imgs(self, ids):
        return self.loadImgs(ids)

CLASSES = ('person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
               'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
               'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
               'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
               'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
               'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
               'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
               'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
               'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
               'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
               'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
               'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush')

if __name__=='__main__':
    import os
    import shutil
    gt = '/project/data/COCO/data'
    os.makedirs(os.path.join(gt,'img'),exist_ok=True)
    os.makedirs(os.path.join(gt,'gt'),exist_ok=True)
    imgroot = '/project/data/COCO/train2017/'
    coco =COCO('/project/data/COCO/annotations/instances_train2017.json')
    ids = coco.getCatIds('person')[0]
    imgIds = coco.catToImgs[ids]
    for i in range(len(imgIds)):
        imgInfo = coco.loadImgs(imgIds[i])[0]
        filename = imgInfo['file_name']
        print(filename)
        annIds = coco.getAnnIds(imgIds=imgInfo['id'])
        anns = coco.loadAnns(annIds)
        num=0
        mask = None
        for ann in anns:
            if ann['category_id']!=ids:
                continue
            if ann['iscrowd']==1 or ann['area'] <4000:
                continue
            num+=1 
            if type(mask)!=np.ndarray:
                mask = coco.annToMask(ann) 
            else:
                mask[coco.annToMask(ann)>0.5]=num
        if type(mask)==np.ndarray:
            #mask = mask*255    
            cv2.imwrite(os.path.join(gt,'gt',filename.split('.')[0]+'.png'),mask)
            shutil.copy(os.path.join(imgroot,filename),os.path.join(gt,'img',filename))
        
        
        
        
