
channel_cfg = dict(
    num_output_channels=14,
    dataset_joints=14,
    dataset_channel=[
        list(range(14)),
    ],
    inference_channel=list(range(14)),
)

# model settings
model = dict(
    type="YOLOv8Detector",
    weights=r'D:\project\CV-platform\val\models\yolov8\yolov8n.onnx',

)

data_cfg = dict(
    image_size=[128, 128],
)
img_norm_cfg = dict(
    mean=[255 * 0.485, 255 * 0.456, 255 * 0.406],
    std=[255 * 0.229, 255 * 0.224, 255 * 0.225],
    to_rgb=False,
)



val_pipeline = [
    dict(type="LoadImageFromFile"),
    #dict(type="Resize",size=(640,640)),
    #dict(type='Normalize', **img_norm_cfg),
    #dict(type="ImageToTensor",key='img')
]

test_pipeline = val_pipeline

data_root = "D:/project/CV-platform/val/coco128"
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=1,
    val_dataloader=dict(samples_per_gpu=4),
    test_dataloader=dict(samples_per_gpu=4),
    val=dict(
        type="DetDataset",
        ann_file=f"{data_root}/annotations",
        data_root=f"{data_root}",
        data_cfg=data_cfg,
        pipeline=val_pipeline,
       ## dataset_info={{_base_.dataset_info}},
    ),
    test=dict(
        type="DetDataset",
        ann_file=f"{data_root}/annotations",
        data_root=f"{data_root}",
        data_cfg=data_cfg,
        pipeline=test_pipeline,
        ##dataset_info={{_base_.dataset_info}},
    ),
)

runner = dict(type="TestRunner",work_dir='./temp')

hooks = [
     dict(type='ImageShowHook',by_step=False),
     dict(type='EvalHook',by_step=False)
]