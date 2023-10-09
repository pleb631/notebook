# Copyright (c) OpenMMLab. All rights reserved.
import copy
from typing import Optional

from mmcv import Registry

WRUNNERS = Registry('Wrunner')


def build_runner_constructor(cfg: dict):
    return WRUNNERS.build(cfg)


def build_runner(cfg: dict):

    runner = build_runner_constructor(cfg)
    return runner
