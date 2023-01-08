import cv2
import math
import glob
import os
import numpy as np
from functools import cmp_to_key
from PIL import Image

from .FileUtils import *
from .Convertion import xyxy2xywh_center, xywh_center2xyxy, xyxy2points, quadrilateral_points2left_top_first_quadrilateral, quadrilateral_points2rectangle_xyxy


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global image_path

    if event == cv2.EVENT_LBUTTONDOWN:
        print(image_path)
        print(x, y)
        

def get_image_features(image, mode='cv2'):
    '''获取图像的属性
    读取图像+获取属性总时间，PIL格式比opencv格式快4倍；如果只是获取分辨率，建议使用PIL格式

    Args:
        cv2_image: np.array, cv2读取的图像
        mode: str, 若为'cv2'，读取opencv格式的图像；若为'PIL'，读取PIL格式的图像高宽；若为'PIL_channel'，读取PIL格式的图像高宽及通道

    Returns:
        height: int, 图像高
        width: int, 图像宽
        channel: int, 图像通道数
    '''
    if mode == 'cv2':
        height, width, channel = image.shape
        return height, width, channel
    elif mode == 'PIL':
        width, height = image.size
        return height, width
    elif mode == 'PIL_channel':
        width, height = image.size
        channel = len(image.split())
        return height, width, channel


def get_video_features(capture):
    '''获取cv2格式视频的属性

    Args:
        capture: cv2.VideoCapture, cv2读取的视频

    Returns:
        fps: int, 帧率
        width: int, 分辨率-宽度
        height: int, 分辨率-高度
        whole_frame_num: int, 总帧数
        current_frame_num: int, 视频文件的当前位置（以毫秒为单位）或帧数（cv2.CAP_PROP_POS_FRAMES）
        duration: int, 时长（单位s）
        fourcc: int, four character code, 视频编码格式，fourcc.org/fourcc.php
                               写视频常用
                               fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                                "MP4V", MPEG-4编码类型，文件名后缀为.mp4
                                "I420",    YUV编码类型，文件名后缀为.avi
                                "PIMI",   MPEG-1编码类型，文件名后缀为.avi
                                "XVID",   MPEG-4编码类型，文件名后缀为.avi
                                "THEO", Ogg Vorbis,  文件名后缀为.ogv
                                "FLV1",    Flash视频，文件名后缀为.flv
    '''
    fps = int(round(capture.get(cv2.CAP_PROP_FPS)))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    whole_frame_num = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame_num = int(capture.get(cv2.CAP_PROP_POS_MSEC))
    duration = whole_frame_num / 1000 / fps
    fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))
    
    return fps, width, height, whole_frame_num, current_frame_num, duration, fourcc
 

def fftCacul(img):
    '''
    :param img: the input image
    :param isOccu: judge whether to occlusion of the current frame by
                    Gaussian mixture model background modeling
    :return: judge whether to occlusion of the current frame by FFT or backGround modeling
    '''
    img_col = cv2.resize(img, (403, 226), interpolation=cv2.INTER_AREA)

    np.seterr(all='ignore')
    assert isinstance(img_col, np.ndarray), 'img_col must be a numpy array'
    assert img_col.ndim == 3, 'img_col must be a color image ({0} dimensions currently)'.format(img_col.ndim)

    img_gry = cv2.cvtColor(img_col, cv2.COLOR_RGB2GRAY)
    rows, cols = img_gry.shape
    crow, ccol = rows//2, cols//2
    f = np.fft.fft2(img_gry)
    fshift = np.fft.fftshift(f)
    fshift[crow-75:crow+75, ccol-75:ccol+75] = 0
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
    elif jpg_file_path.split('.')[-1].lower() == 'jpg':
        with open(jpg_file_path, 'rb') as f:
            f.seek(-2, 2)
            f_end = f.read()
            return f_end == b'\xff\xd9' #判定jpg是否包含结束字段
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
    

def get_specify_frame(capture, frame_num):
    '''获取视频指定帧。如果视频格式有错误，该命令无效，只能从第0帧开始读取，需要重新修改视频格式

    Args:
        capture: cv2.VideoCapture, 视频
        frame_num: int, 指定帧
    '''
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = capture.read()

    return frame


