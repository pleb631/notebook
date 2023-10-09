# Copyright (c) OpenMMLab. All rights reserved.
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

class BaseDetector(metaclass=ABCMeta):
    """Base class for pose detectors.

    All recognizers should subclass it.
    All subclass should overwrite:
        Methods:`forward_val`, supporting to forward when validating.
        Methods:`forward_pred`, supporting to forward when predicting.

    Args:
        backbone (dict): Backbone modules to extract feature.
        head (dict): Head modules to give output.
        train_cfg (dict): Config for training. Default: None.
        test_cfg (dict): Config for testing. Default: None.
    """

    @abstractmethod
    def forward_val(self, img, img_metas, **kwargs):
        """Defines the computation performed at training."""

    @abstractmethod
    def forward_pred(self, img, img_metas, **kwargs):
        """Defines the computation performed at testing."""

    @abstractmethod
    def forward(self, img, img_metas, **kwargs):
        """Forward function."""

    # @staticmethod
    # def _parse_losses(losses):
    #     """Parse the raw outputs (losses) of the network.

    #     Args:
    #         losses (dict): Raw output of the network, which usually contain
    #             losses and other necessary information.

    #     Returns:
    #         tuple[Tensor, dict]: (loss, log_vars), loss is the loss tensor \
    #             which may be a weighted sum of all losses, log_vars \
    #             contains all the variables to be sent to the logger.
    #     """
    #     log_vars = OrderedDict()
    #     for loss_name, loss_value in losses.items():
    #         if isinstance(loss_value, torch.Tensor):
    #             log_vars[loss_name] = loss_value.mean()
    #         elif isinstance(loss_value, float):
    #             log_vars[loss_name] = loss_value
    #         elif isinstance(loss_value, list):
    #             log_vars[loss_name] = sum(_loss.mean() for _loss in loss_value)
    #         else:
    #             raise TypeError(
    #                 f'{loss_name} is not a tensor or list of tensors or float')

    #     loss = sum(_value for _key, _value in log_vars.items()
    #                if 'loss' in _key)

    #     log_vars['loss'] = loss
    #     for loss_name, loss_value in log_vars.items():
    #         # reduce loss when distributed training
    #         if not isinstance(loss_value, float):
    #             if dist.is_available() and dist.is_initialized():
    #                 loss_value = loss_value.data.clone()
    #                 dist.all_reduce(loss_value.div_(dist.get_world_size()))
    #             log_vars[loss_name] = loss_value.item()
    #         else:
    #             log_vars[loss_name] = loss_value

    #     return loss, log_vars



