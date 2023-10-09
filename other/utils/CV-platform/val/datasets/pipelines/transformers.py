# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp

import mmcv
import numpy as np
import cv2


from ..builder import PIPELINES


@PIPELINES.register_module()
class Resize(object):
    """Resize images.

    Args:
        size (int | tuple): Images scales for resizing (h, w).
            When size is int, the default behavior is to resize an image
            to (size, size). When size is tuple and the second value is -1,
            the image will be resized according to adaptive_side. For example,
            when size is 224, the image is resized to 224x224. When size is
            (224, -1) and adaptive_size is "short", the short side is resized
            to 224 and the other side is computed based on the short side,
            maintaining the aspect ratio.
        interpolation (str): Interpolation method. For "cv2" backend, accepted
            values are "nearest", "bilinear", "bicubic", "area", "lanczos". For
            "pillow" backend, accepted values are "nearest", "bilinear",
            "bicubic", "box", "lanczos", "hamming".
            More details can be found in `mmcv.image.geometric`.
        adaptive_side(str): Adaptive resize policy, accepted values are
            "short", "long", "height", "width". Default to "short".
        backend (str): The image resize backend type, accepted values are
            `cv2` and `pillow`. Default: `cv2`.
    """

    def __init__(self,
                 size,
                 interpolation='bilinear',
                 adaptive_side='short',
                 backend='cv2'):
        assert isinstance(size, int) or (isinstance(size, tuple)
                                         and len(size) == 2)
        assert adaptive_side in {'short', 'long', 'height', 'width'}

        self.adaptive_side = adaptive_side
        self.adaptive_resize = False
        if isinstance(size, int):
            assert size > 0
            size = (size, size)
        else:
            assert size[0] > 0 and (size[1] > 0 or size[1] == -1)
            if size[1] == -1:
                self.adaptive_resize = True
        if backend not in ['cv2', 'pillow']:
            raise ValueError(f'backend: {backend} is not supported for resize.'
                             'Supported backends are "cv2", "pillow"')
        if backend == 'cv2':
            assert interpolation in ('nearest', 'bilinear', 'bicubic', 'area',
                                     'lanczos')
        else:
            assert interpolation in ('nearest', 'bilinear', 'bicubic', 'box',
                                     'lanczos', 'hamming')
        self.size = size
        self.interpolation = interpolation
        self.backend = backend

    def _resize_img(self, results):
        for key in results.get('img_fields', ['img']):
            img = results[key]
            ignore_resize = False
            if self.adaptive_resize:
                h, w = img.shape[:2]
                target_size = self.size[0]

                condition_ignore_resize = {
                    'short': min(h, w) == target_size,
                    'long': max(h, w) == target_size,
                    'height': h == target_size,
                    'width': w == target_size
                }

                if condition_ignore_resize[self.adaptive_side]:
                    ignore_resize = True
                elif any([
                        self.adaptive_side == 'short' and w < h,
                        self.adaptive_side == 'long' and w > h,
                        self.adaptive_side == 'width',
                ]):
                    width = target_size
                    height = int(target_size * h / w)
                else:
                    height = target_size
                    width = int(target_size * w / h)
            else:
                height, width = self.size
            if not ignore_resize:
                img = mmcv.imresize(
                    img,
                    size=(width, height),
                    interpolation=self.interpolation,
                    return_scale=False,
                    backend=self.backend)
                results[key] = img
                results['img_shape'] = img.shape

    def __call__(self, results):
        self._resize_img(results)
        return results

    def __repr__(self):
        repr_str = self.__class__.__name__
        repr_str += f'(size={self.size}, '
        repr_str += f'interpolation={self.interpolation})'
        return repr_str


    
@PIPELINES.register_module()
class ImageToTensor:
    """Convert image to :obj:`torch.Tensor` by given keys.

    The dimension order of input image is (H, W, C). The pipeline will convert
    it to (C, H, W). If only 2 dimension (H, W) is given, the output would be
    (1, H, W).

    Args:
        keys (Sequence[str]): Key of images to be converted to Tensor.
    """

    def __init__(self, keys):
        self.keys = keys

    def __call__(self, results):
        """Call function to convert image in results to :obj:`torch.Tensor` and
        permute the channel order.

        Args:
            results (dict): Result dict contains the image data to convert.

        Returns:
            dict: The result dict contains the image converted
                to :obj:`torch.Tensor` and permuted to (C, H, W) order.
        """
        for key in self.keys:
            img = results[key]
            if len(img.shape) < 3:
                img = np.expand_dims(img, -1)
            results[key] = img.transpose(2, 0, 1)
        return results

    def __repr__(self):
        return self.__class__.__name__ + f'(keys={self.keys})'
    
    
    
    
@PIPELINES.register_module()
class Normalize:
    """Normalize the image.

    Added key is "img_norm_cfg".

    Args:
        mean (sequence): Mean values of 3 channels.
        std (sequence): Std values of 3 channels.
        to_rgb (bool): Whether to convert the image from BGR to RGB,
            default is true.
    """

    def __init__(self, mean, std, to_rgb=True):
        self.mean = np.array(mean, dtype=np.float32)
        self.std = np.array(std, dtype=np.float32)
        self.to_rgb = to_rgb

    def __call__(self, results):
        """Call function to normalize images.

        Args:
            results (dict): Result dict from loading pipeline.

        Returns:
            dict: Normalized results, 'img_norm_cfg' key is added into
                result dict.
        """
        for key in results.get('img_fields', ['img']):
            results[key] = mmcv.imnormalize(results[key], self.mean, self.std,
                                            self.to_rgb)
        results['img_norm_cfg'] = dict(
            mean=self.mean, std=self.std, to_rgb=self.to_rgb)
        return results

    def __repr__(self):
        repr_str = self.__class__.__name__
        repr_str += f'(mean={self.mean}, std={self.std}, to_rgb={self.to_rgb})'
        return repr_str