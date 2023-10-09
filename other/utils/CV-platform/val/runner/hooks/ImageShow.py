# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp
import warnings
from typing import Callable, List, Optional, Union
import os
import shutil

from .hook import HOOKS, Hook


@HOOKS.register_module()
class ImageShowHook(Hook):
    def __init__(
        self,
        by_step: bool = True,
        show_iters: int = 1,
        out_dir: str = None,
    ) -> None:
        self.by_step = by_step
        self.show_iters = show_iters
        self.out_dir = out_dir

    def before_run(self, runner):
        if not self.out_dir:
            self.out_dir = runner.work_dir
        self.out_dir = osp.join(self.out_dir,'pred')
        if osp.exists(self.out_dir):
            shutil.rmtree(self.out_dir)
        os.makedirs(self.out_dir,exist_ok=True)

    def after_val_iter(self, runner):
        if not self.by_step:
            return 0
        runner.data_loader.show_result(
            results=runner.data_batch, out_dir=self.out_dir
        )
    
    def after_val_epoch(self, runner):
        if self.by_step:
            return 0
        runner.data_loader.show_result(
            results=runner.results, out_dir=self.out_dir
        )
