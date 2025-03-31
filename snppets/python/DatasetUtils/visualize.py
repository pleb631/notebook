import copy
import cv2
import numpy as np


class colorMap:
    palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
    
    @staticmethod
    def color(label):
        
        color = [int((p * (label ** 2 - label + 1)) % 255) for p in colorMap.palette]
        return color
    
    @staticmethod
    def hex2rgb(h):
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb2hex(rgb):
        rgb = rgb.split(',')
        color = '#'
        for i in rgb:
            num = int(i)
            color += str(hex(num))[-2:].replace('x', '0').upper()
        return color

def label_colormap(n_label=10):
    """Label colormap.

    Parameters
    ----------
    n_labels: int
        Number of labels (default: 256).
    value: float or int
        Value scale or value of label color in HSV space.

    Returns
    -------
    cmap: numpy.ndarray, (N, 3), numpy.uint8
        Label id to colormap.

    """

    def bitget(byteval, idx):
        shape = byteval.shape + (8,)
        return np.unpackbits(byteval).reshape(shape)[..., -1 - idx]

    i = np.arange(n_label, dtype=np.uint8)
    r = np.full_like(i, 0)
    g = np.full_like(i, 0)
    b = np.full_like(i, 0)

    i = np.repeat(i[:, None], 8, axis=1)
    i = np.right_shift(i, np.arange(0, 24, 3)).astype(np.uint8)
    j = np.arange(8)[::-1]
    r = np.bitwise_or.reduce(np.left_shift(bitget(i, 0), j), axis=1)
    g = np.bitwise_or.reduce(np.left_shift(bitget(i, 1), j), axis=1)
    b = np.bitwise_or.reduce(np.left_shift(bitget(i, 2), j), axis=1)

    cmap = np.stack((r, g, b), axis=1).astype(np.uint8)

    return cmap

