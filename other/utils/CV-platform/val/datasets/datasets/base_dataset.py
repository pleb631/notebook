# Copyright (c) OpenMMLab. All rights reserved.
import copy
import os.path as osp
from abc import ABCMeta, abstractmethod
from os import PathLike
from typing import List
import cv2
import os

import mmcv
import numpy as np
from torch.utils.data import Dataset
from ..pipelines import Compose

def expanduser(path):
    if isinstance(path, (str, PathLike)):
        return osp.expanduser(path)
    else:
        return path


class BaseDataset(Dataset, metaclass=ABCMeta):
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

    CLASSES = None

    def __init__(self,
                 data_root,
                 pipeline,
                 ann_file=None,
                 **kwargs,):
        super(BaseDataset, self).__init__()
        self.img_formats=['.jpg','.png','jpeg']
        self.data_root = expanduser(data_root)
        self.pipeline = Compose(pipeline)
        self.ann_file = expanduser(ann_file)
        self.data_infos = self._load_annotations()
        

    @abstractmethod
    def _load_annotations(self):
        pass

    def prepare_data(self, idx):
        results = copy.deepcopy(self.data_infos[idx])
        return self.pipeline(results)
    
    def __len__(self):
        return len(self.data_infos)

    def __getitem__(self, idx):
        return self.prepare_data(idx)
    
    


