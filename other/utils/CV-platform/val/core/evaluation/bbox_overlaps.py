import numpy as np




def box_iou(box1, box2, eps=1e-7, use_legacy_coordinate=False):
    extra_length = 0.0 if not use_legacy_coordinate else 1.0
    
    x11, y11, x12, y12 = np.split(box1, 4, axis=1)
    x21, y21, x22, y22 = np.split(box2, 4, axis=1)

    xa = np.maximum(x11, np.transpose(x21))
    xb = np.minimum(x12, np.transpose(x22))
    ya = np.maximum(y11, np.transpose(y21))
    yb = np.minimum(y12, np.transpose(y22))

    area_inter = np.maximum(0, (xb - xa + extra_length)) * np.maximum(
        0, (yb - ya + extra_length)
    )

    area_1 = (x12 - x11 + extra_length) * (y12 - y11 + extra_length)
    area_2 = (x22 - x21 + extra_length) * (y22 - y21 + extra_length)
    area_union = area_1 + np.transpose(area_2) - area_inter

    return area_inter / (area_union + eps)


def compute_fp_matrix(detections, labels):
    """
    Return correct prediction matrix
    Arguments:
        detections (array[N, 6]), x1, y1, x2, y2, conf, class
        labels (array[M, 5]), class, x1, y1, x2, y2
    Returns:
        correct (array[N, 10]), for 10 IoU levels
    """
    iouv = np.linspace(0.5, 0.95, 10)
    iou = box_iou(labels[:, 1:], detections[:, :4])
    correct = np.zeros((detections.shape[0], iouv.shape[0])).astype(bool)
    correct_class = labels[:, 0:1] == detections[:, 5]
    for i in range(len(iouv)):
        x = np.where(
            (iou >= iouv[i]) & correct_class
        )  # IoU > threshold and classes match
        if x[0].shape[0]:
            matches = np.concatenate(
                (np.stack(x, 1), iou[x[0], x[1]][:, None]), 1
            )  # [label, detect, iou]
            if x[0].shape[0] > 1:
                matches = matches[matches[:, 2].argsort()[::-1]]
                matches = matches[np.unique(matches[:, 1], return_index=True)[1]]
                # matches = matches[matches[:, 2].argsort()[::-1]]
                matches = matches[np.unique(matches[:, 0], return_index=True)[1]]
            correct[matches[:, 1].astype(int), i] = True
    return correct
