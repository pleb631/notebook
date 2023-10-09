import onnxruntime
from .yolov8_utils import prepare_input, process_output
import numpy as np
from ..builder import DETECTORS
from ..base import BaseDetector

@DETECTORS.register_module()
class YOLOv8Detector(BaseDetector):
    def __init__(self,
                 weights,
                 use_onnx=True,
                 use_cuda=False,
                 **kwargs):
        super(YOLOv8Detector, self).__init__(**kwargs)

        self.use_onnx = use_onnx
        self.device = 'cuda' if use_cuda else 'cpu'
     # Load Model
        self.model = self.load_model(use_cuda, weights)


    def load_model(self, use_cuda, weights, fp16=False):
        # Load onnx
        if self.use_onnx:
            if use_cuda:
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            else:
                providers = ['CPUExecutionProvider']

            model = onnxruntime.InferenceSession(weights, providers=providers)
        return model

    def forward_pred(self,img,**kwargs):
        result = self.forward(img)
        #kwargs["result"] = result
        return  result
    def forward_val(self):
        pass
    
    def forward(self, image: np.ndarray,
               input_shape: tuple = (640, 640),
               conf_thres: float = 0.25,
               iou_thres: float = 0.45,
               max_det: int = 1000,
               filter_classes: bool = None,
               agnostic_nms: bool = True,
               ):

        # Preprocess input image and also copying original image for later use
        original_image = image.copy()
        processed_image = prepare_input(
            image, input_shape, 32, False if self.use_onnx else True)

        # Perform Inference on the Image
        if self.use_onnx:
            # Run ONNX model
            input_name = self.model.get_inputs()[0].name
            prediction = self.model.run([self.model.get_outputs()[0].name], {
                input_name: processed_image})[0]
            
        # Run Coreml model   
        detection = []
        
        # Postprocess prediction
        detection = process_output(prediction,
                                    original_image.shape[:2],
                                    processed_image.shape[2:],
                                    conf_thres,
                                    iou_thres,
                                    agnostic=agnostic_nms,
                                    max_det=max_det)

        image_info = {
            'width': original_image.shape[1],
            'height': original_image.shape[0],
        }

        
        return detection, image_info
        

if __name__ == "__main__":
    
        
    import cv2
    from draw import draw_boxes
    im = cv2.imread(r'resources\test2.jpg')
    Detector= YOLOv8Detector(r'myModel\yolov8\yolov8n.onnx')
    detection, image_info = Detector.detect(im)
    
    if detection is not None: 
        bbox_xyxy = detection[:, :4]
        scores = detection[:, 4]
        class_ids = detection[:, 5]
        im = draw_boxes(im, bbox_xyxy, class_ids=class_ids)
    print(detection)
    cv2.imshow('im',im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()