def draw_framenum_on_video(src_video_path, save_video_path, fourcc):
    '''绘制帧号在视频左上角

    Args:
        src_video_path: str, 原始视频路径
        save_video_path: str, 保存视频路径
        fourcc: str, 视频编码格式
    '''
    capture = cv2.VideoCapture(src_video_path)
    assert capture.isOpened()
    fps, width, height, _, _, _, _ = get_video_features(capture)

    os.makedirs(os.path.dirname(save_video_path), exist_ok=True)
    writer = cv2.VideoWriter(save_video_path, cv2.VideoWriter_fourcc(*fourcc), fps, (width,height), True)

    ret, frame = capture.read()
    frame_count = 0
    while ret:
        print("frame_count: ", frame_count)
        cv2.putText(frame, str(frame_count), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
        writer.write(frame)
        ret, frame = capture.read()
        frame_count += 1

    capture.release()
    writer.release()


def cut_video_clip(src_video_path, start_frame_num, end_frame_num, clip_path, fourcc):
    '''截取指定帧段的视频并保存。
    从指定帧开始读取，如果视频格式有错误，该命令无效，只能从第0帧开始读取，需要重新修改视频格式
    cv2.VideoCapture有设置当前帧的功能，cv2.VideoWriter没有。https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga41c5cfa7859ae542b71b1d33bbd4d2b4

    Args:
        src_video_path: str, 原始视频路径
        start_frame_num: int, 开始截取帧号
        end_frame_num: int, 结束截取帧号
        clip_path: str, 视频片段名保存路径
        fourcc: str, 视频编码格式
    '''
    capture = cv2.VideoCapture(src_video_path)
    assert capture.isOpened()

    fps, width, height, _, _, _, _ = get_video_features(capture)

    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame_num)
    ret, frame = capture.read()

    os.makedirs(os.path.split(clip_path)[0], exist_ok=True)
    writer = cv2.VideoWriter(clip_path, cv2.VideoWriter_fourcc(*fourcc), fps, (width,height), True)

    while ret:
        if(start_frame_num <= end_frame_num):
            print("frame_count: ", start_frame_num)
            writer.write(frame)
            ret, frame = capture.read()
            start_frame_num += 1
        else:
            break

    capture.release()
    writer.release()
    cv2.destroyAllWindows()


def get_mask_images(mask_images_list):
    '''根据mask_images_list读取所有蒙版图像，以蒙版图像名作为字典key，返回字典

    Args:
        mask_images_list: list, 蒙版图像文件路径

    Returns:
        mask_images_dict, dict, {"mask_name" : nparray}
    '''
    mask_images_dict = {}
    for line in mask_images_list:
        image_name = os.path.basename(line).split('.')[0]
        image = cv2.imread(line)
        img_gry = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        mask_images_dict[image_name] = img_gry

    return mask_images_dict


def point_in_mask(point, mask_image):
    '''判断蒙版图像中指定点是否合法

    Args:
        point: list, 二维点坐标[x, y]
        mask_image: nparray, 蒙版灰度图

    Returns:
        bool, 若该点对应的像素值大于128，则合法；反之，不合法
    '''
    if point[0] < 0 or point[0] >= mask_image.shape[1] or point[1] < 0 or point[1] >= mask_image.shape[0]:
        return False
    else:
        return mask_image[int(point[1]),int(point[0])] > 128


