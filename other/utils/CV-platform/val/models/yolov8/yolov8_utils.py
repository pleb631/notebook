import cv2
import numpy as np
from ultralytics.yolo.utils import ops
import torch


def prepare_input(image, input_shape, stride, pt):
    input_tensor = LetterBox(input_shape, auto=pt, stride=stride)(img=image)
    input_tensor = input_tensor.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    input_tensor = np.ascontiguousarray(input_tensor).astype(np.float32)  # contiguous
    input_tensor /= 255.0  # 0 - 255 to 0.0 - 1.0
    input_tensor = input_tensor[None].astype(np.float32)
    return input_tensor





class LetterBox:
    """Resize image and padding for detection, instance segmentation, pose."""

    def __init__(self, new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, stride=32):
        """Initialize LetterBox object with specific parameters."""
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.stride = stride

    def __call__(self,img=None):
        """Return updated labels and image with added border."""
        shape = img.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not self.scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if self.auto:  # minimum rectangle
            dw, dh = np.mod(dw, self.stride), np.mod(dh, self.stride)  # wh padding
        elif self.scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])

        dw /= 2  # divide padding into 2 sides
        dh /= 2
        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                 value=(114, 114, 114))  # add border

        return img
    
def process_output(detections, 
                   ori_shape, 
                   input_shape, 
                   conf_threshold, 
                   iou_threshold,
                   classes=None,
                   mlmodel=False,
                   agnostic=False,
                   max_det=300,
                   ):
    detections = torch.from_numpy(detections)
    detections = ops.non_max_suppression(detections,
                                          conf_thres=conf_threshold,
                                          iou_thres=iou_threshold,
                                          classes=classes,
                                          agnostic=agnostic,
                                          max_det=max_det,
                                          )



    for i in range(len(detections)): 
        # Extract boxes from predictions
        detections[i][:, :4] = ops.scale_boxes(input_shape, detections[i][:, :4], ori_shape).round()

    
    return detections[0].cpu().numpy()


def rescale_boxes(boxes, ori_shape, input_shape):

    input_height, input_width = input_shape
    img_height, img_width = ori_shape
    # Rescale boxes to original image dimensions
    input_shape = np.array(
        [input_width, input_height, input_width, input_height])
    boxes = np.divide(boxes, input_shape, dtype=np.float32)
    boxes *= np.array([img_width, img_height, img_width, img_height])
    return boxes
