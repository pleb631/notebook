
```bash
!pip install timm
```

查询模型

```python
model_list = timm.list_models()
print(len(model_list), model_list[:3])
# Results 541 ['adv_inception_v3', 'botnet26t_256', 'botnet50ts_256']
```

查看有预训练参数的模型

```bash
model_pretrain_list = timm.list_models(pretrained=True)
print(len(model_pretrain_list), model_pretrain_list[:3])
# Results：396 ['adv_inception_v3', 'cait_m36_384', 'cait_m48_448']
```

检索特定模型，采用模糊查询，如resnet系列

```bash
model_resnet = timm.list_models('*resnet*')
print(len(model_resnet), model_resnet[:3])
# Results: 117 ['cspresnet50', 'cspresnet50d', 'cspresnet50w']
```

创建模型

```bash
import torch
x = torch.randn([1, 3, 224, 224])
model_resnet50 = timm.create_model('resnet50', pretrained=True)
out = model_resnet50(x)
print(out.shape)
# Results: torch.Size([1, 1000])

```

改变输出类别

```bash
model_resnet50_finetune = timm.create_model('resnet50', pretrained=True, num_classes=10)
out = model_resnet50_finetune (x)
print(out.shape)
# Results: torch.Size([1, 10])

```

改变输入通道数，通过out_indices参数指定从哪个level获取feature

```bash
# 通道数改变后，对应的权重参数会进行相应的处理，此处不作详细说明，
#可参照：https://fastai.github.io/timmdocs/models或直接查看源代码
feature_extractor = timm.create_model('resnet50', in_chans=1, features_only=True, out_indices=[1, 3, 4])

```