def get_color_map_list(num_classes, custom_color=None):
    """
    Returns the color map for visualizing the segmentation mask,
    which can support arbitrary number of classes.

    Args:
        num_classes (int): Number of classes.
        custom_color (list, optional): Save images with a custom color map. Default: None, use paddleseg's default color map.

    Returns:
        (list). The color map.
    """

    num_classes += 1
    color_map = num_classes * [0, 0, 0]
    for i in range(num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= ((lab >> 0) & 1) << (7 - j)
            color_map[i * 3 + 1] |= ((lab >> 1) & 1) << (7 - j)
            color_map[i * 3 + 2] |= ((lab >> 2) & 1) << (7 - j)
            j += 1
            lab >>= 3
    color_map = color_map[3:]

    if custom_color:
        color_map[: len(custom_color)] = custom_color
    return color_map


##检测


def draw_image_boxes(bgr_image, boxes_list, color=(0, 0, 255)):
    """_summary_

    Args:
        bgr_image (_type_):
        boxes_list (_type_): [[x1y1x2y2]...]
        color (tuple, optional): . Defaults to (0, 0, 255).

    Returns:
        _type_: img
    """
    thickness = 2
    for box in boxes_list:
        x1, y1, x2, y2 = box
        point1 = (int(x1), int(y1))
        point2 = (int(x2), int(y2))
        cv2.rectangle(bgr_image, point1, point2, color, thickness=thickness)
    return bgr_image


def combile_label_prob(label_list, prob_list):
    """
    将label_list和prob_list拼接在一起，以便显示
    :param label_list:
    :param prob_list:
    :return:
    """
    return [f"{str(l)}:{str(p)[:5]}" for l, p in zip(label_list, prob_list)]


def draw_bboxes_and_labels(rgb_image, bboxes, probs, labels, color=None):
    """
    :param title:
    :param rgb_image:
    :param bboxes:  [[x1,y1,x2,y2],[x1,y1,x2,y2]]
    :param probs:
    :param labels:
    :return:
    """
    class_set = list(set(labels))
    boxes_name = combile_label_prob(labels, probs)
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    set_color = color
    for l, name, box in zip(labels, boxes_name, bboxes):
        if not color:
            cls_id = class_set.index(l)
            set_color = COLOR_MAP(cls_id)
        box = [int(b) for b in box]
        draw_bbox_text(bgr_image, box, set_color, name, drawType="custom")

    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    return rgb_image


def draw_bbox_text(img, bbox, color, name, drawType="custom", top=True):
    """
    :param img:
    :param bbox:[x1y1x2y2]
    :param color:
    :param name:
    :param drawType:
    :param top:
    :return:
    """
    if drawType == "simple":
        fontScale = 0.6
        thickness = 1
        cv2.rectangle(
            img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness, 8, 0
        )
        cv2.putText(
            img,
            str(name),
            (bbox[0], bbox[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale,
            color,
            thickness,
        )
    elif drawType == "custom":
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)

        fontScale = 0.6
        thickness = 1
        text_size, baseline = cv2.getTextSize(
            str(name), cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness
        )
        if top:
            text_loc = (bbox[0], bbox[1] - text_size[1])
        else:
            text_loc = (bbox[2], bbox[1] + text_size[1])

        cv2.rectangle(
            img,
            (text_loc[0] - 1, text_loc[1] - 2 - baseline),
            (text_loc[0] + text_size[0], text_loc[1] + text_size[1]),
            color,
            -1,
        )
        # draw score value
        cv2.putText(
            img,
            str(name),
            (text_loc[0], text_loc[1] + baseline),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale,
            (255, 255, 255),
            thickness,
            8,
        )
    return img



##关键点


def draw_points_text(img, points, texts=None, color=(0, 0, 255), drawType="custom"):
    """

    :param img:
    :param points:
    :param texts:
    :param color:
    :param drawType: custom or simple
    :return:
    """
    thickness = 5
    if texts is None:
        texts = [""] * len(points)
    for point, text in zip(points, texts):
        point = (int(point[0]), int(point[1]))
        cv2.circle(img, point, thickness, color, -1)
        draw_text(img, point, text, bg_color=color, drawType=drawType)
    return img


def draw_landmark(image, landmarks_list, point_color=(0, 0, 255), vis_id=False):
    image = copy.copy(image)
    point_size = 1
    thickness = 4  # 可以为 0 、4、8
    for landmarks in landmarks_list:
        for i, landmark in enumerate(landmarks):
            # 要画的点的坐标
            point = (int(landmark[0]), int(landmark[1]))
            cv2.circle(image, point, point_size, point_color, thickness)
            if vis_id:
                image = draw_points_text(
                    image, [point], texts=str(i), color=point_color, drawType="simple"
                )
    return image


def draw_text(img, point, text, bg_color=(255, 0, 0), drawType="custom"):
    """
    在目标点输出一行文字,并可以对文字画框
    :param img:
    :param point:
    :param text:
    :param drawType: custom or simple
    :return:
    """
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    # fontFace=cv2.FONT_HERSHEY_SIMPLEX
    if drawType == "custom":
        fontScale = 0.4
        thickness = 5
        text_size, baseline = cv2.getTextSize(str(text), fontFace, fontScale, thickness)
        text_loc = (point[0], point[1] + text_size[1])
        cv2.rectangle(
            img,
            (text_loc[0] - 1, text_loc[1] - 2 - baseline),
            (text_loc[0] + text_size[0], text_loc[1] + text_size[1]),
            bg_color,
            -1,
        )
        text_thickness = 1
        # draw score value
        cv2.putText(
            img,
            str(text),
            (text_loc[0], text_loc[1] + baseline),
            fontFace,
            fontScale,
            (255, 255, 255),
            text_thickness,
            8,
        )
    elif drawType == "simple":
        cv2.putText(img, str(text), point, fontFace, 0.5, (255, 0, 0))
    return img


def draw_text_line(img, point, text_line: str, bg_color=(255, 0, 0), drawType="custom"):
    """
    在目标点输出多行文字
    :param img:
    :param point:
    :param text:
    :param drawType: custom or custom
    :return:
    """
    fontScale = 0.4
    thickness = 5
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    # fontFace=cv2.FONT_HERSHEY_SIMPLEX
    text_line = text_line.split("\n")
    # text_size, baseline = cv2.getTextSize(str(text_line), fontFace, fontScale, thickness)
    text_size, baseline = cv2.getTextSize(
        str(text_line), fontFace, fontScale, thickness
    )
    for i, text in enumerate(text_line):
        if text:
            draw_point = [point[0], point[1] + (text_size[1] + 2 + baseline) * i]
            img = draw_text(img, draw_point, text, bg_color, drawType)
    return img




def draw_point_line(img, points, pointline=None, color=(0, 255, 0), texts=None, drawType="simple", check=True):
    """
    在图像中画点和连接线
    :param img:
    :param points: 点列表
    :param pointline: `auto`->pointline = circle_line(len(points), iscircle=True)
    :param color:
    :param texts:
    :param drawType: simple or custom
    :param check:
    :return:
    """
    if pointline is None:
        pointline = []
    points = np.asarray(points, dtype=np.int32)
    image = copy.copy(img)
    line_thickness = 1
    if texts is None:
        texts = list(range(len(points)))
    image = draw_points_text(image, points, texts=texts, color=color, drawType=drawType)
    if pointline == "auto":
        pointline = circle_line(len(points), iscircle=True)
    for point_index in pointline:
        point1 = tuple(points[point_index[0]])
        point2 = tuple(points[point_index[1]])
        if check:
            if point1 is None or point2 is None:
                continue
            if sum(point1) <= 0 or sum(point2) <= 0:
                continue
        cv2.line(image, point1, point2, color, line_thickness)  # 绿色，3个像素宽度
    return image


def circle_line(num_point, iscircle=True):
    """
    产生连接线的点,用于绘制连接线
    points_line=circle_line(len(points),iscircle=True)
    >> [(0, 1), (1, 2), (2, 0)]
    :param num_point:
    :param iscircle: 首尾是否相连
    :return:
    """
    start = 0
    end = num_point - 1
    points_line = []
    for i in range(start, end + 1):
        if i == end and iscircle:
            points_line.append([end, start])
        elif i != end:
            points_line.append([i, i + 1])
    return points_line


# 分割图


def visualize(image, result, color_map, weight=0.6):
    """
    Convert predict result to color image, and save added image.

    Args:
        image (str): The path of origin image.
        result (np.ndarray): The predict result of image.
        color_map (list): The color used to save the prediction results.
        save_dir (str): The directory for saving visual image. Default: None.
        weight (float): The image weight of visual image, and the result weight is (1 - weight). Default: 0.6

    Returns:
        vis_result (np.ndarray): If `save_dir` is None, return the visualized result.
    """

    color_map = [color_map[i : i + 3] for i in range(0, len(color_map), 3)]
    color_map = np.array(color_map).astype("uint8")
    # Use OpenCV LUT for color mapping
    c1 = cv2.LUT(result, color_map[:, 0])
    c2 = cv2.LUT(result, color_map[:, 1])
    c3 = cv2.LUT(result, color_map[:, 2])
    pseudo_img = np.dstack((c3, c2, c1))

    im = cv2.imread(image)
    return cv2.addWeighted(im, weight, pseudo_img, 1 - weight, 0)


def get_pseudo_color_map(pred, color_map=None):
    """
    Get the pseudo color image.

    Args:
        pred (numpy.ndarray): the origin predicted image.
        color_map (list, optional): the palette color map. Default: None,
            use paddleseg's default color map.

    Returns:
        (numpy.ndarray): the pseduo image.
    """
    pred_mask = PIL.Image.fromarray(pred.astype(np.uint8), mode="P")
    if color_map is None:
        color_map = get_color_map_list(256)
    pred_mask.putpalette(color_map)
    return pred_mask



