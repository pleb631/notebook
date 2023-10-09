# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp
import platform
import shutil
import time
import warnings
from typing import Any, Dict, List, Optional, Tuple

import torch
from torch.utils.data import DataLoader

import mmcv
from .base_runner import BaseRunner
from .builder import WRUNNERS


@WRUNNERS.register_module()
class TestRunner(BaseRunner):
    """Epoch-based Runner.

    This runner train models epoch by epoch.
    """

    def run_iter(self, data_batch: Any, test_mode: bool, **kwargs) -> None:

        outputs = self.model.val_step(data_batch, self.optimizer, **kwargs)
        if not isinstance(outputs, dict):
            raise TypeError('"batch_processor()" or "model.train_step()"'
                            'and "model.val_step()" must return a dict')
        # if 'log_vars' in outputs:
        #     self.log_buffer.update(outputs['log_vars'], outputs['num_samples'])
        self.outputs = outputs


    @torch.no_grad()
    def val(self, data_loader, model,**kwargs):
        self.model = model
        self.mode = 'val'
        self.data_loader = data_loader
        self.call_hook('before_val_epoch')
        time.sleep(2)  # Prevent possible deadlock during epoch transition
        prog_bar = mmcv.ProgressBar(len(self.data_loader))
        
        for data_batch in self.data_loader:
            self.data_batch = data_batch
            self.call_hook('before_val_iter')
            result = self.model.forward_pred(**self.data_batch)
            self.data_batch['result'] = result
            self.results.append(self.data_batch)
            
            self.call_hook('after_val_iter')         
            # batch_size = len(next(iter(data_batch.values())))
            # for _ in range(batch_size):
            prog_bar.update()
        #self.data_loader.show_result(self.results)
        self.call_hook('after_val_epoch')

    def run(self,
            data_loaders: List[DataLoader],
            **kwargs) -> None:
        """Start running.

        Args:
            data_loaders (list[:obj:`DataLoader`]): Dataloaders for training
                and validation.
            workflow (list[tuple]): A list of (phase, epochs) to specify the
                running order and epochs. E.g, [('train', 2), ('val', 1)] means
                running 2 epochs for training and 1 epoch for validation,
                iteratively.
        """
        #assert isinstance(data_loaders, list)



        self.call_hook('before_run')

        self.val(data_loaders, **kwargs)

        time.sleep(1)  # wait for some hooks like loggers to finish
        self.call_hook('after_run')

