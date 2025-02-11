import cv2
import math
import glob
import os
import numpy as np
from PIL import Image
from pathlib import Path

from .FileUtils import *
from .Convertion import (
    quadrilateral_points2left_top_first_quadrilateral,
    xyxy2xywh
)
from functools import reduce


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global image_path

    if event == cv2.EVENT_LBUTTONDOWN:
        print(image_path)
        print(x, y)


def get_image_features(image, mode="cv2"):
    """获取图像的属性
    读取图像+获取属性总时间，PIL格式比opencv格式快4倍；如果只是获取分辨率，建议使用PIL格式

    Args:
        cv2_image: np.array, cv2读取的图像
        mode: str, 若为'cv2'，读取opencv格式的图像；若为'PIL'，读取PIL格式的图像高宽；若为'PIL_channel'，读取PIL格式的图像高宽及通道

    Returns:
        height: int, 图像高
        width: int, 图像宽
        channel: int, 图像通道数
    """
    if mode == "cv2":
        height, width, channel = image.shape
        return height, width, channel
    elif mode == "PIL":
        width, height = image.size
        return height, width
    elif mode == "PIL_channel":
        width, height = image.size
        channel = len(image.split())
        return height, width, channel


def fftCacul(img):
    """
    :param img: the input image
    :param isOccu: judge whether to occlusion of the current frame by
                    Gaussian mixture model background modeling
    :return: judge whether to occlusion of the current frame by FFT or backGround modeling
    """
    img_col = cv2.resize(img, (403, 226), interpolation=cv2.INTER_AREA)

    np.seterr(all="ignore")
    assert isinstance(img_col, np.ndarray), "img_col must be a numpy array"
    assert (
        img_col.ndim == 3
    ), "img_col must be a color image ({0} dimensions currently)".format(img_col.ndim)

    img_gry = cv2.cvtColor(img_col, cv2.COLOR_RGB2GRAY)
    rows, cols = img_gry.shape
    crow, ccol = rows // 2, cols // 2
    f = np.fft.fft2(img_gry)
    fshift = np.fft.fftshift(f)
    fshift[crow - 75 : crow + 75, ccol - 75 : ccol + 75] = 0
    f_ishift = np.fft.ifftshift(fshift)
    img_fft = np.fft.ifft2(f_ishift)
    img_fft = 20 * np.log(np.abs(img_fft))
    result = np.mean(img_fft)

    return img_fft, result


def is_valid_jpg(jpg_file_path):
    """判断JPG文件下载是否完整，筛选出保存一半中断的jpg图片

    Args:
        jpg_file_path: str, 需要判断的JPG文件路径

    Returns:
        bool, True则合法，False则非法
    """
    if os.path.getsize(jpg_file_path) == 0:
        return False
    elif jpg_file_path.split(".")[-1].lower() == "jpg":
        with open(jpg_file_path, "rb") as f:
            f.seek(-2, 2)
            f_end = f.read()
            return f_end == b"\xff\xd9"  # 判定jpg是否包含结束字段
    else:
        return False