def gray2heatmap(image):
    '''将灰度图转换为热力图

    Args:
        image: np.array, 灰度图
    
    Returns:
        heatmap: np.array, 热力图
    '''
    norm_img = image.copy()
    cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    norm_img = 255 - norm_img

    heatmap = cv2.applyColorMap(norm_img, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    return heatmap


def depth2gray(depth_npy_path):
    '''深度图转换为灰度图

    Args:
        depth_npy_path: str, 深度图路径

    Returns:
        norm_img: np.array, 灰度图
    '''
    depth = np.load(depth_npy_path)
    depth[np.isnan(depth)] = np.nanmin(depth)
    depth[np.isinf(depth)] = np.nanmin(depth)
    norm_img = depth.copy()
    cv2.normalize(depth, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    # norm_img = 255 - norm_img
    # depth[depth==255] = 0

    return norm_img


def gen_affine_image(src_image, src_image_points, dst_image_points, width, height):
    '''对图像做仿射变换，生成新的图像。仿射变换：将矩形映射成任意平行四边形，各边仍保持平行。需要提供三个顶点。

    Args:
        src_image: nparray, 原始图像
        src_image_points: list, 原始图像上三个点，按逆时针排序，三个点分别对应左上角、左下角、右上角，如[[58,144],[348,960],[1920,130]]
        dst_image_points: list, 原始图像上变换目标三个点，按逆时针排序，三个点分别对应左上角、左下角、右上角，如[[0,0], [0,height], [width,0]]
        width: int, 保存仿射变换图像的宽
        height: int, 保存仿射变换图像的高
    
    Returns:
        affine_image: nparray, 仿射变换生成的图像
    '''
    M = cv2.getAffineTransform(np.float32(src_image_points), np.float32(dst_image_points))
    affine_image = cv2.warpAffine(src_image, M, (width, height))

    return affine_image


def gen_perspective_image(src_image, src_image_points, dst_image_points, width, height):
    '''对图像做透视变换，生成新的图像。透视变换：将矩形映射为任意四边形，直线仍保持直线。由于不再是平行四边形，需提供四个顶点。

    Args:
        src_image: nparray, 原始图像
        src_image_points: list, 原始图像上四个点，按逆时针排序，如[[58,144],[348,960],[1678,936],[1920,130]]
        dst_image_points: list, 原始图像上变换目标四个点，按逆时针排序，如[[0,0], [0,height], [width,height], [width,0]]
        width: int, 保存透视变换图像的宽
        height: int, 保存透视变换图像的高
    
    Returns:
        perspective_image: nparray, 透视变换生成的图像
    '''
    M = cv2.getPerspectiveTransform(np.float32(src_image_points), np.float32(dst_image_points))
    perspective_image = cv2.warpPerspective(src_image, M, (width, height))

    return perspective_image


def gen_perspective_points(src_image_points, dst_image_points, src_points):
    '''对点做透视变换，生成新的点

    Args:
        src_image_points: list, 原始图像上四个点，按逆时针排序，如[[58,144],[348,960],[1678,936],[1920,130]]
        dst_image_points: list, 原始图像上变换目标四个点，按逆时针排序，如[[0,0], [0,height], [width,height], [width,0]]
        src_points: list, 原始点；eg: [[x1,y1],[x2,y2],...]

    Returns:
        perspective_points: list, 透视变换生成的矩形框
    '''
    M = cv2.getPerspectiveTransform(np.float32(src_image_points), np.float32(dst_image_points))

    n = len(src_points)
    base_points_arr = np.array(src_points, dtype=int)
    xy = np.ones((n, 3))

    xy[:, :2] = base_points_arr.reshape(n, 2)
    
    xy = xy @ M.T
    xy = xy[:, :2] / xy[:, 2:3]

    perspective_points = np.array(xy[:, :2], dtype=int)

    return perspective_points


def gen_perspective_boxes(src_image_points, dst_image_points, src_boxes, width, height):
    '''对矩形框做透视变换，生成新的矩形框

    Args:
        src_image_points: list, 原始图像上四个点，按逆时针排序，如[[58,144],[348,960],[1678,936],[1920,130]]
        dst_image_points: list, 原始图像上变换目标四个点，按逆时针排序，如[[0,0], [0,height], [width,height], [width,0]]
        src_boxes: list, 原始矩形框
        width: int, 原始图像的宽
        height: int, 原始图像的高

    Returns:
        perspective_boxes: nparray, 透视变换生成的矩形框
    '''
    M = cv2.getPerspectiveTransform(np.float32(src_image_points), np.float32(dst_image_points))

    n = len(src_boxes)
    base_box_arr = np.array(src_boxes, dtype=int)
    # 设变换之前的点是z值为1的点，它三维平面上的值是x,y,1，在二维平面上的投影是x,y
    xy = np.ones((n * 4, 3))

    # [xmin, ymin, xmax, ymax]转为[x1y1, x2y2, x1y2, x2y1]
    xy[:, :2] = base_box_arr[:, [0, 1, 2, 3, 0, 3, 2, 1]].reshape(n * 4, 2)  
    
    # 通过矩阵变换成三维中的点X,Y,Z，除以三维中Ｚ轴的值，转换成二维中的点，得到变换后四边形四个角点的(x,y)值；
    xy = xy @ M.T
    xy = (xy[:, :2] / xy[:, 2:3]).reshape(n, 8)
    
    # 取四边形最小最大x,y作为新的矩形[xmin,ymin,xmax,ymax]
    x = xy[:, [0, 2, 4, 6]]
    y = xy[:, [1, 3, 5, 7]]
    xy = np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T

    # 宽高边界值
    xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
    xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)
    perspective_boxes = np.array(xy, dtype=int)

    return perspective_boxes


def gen_mask_image(points_list, width, height):
    '''根据连续顶点列表生成指定大小的蒙版图像

    Args:
        points_list: list, 顶点列表，顶点要按照顺时针或逆时针顺序排列好
        width: int, 蒙版图像的宽
        height: int, 蒙版图像的高
    
    Returns:
        mask_image: nparray, 生成的蒙版图像
    '''
    mask_image = np.zeros((height, width, 3),dtype=np.uint8) * 255
    poly = np.array(points_list)
    cv2.fillPoly(mask_image, [poly], (255, 255, 255))

    return mask_image


def extend_box(bbox, extend_ratio_width, extend_ratio_height):
    '''按extend_ratio对矩形进行扩边
    
    Args:
        bbox: list, 矩形框，格式[xmin, ymin, xmax, ymax]
        extend_ratio_width: float, 宽扩边比例。如0.4，则扩边1.4倍
        extend_ratio_height: float, 高扩边比例。如0.4，则扩边1.4倍
    
    Returns:
        extend_box: list, 矩形框，格式[xmin, ymin, xmax, ymax]
    '''
    bbox_xywh_center = xyxy2xywh_center(bbox)
    bbox_xywh_center[2] = bbox_xywh_center[2] * (1 + extend_ratio_width)
    bbox_xywh_center[3] = bbox_xywh_center[3] * (1 + extend_ratio_height)
    extend_box = xywh_center2xyxy(bbox_xywh_center)

    return extend_box


def crop_image_extend_border(image, bbox, extend_ratio_width=0, extend_ratio_height=0):
    '''从图片中裁剪出一个矩形，按extend_ratio进行扩边
    
    Args:
        image: nparray, 需要裁剪的图像
        bbox: list, 矩形框，格式[xmin, ymin, xmax, ymax]
        extend_ratio_width: float, 宽扩边比例。如0.4，则扩边1.4倍
        extend_ratio_height: float, 高扩边比例。如0.4，则扩边1.4倍
    
    Returns:
        roi_img: nparray, 裁剪后的图片
    '''
    height, width = image.shape[:2]
    bbox_xyxy = extend_box(bbox, extend_ratio_width, extend_ratio_height)
    
    # image slice，图像切片/裁剪，img[y : y+h, x:x+w]   [0:rows, 0:cols]
    roi_img = image[max(bbox_xyxy[1], 0):min(bbox_xyxy[3], height), 
                                       max(bbox_xyxy[0], 0):min(bbox_xyxy[2], width)]

    return roi_img


def crop_rotated_box_image(image, rotated_box, size):
    '''裁剪旋转矩形框

    Args:
        image: np.array, 图像
        rotated_box: list, 旋转矩形, [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    Returns:
        rotated_box_image: np.array, 裁剪后的图像
        size: tuple, 旋转行人框的尺寸(width, height)
    '''
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
    left_top_first_rotated_box = np.int0(quadrilateral_points2left_top_first_quadrilateral(rotated_box, mode='person_quad'))

    # 做透视变换，将旋转矩形区域校正至矩形宽高区域
    src_image_points = left_top_first_rotated_box.astype("float32")
    dst_image_points = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")
    rotated_box_image = gen_perspective_image(image, src_image_points, dst_image_points, width, height)

    return rotated_box_image


def pad_shorter(img):
    '''PIL.Image图像短边补黑边

    Args:
        img: PIL.Image, 需要resize的图片

    Returns:
        new_img: PIL.Image, 补黑边后的图像
    '''
    w,h = img.size[-2:]
    s = max(h, w) 
    new_im = Image.new("RGB", (s, s))
    new_im.paste(img, ((s-w)//2, (s-h)//2))
    return new_im


def pad_shorter_ratio(img, ratio, border_type):
    '''PIL.Image图像短边补黑边，设定补黑边后的图像宽高比例为ratio

    Args:
        img: PIL.Image, 需要resize的图片
        ratio: float, 宽高比
        border_type: int, 边框复制方式；cv2.BORDER_CONSTANT代表补常数值，cv2.BORDER_REPLICATE代表复制边界值

    Returns:
        new_img: PIL.Image, 补黑边后的图像
    '''
    w,h = img.size[-2:]
    if ratio < 1:
        new_width, new_height = w, int(w/ratio)
    else:
        new_width, new_height = h*ratio, h
    
    cv2_img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)

    if border_type == cv2.BORDER_REPLICATE:
        cv2_pad_img = resize_black_border(cv2_img, new_width, new_height, cv2.BORDER_REPLICATE)
    elif border_type == cv2.BORDER_CONSTANT:
        cv2_pad_img = resize_black_border(cv2_img, new_width, new_height, cv2.BORDER_CONSTANT)
    
    pad_im = Image.fromarray(cv2.cvtColor(cv2_pad_img,cv2.COLOR_BGR2RGB))

    return pad_im


def resize_black_border(img, new_width, new_height, border_type, color=(0, 0, 0)):
    '''将图片保持长宽比缩放至指定宽高(new_width, new_height)，周围补黑边

    Args:
        img: nparray, 需要resize的图片
        new_width: int, 缩放后的宽
        new_height: int, 缩放后的高
        border_type: int, 边框复制方式；cv2.BORDER_CONSTANT代表补常数值，cv2.BORDER_REPLICATE代表复制边界值
        color: tuple, 空余部分补常数值，默认为黑色

    Returns:
        pad_img: nparray, 按比例缩放并补黑边后的图片
    '''
    size = img.shape
    h, w = size[0], size[1]
    #长边缩放为min_side
    w_scale = new_width / w
    h_scale = new_height / h
    # if w > h:
    if w_scale < h_scale:
        scale = w / new_width
    else:
        scale = h / new_height

    tmp_w, tmp_h = int(w/scale), int(h/scale)
    resize_img = cv2.resize(img, (tmp_w, tmp_h))
    
    #从图像边界向上,下,左,右扩的像素数目
    top = int((new_height - tmp_h)/2)
    bottom = int(new_height - tmp_h - top)
    left = int((new_width - tmp_w)/2)
    right = int(new_width - tmp_w - left)
    
    if border_type == cv2.BORDER_REPLICATE:
        pad_img = cv2.copyMakeBorder(resize_img, top, bottom, left, right, cv2.BORDER_REPLICATE)
    elif border_type == cv2.BORDER_CONSTANT:
        pad_img = cv2.copyMakeBorder(resize_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color) 

    return pad_img


def merge_images(images_list, height, width, rows, black_border, background_color='black', text_info=None, mode='stretch'):
    '''将图片列表按指定行列数进行排布，生成大图

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
    '''
    cols =math.ceil(len(images_list) / rows)
    height = int(height)
    width = int(width)
    if background_color == 'black':
        merged_image = np.zeros((height*rows + black_border*max(0, rows-1),width*cols + black_border*max(0, cols-1),3),dtype=np.uint8) * 255
    elif background_color == 'white':
        merged_image = np.ones((height*rows + black_border*max(0, rows-1),width*cols + black_border*max(0, cols-1),3),dtype=np.uint8) * 255

    for image_index in range(len(images_list)):
        h_start = (image_index//cols) * (height + black_border)
        w_start = (image_index%cols) * (width + black_border)
        h_end = h_start + height
        w_end = w_start + width
        if mode == 'stretch':
            merged_image[h_start:h_end,w_start:w_end,:] = cv2.resize(images_list[image_index], (width,height)).copy()
        elif mode == 'keep_aspect_ratio':
            if background_color == 'black':
                merged_image[h_start:h_end,w_start:w_end,:] = resize_black_border(images_list[image_index], width, height, cv2.BORDER_CONSTANT).copy()
            elif background_color == 'white':
                merged_image[h_start:h_end,w_start:w_end,:] = resize_black_border(images_list[image_index], width, height, cv2.BORDER_CONSTANT, (255,255,255)).copy()

    # 绘制描述信息
    if text_info is not None:
        dh = 50
        for image_index in range(len(images_list)):
            text = text_info[image_index]
            h_start = (image_index//cols) * (height + black_border) + int(height / 7)
            w_start = (image_index%cols) * (width + black_border)
            
            for i, txt in enumerate(text.split('\n')):
                h = h_start + i * dh
                cv2.putText(merged_image, str(txt), (w_start, h), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

    return merged_image


def merge_videos(videos_path_list, height, width, rows, black_border, saved_video_path, show_info):
    '''将视频列表按指定行列数进行排布，生成大图视频

    Args:
        videos_path_list: list, 需要进行排布的视频列表
        height: int, 大图内每张图片的高
        width: int, 大图内每张图片的宽
        rows: int, 排布的行数；列数会自动计算
        black_border: int, 大图内每张图片之间的间隔
        saved_video_path: str, 保存视频的路径
        show_info: list, 每张图片要写的描述
    '''
    frame_count = 0
    captures_list, rets, frames = [], [], []
    for video_name in videos_path_list:
        capture = cv2.VideoCapture(video_name)
        assert capture.isOpened()
        captures_list.append(capture)
    
    for capture_index in range(len(captures_list)):
        tmp_ret, tmp_frame = captures_list[capture_index].read()
        rets.append(tmp_ret)
        frames.append(tmp_frame)
    
    tmp_merged_image = merge_images(frames, height, width, rows, black_border)
    fps = int(round(captures_list[0].get(cv2.CAP_PROP_FPS)))
    video =cv2.VideoWriter(saved_video_path, cv2.VideoWriter_fourcc('D','I','V','X'), fps, (tmp_merged_image.shape[1], tmp_merged_image.shape[0]), True)

    while rets[0]:
        print('frame_count', frame_count)
        # if frame_count > 25*10:
        #     break
        if not(show_info is None):
            for frame_index in range(len(frames)):
                cv2.putText(frames[frame_index], show_info[frame_index], (10, 50), cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),2)
                cv2.putText(frames[frame_index], str(frame_count), (10, 200), cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),2)

        merged_image = merge_images(frames, height, width, rows, black_border)
        video.write(merged_image)

        for capture_index in range(len(captures_list)):
            tmp_ret, tmp_frame = captures_list[capture_index].read()
            rets[capture_index] = tmp_ret
            frames[capture_index] = tmp_frame
        
        frame_count += 1

    for capture_index in range(len(captures_list)):
        captures_list[capture_index].release()
    
    video.release()


def image_with_translucent_mask(image, mode, mask_info, color, alpha, beta, gamma):
    '''原图上绘制半透明mask图像
    dst = src1 * alpha + src2 * beta + gamma
    若需要覆盖操作，使用src_image[h_start:h_end,w_start:w_end,:] = box_image
    
    Args:
        image: np.array, 原图
        mode: str, 'rect'代表矩形mask；'circle'代表圆形mask；'polygon'代表多边形mask；'img'代表图像mask
        mask_info: 对应的mask信息
        color: tuple, 几何图形mask颜色
        alpha: float, 图像1的权重
        beta: float, 图像2的权重
        gamma: float, 偏移量

    Returns:
        dst_image: np.array, 添加mask后的图形
    '''
    empty_image = np.zeros((image.shape), dtype=np.uint8)

    if mode == 'rect':
        mask_image = cv2.rectangle(empty_image, (int(mask_info[0]), int(mask_info[1])), (int(mask_info[2]),int(mask_info[3])), color, thickness=-1)
    elif mode == 'circle':
        mask_image = cv2.circle(empty_image, (int(mask_info[0]),int(mask_info[1])), radius = mask_info[2], color = color, thickness=-1)
    elif mode == 'polygon':
        mask_image = cv2.fillPoly(empty_image, mask_info, color)
    elif mode == 'img':
        mask_image = mask_info
    
    dst_image = cv2.addWeighted(image, alpha, mask_image, beta, gamma)

    return dst_image


'''
相机标定
'''
def get_chessboard_corners(image_path, row, col):
    '''寻找图像中棋盘格的角点，并使用亚像素角点检测进行修正

    Args:
        image_path: str, 图像路径
        row: int, 棋盘格角点行数
        col: int, 棋盘格角点列数

    Returns:
        ret: bool, 是否找到棋盘格角点
        image: np.array, 图像
        corners: np.array, 像素级别的棋盘格角点
        corners_subpixel: np.array, 亚像素级别的棋盘格角点
    '''
    corners_subpixel = None
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.001)

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (row, col), None)
    
    if ret == True:
        corners_subpixel = cv2.cornerSubPix(gray,corners, (5,5), (-1,-1), criteria)

    return ret, image, corners, corners_subpixel


def calibration_internal_params(intern_image_paths_list, row, col, show_flag=False):
    '''多张棋盘格图像标定内参

    Args:
        intern_image_paths_list: list, 多张内参图像绝对路径列表
        row: int, 棋盘格角点行数
        col: int, 棋盘格角点列数
        show_flag: bool, 是否绘制棋盘格

    Returns:
        A_matrix: np.array, 内参矩阵
        d_vector: np.array, 畸变系数向量
        mean_error/len(objpoints): np.array, 误差
    '''
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((col * row, 3), np.float32)
    objp[:,:2] = np.mgrid[0:row, 0:col].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    image_points = [] # 2d points in image plane.

    for intern_image_path in intern_image_paths_list:
        ret, image, _, corners_subpixel = get_chessboard_corners(intern_image_path, row, col)

        if ret == True:
            objpoints.append(objp)
            image_points.append(corners_subpixel)

            if show_flag:
                # 绘制棋盘格角点，红色线头为起始点
                image = cv2.drawChessboardCorners(image, (row, col), corners_subpixel,ret)

                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                cv2.resizeWindow("image", image.shape[1], image.shape[0])
                cv2.imshow('image', image)
                cv2.waitKey(10)

    if show_flag:
        cv2.destroyAllWindows()

    # A_matrix内参矩阵, d_vector畸变系数; r_vector旋转向量, t_vector平移向量(每张图像有一个rt)
    ret, A_matrix, d_vector, r_vector, t_vector = cv2.calibrateCamera(objpoints, image_points, image.shape[::-1][1:], None, None)

    mean_error = 0
    for i in range(len(objpoints)):
        # 通过给定的内参数和外参数计算三维点投影到二维图像平面上的坐标
        calcu_image_points, _ = cv2.projectPoints(objpoints[i], r_vector[i], t_vector[i], A_matrix, d_vector)
        error = cv2.norm(image_points[i], calcu_image_points, cv2.NORM_L2)/len(calcu_image_points)
        mean_error += error

    return A_matrix, d_vector, mean_error/len(objpoints)


def calibration_external_params(extern_image_path, id, A_matrix, d_vector, row, col, side, save_json_path, show_flag):
    '''单张棋盘格图像标定外参。利用几组世界坐标系3D点和对应图像坐标系2D点坐标，以及内参反推出外参

    Args:
        extern_image_path: str, 外参图像绝对路径
        id: str, 相机id号
        A_matrix: np.array, 内参矩阵
        d_vector: np.array, 畸变系数向量
        row: int, 棋盘格角点行数
        col: int, 棋盘格角点列数
        side: int, 棋盘格方格边长，单位mm
        save_json_path: str, 内外参json文件保存路径
        show_flag: bool, 是否绘制棋盘格

    Returns:
        mean_error/len(objpoints): np.array, 误差
    '''
    carmera, carmeraMatrix = {}, {}
    carmera['id'] = id
    carmera['calib_extern_image'] = os.path.basename(extern_image_path)

    objp = np.zeros((col * row, 3), np.float32)
    objp[:,:2] = np.mgrid[0:row, 0:col].T.reshape(-1,2)
    objp = objp * side

    A_matrix = A_matrix.reshape(3, 3)
    d_vector = d_vector.reshape(1, 5)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    image_points = [] # 2d points in image plane.

    ret, image, _, corners_subpixel = get_chessboard_corners(extern_image_path, row, col)

    if ret == True:
        objpoints.append(objp)
        image_points.append(corners_subpixel)

        if show_flag:
            # 绘制棋盘格角点，红色线头为起始点
            image = cv2.drawChessboardCorners(image, (row, col), corners_subpixel,ret)

            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow("image", image.shape[1], image.shape[0])
            cv2.imshow('image',image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # 利用几组世界坐标系3D点和对应图像坐标系2D点坐标，以及内参反推出外参
    ret, rotation, translation = cv2.solvePnP(objpoints[0], image_points[0], A_matrix, d_vector)
    
    # 利用罗德里格斯公式将旋转向量转换为旋转矩阵
    R_matrix = cv2.Rodrigues(rotation)[0]
    RT = np.hstack((R_matrix,translation))
    print("RT: ", RT)

    # 重投影计算误差
    calcu_image_points, _ = cv2.projectPoints(objpoints[0], rotation, translation, A_matrix, d_vector)
    error0 = cv2.norm(image_points[0], calcu_image_points, cv2.NORM_L2) / len(calcu_image_points)
    print(id,"error: ", error0)
    
    carmera['kmat'] = A_matrix.reshape(1, 9).tolist()[0]
    carmera['dvec'] = d_vector.reshape(1, 5).tolist()[0]
    carmera['pmat'] = RT.reshape(1,12).tolist()[0]
    carmeraMatrix["cameras"] = [carmera]

    save_json(save_json_path, carmeraMatrix)


def verify_calibration_params():
    '''验证内外参标定是否正确
        1.重投影计算误差
        2.将世界坐标系中某一点重投影回图像内，绘制出来，观察是否准确
    '''
    pass


def get_undistort_image_using_A(image_path, calib_json_path, crop_flag=False):
    '''利用内参矩阵得到去除图像畸变后的图像

    Args:
        image_path: str, 外参图像路径
        calib_json_path: str, 内外参标定文件路径
        crop_flag: bool, 是否剪裁掉去除畸变产生的外侧黑边区域

    Returns:
        undistort_image: np.array, 去畸变后的图像
    '''
    json_data = read_json(calib_json_path, mode = 'all')
    A_matrix = np.array(json_data['cameras'][0]['kmat']).reshape(3,3)
    d_vector = np.array(json_data['cameras'][0]['dvec']).reshape(1,5)

    image = cv2.imread(image_path)
    h,  w = image.shape[:2]
    new_A_matrix, roi=cv2.getOptimalNewCameraMatrix(A_matrix, d_vector, (w,h),1,(w,h))
    undistort_image = cv2.undistort(image, A_matrix, d_vector, None, new_A_matrix)

    # 裁剪黑边
    if crop_flag:
        x,y,w,h = roi
        undistort_image = undistort_image[y:y+h, x:x+w]

    return undistort_image


def get_undistort_points_using_A(points, calib_json_path, width, height):
    '''利用内参矩阵得到去除图像畸变后的点

    Args:
        points: list, 点列表
        width: int, 原始图像宽
        height: int, 原始图像高
        calib_json_path: str, 内外参标定文件路径

    Returns:
        undistort_points: np.array, 去畸变后的点
    '''
    json_data = read_json(calib_json_path, mode = 'all')
    A_matrix = np.array(json_data['cameras'][0]['kmat']).reshape(3,3)
    d_vector = np.array(json_data['cameras'][0]['dvec']).reshape(1,5)

    new_A_matrix, roi=cv2.getOptimalNewCameraMatrix(A_matrix, d_vector, (width, height),1,(width, height))
    points = points.reshape(-1, 1, 2).astype(np.float32)
    undistort_points = cv2.undistortPoints(points, A_matrix, d_vector, None, new_A_matrix).reshape(-1, 2)

    return undistort_points


def get_undistort_box_using_A(box, calib_json_path, width, height):
    '''利用内参矩阵得到去除图像畸变后的矩形框

    Args:
        box: list, 矩形框
        width: int, 原始图像宽
        height: int, 原始图像高
        calib_json_path: str, 内外参标定文件路径

    Returns:
        undistort_box: np.array, 去畸变后的矩形框
    '''
    json_data = read_json(calib_json_path, mode = 'all')
    A_matrix = np.array(json_data['cameras'][0]['kmat']).reshape(3,3)
    d_vector = np.array(json_data['cameras'][0]['dvec']).reshape(1,5)

    new_A_matrix, roi=cv2.getOptimalNewCameraMatrix(A_matrix, d_vector, (width, height),1,(width, height))
    points = np.array(xyxy2points(box), dtype=np.float32).reshape(-1, 1, 2)
    undistort_points = cv2.undistortPoints(points, A_matrix, d_vector, None, new_A_matrix).reshape(-1, 2).tolist()
    undistort_box = quadrilateral_points2rectangle_xyxy(undistort_points)

    return undistort_box


def get_point_distance_using_RT(image_path, calib_json_path, point_row, point_col, row, col, side, show_flag=False):
    '''利用外参计算棋盘格某一点距离相机的距离

    Args:
        image_path: str, 外参图像路径
        calib_json_path: str, 内外参标定文件路径
        point_row: int, 该点所在棋盘格内的行数，从1开始算
        point_col: int, 该点所在棋盘格内的列数，从1开始算
        row: int, 棋盘格角点总行数
        col: int, 棋盘格角点总列数
        side: int, 棋盘格每个方格的边长，单位毫米
        show_flag: bool, 是否将距离和点绘制在图像上

    Returns:
        distance: float, 该点距离相机的距离
    '''
    def RotateByZ(Cx, Cy, thetaZ):
        rz = thetaZ*math.pi/180.0
        outX = math.cos(rz)*Cx - math.sin(rz)*Cy
        outY = math.sin(rz)*Cx + math.cos(rz)*Cy
        return outX, outY
    def RotateByY(Cx, Cz, thetaY):
        ry = thetaY*math.pi/180.0
        outZ = math.cos(ry)*Cz - math.sin(ry)*Cx
        outX = math.sin(ry)*Cz + math.cos(ry)*Cx
        return outX, outZ
    def RotateByX(Cy, Cz, thetaX):
        rx = thetaX*math.pi/180.0
        outY = math.cos(rx)*Cy - math.sin(rx)*Cz
        outZ = math.sin(rx)*Cy + math.cos(rx)*Cz
        return outY, outZ

    json_data = read_json(calib_json_path, mode = 'all')
    for cam_data in json_data['cameras']:
        if cam_data['calib_extern_image'] == os.path.basename(image_path):
            Rt = np.array(cam_data['pmat']).reshape(3,4)
            R_matrix = Rt[:,:3]
            t_vector = Rt[:,3]

            point_world_coordinate = [point_row * side, point_col * side, 0]
            point_vector = point_world_coordinate

            # 验证根据博客http://www.cnblogs.com/singlex/p/pose_estimation_1.html提供方法求解相机位姿
            # 先将相机坐标系与世界坐标系旋转为平行：计算相机坐标系的三轴旋转欧拉角，旋转后可以转出世界坐标系。旋转顺序z,y,x
            thetaZ = math.atan2(R_matrix[1, 0], R_matrix[0, 0])*180.0/math.pi
            thetaY = math.atan2(-1.0*R_matrix[2, 0], math.sqrt(R_matrix[2, 1]**2 + R_matrix[2, 2]**2))*180.0/math.pi
            thetaX = math.atan2(R_matrix[2, 1], R_matrix[2, 2])*180.0/math.pi
            # 相机坐标系下的值
            x, y, z = t_vector[0], t_vector[1], t_vector[2]

            # 按顺序进行三次旋转
            (x, y) = RotateByZ(x, y, -1.0*thetaZ)
            (x, z) = RotateByY(x, z, -1.0*thetaY)
            (y, z) = RotateByX(y, z, -1.0*thetaX)
            
            # 相机位置在世界坐标系的坐标
            Cx, Cy, Cz = x*-1, y*-1, z*-1
            t_vector = np.array([Cx, Cy, Cz])
            
            # 点到相机中心的向量，求模即为距离
            point_2_cam_center_vector = t_vector - point_vector
            distance = np.linalg.norm(point_2_cam_center_vector, ord=2)

            if show_flag:
                ret, image, _, corners_subpixel = get_chessboard_corners(image_path, row, col)

                # 绘制棋盘格角点，红色线头为起始点
                image = cv2.drawChessboardCorners(image, (row, col), corners_subpixel, ret)
                point_num = (point_col - 1) * row + (point_row - 1)
                position = (int(corners_subpixel[point_num][0][0]), int(corners_subpixel[point_num][0][1]))
                cv2.circle(image, position, 1, (255,255,255), 18)
                cv2.putText(image, '%.04fm'%(distance/1000), position, cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                cv2.resizeWindow("image", 1920, 1080)
                cv2.imshow('image',image)
                cv2.waitKey(0)

            return distance


'''
Others
'''
def others(self):
    '''图像处理相关的小功能，一两行能实现的
    '''
    images_path = glob.glob('game1/Clip1/*.jpg')
    images_path.sort(key = cmp_to_key(lambda a,b:int(os.path.basename(a)[:-4])-int(os.path.basename(b)[:-4])))
    
    # colos for display
    colors = (np.random.rand(32, 3) * 255).astype(dtype=np.int32)
    
    # 灰度图单通道转3通道
    image = np.stack((image,)*3, axis=-1)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 两图像叠加；dst = src1 * alpha + src2 * beta + gamma
    dst_image = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

    # 图像位运算按位取反bitwise_not()、按位与bitwise_and()、或bitwise_or()、异或bitwise_xor()
    dst_image = cv2.bitwise_and(image, mask_image)
    
    # scale image pixels value
    cv2.normalize(src_img, dst_img, 0, 255, cv2.NORM_MINMAX)
    
    # image slice，图像切片/裁剪，img[y : y+h, x:x+w]   [0:rows, 0:cols]
    roi_img = src_img[:, 21:106]
    
    # draw
    cv2.line(img, ptStart, ptEnd, point_color, thickness, lineType)
    cv2.circle(img, (int(center_x),int(center_y)), 1, (0,0,255), 8)
    cv2.rectangle(img, (int(left_top_x), int(left_top_y)), (int(right_bottom_x),int(right_bottom_y)), (255, 255, 255), 2)
    cv2.putText(img, cams_sn[cams_sn_index], (left_top_x, left_top_y), cv2.FONT_HERSHEY_COMPLEX,6,(0,255,0),5)
    cv2.polylines(image, [points_array], True, (0,0,0), 2)
    
    cv2.namedWindow('show', cv2.WINDOW_NORMAL)
    cv2.resizeWindow("show", 1224, 1080)
    
    # mouse callback
    cv2.setMouseCallback("show", on_EVENT_LBUTTONDOWN)
    cv2.imshow('show', img)
    key_num = cv2.waitKey(0)
    if chr(key_num) == 'r':
        print('press r')

    cv2.imwrite("./draw.jpg", img)