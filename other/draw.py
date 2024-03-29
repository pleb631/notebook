from PIL import Image
import numpy as np
import cv2





def centerize(
    src,
    shape,
    cval=None,
    return_mask=False,
    interpolation="linear",
    loc="center",
):
    """Centerize image for specified image size
    #等比例缩放和扩边至指定大小
    Parameters
    ----------
    src: numpy.ndarray
        Image to centerize
    shape: tuple of int
        Image shape (height, width) or (height, width, channel)
    cval: int or float or numpy.ndarray
        Color to be filled in the blank.
    return_mask: numpy.ndarray
        Mask for centerized image.
    interpolation: str
        Interpolation method (default: 'linear').
    loc: str
        Location of image ('center', 'lt', 'rb'). (default: 'center')

    Returns
    -------
    dst: numpy.ndarray
        Centerized image.

    """
    if src.shape[:2] == shape[:2]:
        if return_mask:
            return src, np.ones(shape[:2], dtype=bool)
        else:
            return src

    if len(shape) != src.ndim:
        shape = list(shape) + [src.shape[2]]

    dst = np.zeros(shape, dtype=src.dtype)
    if cval:
        dst[:, :] = cval

    src_h, src_w = src.shape[:2]
    scale_h, scale_w = 1.0 * shape[0] / src_h, 1.0 * shape[1] / src_w
    scale = min(scale_h, scale_w)
    dst_h, dst_w = int(round(src_h * scale)), int(round(src_w * scale))
    src = cv2.resize(src, (dst_w, dst_h), interpolation=cv2.INTER_NEAREST)

    ph, pw = 0, 0
    h, w = src.shape[:2]
    dst_h, dst_w = shape[:2]
    if loc == "center":
        if h < dst_h:
            ph = (dst_h - h) // 2
        if w < dst_w:
            pw = (dst_w - w) // 2
    elif loc == "lt":
        ph = 0
        pw = 0
    elif loc == "rb":
        if h < dst_h:
            ph = dst_h - h
        if w < dst_w:
            pw = dst_w - w
    else:
        raise ValueError("Unsupported loc: {}".format(loc))
    dst[ph : ph + h, pw : pw + w] = src

    if return_mask:
        mask = np.zeros(shape[:2], dtype=bool)
        mask[ph : ph + h, pw : pw + w] = True
        return dst, mask
    else:
        return dst
    



def mask_to_bbox(masks):
    bboxes = np.zeros((len(masks), 4), dtype=float)
    for i, mask in enumerate(masks):
        if mask.sum() == 0:
            continue
        where = np.argwhere(mask)
        (y1, x1), (y2, x2) = where.min(0), where.max(0) + 1
        bbox = y1, x1, y2, x2
        bboxes[i] = bbox
    return bboxes