def plt2cv(fig):
    """
    fig = plt.figure()
    image = fig2data(fig)
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    import PIL.Image as Image

    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    image = Image.frombytes("RGBA", (w, h), buf.tostring())
    image = np.asarray(image)
    return image


def point_in_mask(point, mask_image):
    """判断蒙版图像中指定点是否合法

    Args:
        point: list, 二维点坐标[x, y]
        mask_image: nparray, 蒙版灰度图

    Returns:
        bool, 若该点对应的像素值大于128，则合法；反之，不合法
    """
    if (
        point[0] < 0
        or point[0] >= mask_image.shape[1]
        or point[1] < 0
        or point[1] >= mask_image.shape[0]
    ):
        return False
    else:
        return mask_image[int(point[1]), int(point[0])] > 128


def gray2heatmap(image):
    """将灰度图转换为热力图

    Args:
        image: np.array, 灰度图

    Returns:
        heatmap: np.array, 热力图
    """
    norm_img = image.copy()
    cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    norm_img = 255 - norm_img

    heatmap = cv2.applyColorMap(norm_img, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    return heatmap


def depth2gray(depth_npy_path):
    """深度图转换为灰度图

    Args:
        depth_npy_path: str, 深度图路径

    Returns:
        norm_img: np.array, 灰度图
    """
    depth = np.load(depth_npy_path)
    depth[np.isnan(depth)] = np.nanmin(depth)
    depth[np.isinf(depth)] = np.nanmin(depth)
    norm_img = depth.copy()
    cv2.normalize(depth, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    # norm_img = 255 - norm_img
    # depth[depth==255] = 0

    return norm_img


def gen_mask_image(points_list, width, height):
    """根据连续顶点列表生成指定大小的蒙版图像

    Args:
        points_list: list, 顶点列表，顶点要按照顺时针或逆时针顺序排列好
        width: int, 蒙版图像的宽
        height: int, 蒙版图像的高

    Returns:
        mask_image: nparray, 生成的蒙版图像
    """
    mask_image = np.zeros((height, width, 3), dtype=np.uint8) * 255
    poly = np.array(points_list)
    cv2.fillPoly(mask_image, [poly], (255, 255, 255))

    return mask_image


def extend_box(bbox, extend_ratio_width, extend_ratio_height):
    """按extend_ratio对矩形进行扩边

    Args:
        bbox: list, 矩形框，格式[xmin, ymin, xmax, ymax]
        extend_ratio_width: float, 宽扩边比例。如0.4，则扩边1.4倍
        extend_ratio_height: float, 高扩边比例。如0.4，则扩边1.4倍

    Returns:
        extend_box: list, 矩形框，格式[xmin, ymin, xmax, ymax]
    """
    bbox_xywh_center = xyxy2xywh(bbox)
    bbox_xywh_center[2] = bbox_xywh_center[2] * (1 + extend_ratio_width)
    bbox_xywh_center[3] = bbox_xywh_center[3] * (1 + extend_ratio_height)

    return xywh2xyxy(bbox_xywh_center)


def crop_image_extend_border(image, bbox, extend_ratio_width=0, extend_ratio_height=0):
    """从图片中裁剪出一个矩形，按extend_ratio进行扩边

    Args:
        image: nparray, 需要裁剪的图像
        bbox: list, 矩形框，格式[xmin, ymin, xmax, ymax]
        extend_ratio_width: float, 宽扩边比例。如0.4，则扩边1.4倍
        extend_ratio_height: float, 高扩边比例。如0.4，则扩边1.4倍

    Returns:
        roi_img: nparray, 裁剪后的图片
    """
    height, width = image.shape[:2]
    bbox_xyxy = extend_box(bbox, extend_ratio_width, extend_ratio_height)

    return image[
        max(bbox_xyxy[1], 0) : min(bbox_xyxy[3], height),
        max(bbox_xyxy[0], 0) : min(bbox_xyxy[2], width),
    ]


def crop_rotated_box_image(image, rotated_box, size):
    """裁剪旋转矩形框

    Args:
        image: np.array, 图像
        rotated_box: list, 旋转矩形, [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    Returns:
        rotated_box_image: np.array, 裁剪后的图像
        size: tuple, 旋转行人框的尺寸(width, height)
    """
    rotated_box, size = np.int0(rotated_box), np.int0(size)
    (width, height) = size

    # 此方法cv2.boxPoints得到的顶点坐标不可控
    # 转换为最小外接矩形的（中心(x,y), (宽,高), 旋转角度）形式，得到其宽高
    # 旋转角度θ是水平轴（x轴）逆时针旋转，与碰到的矩形的第一条边的夹角。并且这个边的边长是width，另一条边边长是height。
    # min_area_rect = cv2.minAreaRect(rotated_box)
    # # width = int(min_area_rect[1][0])
    # # height = int(min_area_rect[1][1])
    # # 获取最小外接矩形的4个顶点坐标，坐标顺序为左下、左上、右上、右下
    # box = cv2.boxPoints(min_area_rect)
    # box = np.int0(box)

    # 旋转矩形框转换为左上角点为起始点，按顺时针排序的形式
    left_top_first_rotated_box = np.int0(
        quadrilateral_points2left_top_first_quadrilateral(
            rotated_box, mode="person_quad"
        )
    )

    # 做透视变换，将旋转矩形区域校正至矩形宽高区域
    src_image_points = left_top_first_rotated_box.astype("float32")
    dst_image_points = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype="float32",
    )
    return gen_perspective_image(
        image, src_image_points, dst_image_points, width, height
    )


def normalize(im, mean, std):
    im = im.astype(np.float32, copy=False) / 255.0
    im -= mean
    im /= std
    return im


# 定义一个函数，用于调整图像的长边大小，默认值为224
def resize_long(im, long_size=224, interpolation=cv2.INTER_LINEAR):
    # 计算图像的短边大小
    value = max(im.shape[0], im.shape[1])
    scale = float(long_size) / float(value)
    resized_width = int(round(im.shape[1] * scale))
    resized_height = int(round(im.shape[0] * scale))

    # 调整图像大小
    im = cv2.resize(im, (resized_width, resized_height), interpolation=interpolation)
    return im


# 定义一个函数，用于改变图片的尺寸
def rescale_size(img_size, target_size):
    # 计算缩放比例
    scale = min(max(target_size) / max(img_size), min(target_size) / min(img_size))
    # 计算改变后的尺寸
    rescaled_size = [round(i * scale) for i in img_size]
    # 返回改变后的尺寸和缩放比例
    return rescaled_size, scale


def resize_short(im, short_size=224, interpolation=cv2.INTER_LINEAR):
    value = min(im.shape[0], im.shape[1])
    scale = float(short_size) / float(value)
    resized_width = int(round(im.shape[1] * scale))
    resized_height = int(round(im.shape[0] * scale))

    im = cv2.resize(im, (resized_width, resized_height), interpolation=interpolation)
    return im


def resize_black_border(img, new_width, new_height, border_type, color=(0, 0, 0)):
    """将图片保持长宽比缩放至指定宽高(new_width, new_height)，周围补黑边

    Args:
        img: nparray, 需要resize的图片
        new_width: int, 缩放后的宽
        new_height: int, 缩放后的高
        border_type: int, 边框复制方式；cv2.BORDER_CONSTANT代表补常数值，cv2.BORDER_REPLICATE代表复制边界值
        color: tuple, 空余部分补常数值，默认为黑色

    Returns:
        pad_img: nparray, 按比例缩放并补黑边后的图片
    """
    size = img.shape
    h, w = size[0], size[1]
    # 长边缩放为min_side
    w_scale = new_width / w
    h_scale = new_height / h
    # if w > h:
    scale = w / new_width if w_scale < h_scale else h / new_height
    tmp_w, tmp_h = int(w / scale), int(h / scale)
    resize_img = cv2.resize(img, (tmp_w, tmp_h))

    # 从图像边界向上,下,左,右扩的像素数目
    top = int((new_height - tmp_h) / 2)
    bottom = int(new_height - tmp_h - top)
    left = int((new_width - tmp_w) / 2)
    right = int(new_width - tmp_w - left)

    if border_type == cv2.BORDER_REPLICATE:
        pad_img = cv2.copyMakeBorder(
            resize_img, top, bottom, left, right, cv2.BORDER_REPLICATE
        )
    elif border_type == cv2.BORDER_CONSTANT:
        pad_img = cv2.copyMakeBorder(
            resize_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
        )

    return pad_img


def merge_images(
    images_list,
    height,
    width,
    rows,
    black_border,
    background_color="black",
    text_info=None,
    mode="stretch",
):
    """将图片列表按指定行列数进行排布，生成大图

    Args:
        images_list: list, 需要进行排布的图片列表
        height: int, 大图内每张图片的高
        width: int, 大图内每张图片的宽
        rows: int, 排布的行数；列数会自动计算
        black_border: int, 大图内每张图片之间的间隔
        background_color: str, 'black'代表底色为黑色；'white'代表底色为白色
        text_info: list, 每张图片要写的描述
        mode: str, resize方式：'stretch'代表拉伸为指定宽高；'keep_aspect_ratio'代表保留长宽比，长边缩放为指定大小

    Returns:
        merged_image: nparray, 排布后的大图
    """
    cols = math.ceil(len(images_list) / rows)
    height = int(height)
    width = int(width)
    if background_color == "black":
        merged_image = (
            np.zeros(
                (
                    height * rows + black_border * max(0, rows - 1),
                    width * cols + black_border * max(0, cols - 1),
                    3,
                ),
                dtype=np.uint8,
            )
            * 255
        )
    elif background_color == "white":
        merged_image = (
            np.ones(
                (
                    height * rows + black_border * max(0, rows - 1),
                    width * cols + black_border * max(0, cols - 1),
                    3,
                ),
                dtype=np.uint8,
            )
            * 255
        )

    for image_index in range(len(images_list)):
        h_start = (image_index // cols) * (height + black_border)
        w_start = (image_index % cols) * (width + black_border)
        h_end = h_start + height
        w_end = w_start + width
        if mode == "stretch":
            merged_image[h_start:h_end, w_start:w_end, :] = cv2.resize(
                images_list[image_index], (width, height)
            ).copy()
        elif mode == "keep_aspect_ratio":
            if background_color == "black":
                merged_image[h_start:h_end, w_start:w_end, :] = resize_black_border(
                    images_list[image_index], width, height, cv2.BORDER_CONSTANT
                ).copy()
            elif background_color == "white":
                merged_image[h_start:h_end, w_start:w_end, :] = resize_black_border(
                    images_list[image_index],
                    width,
                    height,
                    cv2.BORDER_CONSTANT,
                    (255, 255, 255),
                ).copy()

    # 绘制描述信息
    if text_info is not None:
        dh = 50
        for image_index in range(len(images_list)):
            text = text_info[image_index]
            h_start = (image_index // cols) * (height + black_border) + height // 7
            w_start = (image_index % cols) * (width + black_border)

            for i, txt in enumerate(text.split("\n")):
                h = h_start + i * dh
                cv2.putText(
                    merged_image,
                    str(txt),
                    (w_start, h),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

    return merged_image


def filter_gray_error_image(image_dir):
    """删除视频保存中错误的图片，全图大部分为灰色

    Args:
        image_dir: str, 需要进行筛选的图像路径
    """
    files = os.listdir(image_dir)
    count = 0
    for index, file in enumerate(files):
        print(index)
        image = cv2.imread(image_dir + file)
        if fftCacul(image)[1] < 10:
            count += 1
            print(index, image_dir + file)
            os.remove(image_dir + file)
    print("rm num", count)


def filter_incomplete_image(image_dir_path):
    """删除指定目录下保存不完整的图像，即无法读取的图像

    Args:
        image_dir_path: str, 需要进行筛选的图像目录路径
    """
    images_path = glob.glob(f"{image_dir_path}*.jpg")
    count = 0
    for index, image_path in enumerate(images_path):
        if not is_valid_jpg(image_path):
            count += 1
            print(index, image_path, get_str_of_size(os.path.getsize(image_path)))
            os.remove(image_path)

    print("error num:", count)


def filter_similar_image(image_dir_path, save_image_dir_path, threshold=5):
    """感知哈希算法去除相似图像。如果不相同的数据位小于等于5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片。
    每张图片计算哈希值，计算两两图像的汉明距离，记录小于阈值的图像对，遍历删除相似图像，得到最终需要保留的图像，保存在同级目录'filtered_images/'下

    Args:
        image_dir_path: str, 需要进行筛选的图像路径
        save_image_dir_path: str, 筛选过的图像保存路径
        threshold: int, 汉明距离阈值
    """

    # 计算图像哈希值
    def avhash(image):
        if not isinstance(image, Image.Image):
            image = Image.open(image)
        image = image.resize((8, 8), Image.LANCZOS).convert("L")
        avg = reduce(lambda x, y: x + y, image.getdata()) / 64.0
        return reduce(
            lambda x, y_z: x | y_z[1] << y_z[0],
            enumerate(map(lambda i: 0 if i < avg else 1, image.getdata())),
            0,
        )

    # 计算哈希值汉明距离
    def hamming(h1, h2):
        h, d = 0, h1 ^ h2
        while d:
            h += 1
            d &= d - 1
        return h

    image_names = glob.glob(f"{image_dir_path}**/*.jpg",recursive=True)+glob.glob(f"{image_dir_path}**/*.png",recursive=True)

    print("Caculating hash value of images...")
    image_hash_list = []
    for index, image_name in enumerate(image_names):
        print(index, image_name)
        if not is_valid_jpg(image_name):
            image_names.remove(image_name)
            continue
        h_value = avhash(image_name)
        image_hash_list.append((image_name, h_value))

    print("Deleting duplicates")
    remaining_list = image_names.copy()
    for index_i in range(len(image_hash_list)):
        for index_j in range(index_i + 1, len(image_hash_list)):
            if (
                hamming(image_hash_list[index_i][1], image_hash_list[index_j][1])
                <= threshold
            ):
                print("delete %d %s" % (index_i, image_hash_list[index_i][0]))
                remaining_list.remove(image_hash_list[index_i][0])
                break

    print("Copying remaining images...")
    for index in range(len(remaining_list)):
        print(f"keep {remaining_list[index]}")
        save_path = Path(save_image_dir_path)/Path(remaining_list[index]).relative_to(image_dir_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(remaining_list[index], save_path)


"""
Others
"""


def image_to_base64(rgb_image):
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    image = cv2.imencode(".jpg", bgr_image)[1]
    # image_base64 = str(base64.b64encode(image))[2:-1]
    image_base64 = base64.b64encode(image)
    image_base64 = str(image_base64, encoding="utf-8")
    return image_base64


def base64_to_image(image_base64):
    # base64解码
    img_data = base64.b64decode(image_base64)
    # 转换为np数组
    rgb_array = np.fromstring(img_data, np.uint8)
    return cv2.imdecode(rgb_array, cv2.IMREAD_COLOR)


def imread(filename: str, flags: int = cv2.IMREAD_COLOR):
    return cv2.imdecode(np.fromfile(filename, np.uint8), flags)


def imwrite(filename: str, img: np.ndarray, params=None):
    try:
        cv2.imencode(os.path.splitext(filename)[1], img, params)[1].tofile(filename)
        return True
    except Exception:
        return False


def pillow_to_numpy(img):
    img_numpy = np.asarray(img)
    if not img_numpy.flags.writeable:
        img_numpy = np.array(img)
    return img_numpy


def numpy_to_pillow(img, mode=None):
    return Image.fromarray(img, mode=mode)


