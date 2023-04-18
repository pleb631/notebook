


def get_kwargs_name(**kwargs):
    prefix = []
    for k, v in kwargs.items():
        if isinstance(v, list):
            v = [str(l) for l in v]
            prefix += v
        else:
            prefix.append(str(v))
    prefix = "_".join(prefix)
    return prefix


def jujge():
    str = "hello world"
    print(str.isalnum()) # 判断所有字符都是数字或者字母
    print(str.isalpha()) # 判断所有字符都是字母
    print(str.isdigit()) # 判断所有字符都是数字
    print(str.islower()) # 判断所有字符都是小写
    print(str.isupper()) # 判断所有字符都是大写
    print(str.istitle()) # 判断所有单词都是首字母大写，像标题
    print(str.isspace()) # 判断所有字符都是空白字符、\t、\n、\r


def preprocess(image_path, mean=[0.485*255, 0.456*255, 0.406*255], std = [0.229*255, 0.224*255, 0.225*255]):
    original_image = cv2.imread(image_path)
    # the model expects RGB inputs
    original_image = original_image[:, :, ::-1]

    if not isinstance(mean, np.ndarray):
        mean = np.array(mean)
    if not isinstance(std, np.ndarray):
        std = np.array(std)
    if mean.ndim == 1:
        mean = np.reshape(mean, (1, 1,-1))
    if std.ndim == 1:
        std = np.reshape(std, (1, 1,-1))

    img = np.subtract(img, mean)  # i.e. arrays = _div - mean
    img = np.divide(img, std)
    img = img[:, :, ::-1]

    #img = img.astype("float32").transpose(2, 0, 1)[np.newaxis]  # (1, 3, h, w)
    return img



import torch
def convert_ndarray_to_tensor(state_dict: dict):
    """
    In-place convert all numpy arrays in the state_dict to torch tensor.

    Args:
        state_dict (dict): a state-dict to be loaded to the model.
    """
    # model could be an OrderedDict with _metadata attribute
    # (as returned by Pytorch's state_dict()). We should preserve these
    # properties.
    for k in list(state_dict.keys()):
        v = state_dict[k]
        if not isinstance(v, np.ndarray) and not isinstance(
                v, torch.Tensor
        ):
            raise ValueError(
                "Unsupported type found in checkpoint! {}: {}".format(
                    k, type(v)
                )
            )
        if not isinstance(v, torch.Tensor):
            state_dict[k] = torch.from_numpy(v)