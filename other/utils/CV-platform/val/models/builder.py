# Copyright (c) OpenMMLab. All rights reserved.
from mmcv.cnn import MODELS as MMCV_MODELS
from mmcv.cnn import build_model_from_cfg
from mmcv.utils import Registry

MODELS = Registry(
    'models', build_func=build_model_from_cfg, parent=MMCV_MODELS)

DETECTORS = MODELS



def build_detector(cfg):
    """Build backbone."""
    return DETECTORS.build(cfg)

