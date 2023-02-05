import copy
import cv2
import numpy as np



def get_color_map(nums=25):
    colors = [
        "#FF0000", "#FF7F50", "#B0171F", "#872657", "#FF00FF",
        "#FFFF00", "#FF8000", "#FF9912", "#DAA569", "#FF6100",
        "#0000FF", "#3D59AB", "#03A89E", "#33A1C9", "#00C78C",
        "#00FF00", "#385E0F", "#00C957", "#6B8E23", "#2E8B57",
        "#A020F0", "#8A2BE2", "#A066D3", "#DA70D6", "#DDA0DD"]
    colors = colors * int(np.ceil(nums / len(colors)))
    return colors

def convert_color_map(color, colorType="BGR"):
    '''
    :param color:
    :param colorType:
    :return:
    '''
    assert (len(color) == 7 and color[0] == "#"), "input color error:color={}".format(color)
    R = color[1:3]
    G = color[3:5]
    B = color[5:7]

    R = int(R, 16)
    G = int(G, 16)
    B = int(B, 16)
    if colorType == "BGR":
        return (B, G, R)
    elif colorType == "RGB":
        return (R, G, B)
    else:
        assert "colorType error "
        
# def set_class_set(class_set=set()):
#     global CLASS_SET
#     CLASS_SET = class_set

def get_color(id):
    color = convert_color_map(COLOR_MAP[id])
    return color


COLOR_MAP = get_color_map(200)


def cv_show_image(title, image, type='rgb', waitKey=0):
    '''
    调用OpenCV显示RGB图片
    :param title: 图像标题
    :param image: 输入RGB图像
    :param type:'rgb' or 'bgr'
    :return:
    '''
    img = copy.copy(image)
    channels = img.shape[-1]
    if channels == 3 and type == 'rgb':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 将BGR转为RGB
    if title:
        cv2.imshow(title, img)
        cv2.waitKey(waitKey)



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
    '''
    将label_list和prob_list拼接在一起，以便显示
    :param label_list:
    :param prob_list:
    :return:
    '''
    info = [str(l) + ":" + str(p)[:5] for l, p in zip(label_list, prob_list)]
    return info

def draw_image_detection_bboxes(rgb_image, bboxes, probs, labels, color=None):
    '''
    :param title:
    :param rgb_image:
    :param bboxes:  [[x1,y1,x2,y2],[x1,y1,x2,y2]]
    :param probs:
    :param labels:
    :return:
    '''
    class_set = list(CLASS_SET)
    if not class_set:
        class_set = list(set(labels))
    boxes_name = combile_label_prob(labels, probs)
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    # color_map=list(matplotlib.colors.cnames.values())
    # color_map=list(reversed(color_map))
    set_color = color
    for l, name, box in zip(labels, boxes_name, bboxes):
        if not color:
            cls_id = class_set.index(l)
            set_color = get_color(cls_id)
        box = [int(b) for b in box]
        # cv2.rectangle(bgr_image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2, 8, 0)
        # cv2.putText(bgr_image, name, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
        # cv2.rectangle(bgr_image, (box[0], box[1]), (box[2], box[3]), color, 2, 8, 0)
        # cv2.putText(bgr_image, str(name), (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, thickness=2)
        draw_bbox_text(bgr_image, box, set_color, name, drawType="custom")
    # cv2.imshow(title, bgr_image)
    # cv2.waitKey(0)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    return rgb_image




def draw_bbox_text(img, bbox, color, name, drawType="custom", top=True):
    """
    :param img:
    :param bbox:
    :param color:
    :param name:
    :param drawType:
    :param top:
    :return:
    """
    if drawType == "simple":
        fontScale = 0.6
        thickness = 1
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness, 8, 0)
        cv2.putText(img, str(name), (bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness)
    elif drawType == "custom":
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        # draw score roi
        # fontScale = 0.4
        fontScale = 0.6
        thickness = 1
        text_size, baseline = cv2.getTextSize(str(name), cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness)
        if top:
            text_loc = (bbox[0], bbox[1] - text_size[1])
        else:
            # text_loc = (bbox[0], bbox[3])
            # text_loc = (bbox[2], bbox[3] - text_size[1])
            text_loc = (bbox[2], bbox[1] + text_size[1])

        cv2.rectangle(img, (text_loc[0] - 2 // 2, text_loc[1] - 2 - baseline),
                      (text_loc[0] + text_size[0], text_loc[1] + text_size[1]), color, -1)
        # draw score value
        cv2.putText(img, str(name), (text_loc[0], text_loc[1] + baseline), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                    (255, 255, 255), thickness, 8)
    return img


def show_boxList(win_name, boxList, rgb_image, waitKey=0):
    '''
    [xmin,ymin,xmax,ymax]
    :param win_name:
    :param boxList:
    :param rgb_image:
    :return:
    '''
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    for item in boxList:
        name = item["label"]
        xmin = item["xtl"]
        xmax = item["xbr"]
        ymin = item["ytl"]
        ymax = item["ybr"]
        # box=[xbr,ybr,xtl,ytl]
        box = [xmin, ymin, xmax, ymax]
        box = [int(float(b)) for b in box]
        cv2.rectangle(bgr_image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2, 8, 0)
        cv2.putText(bgr_image, name, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
    # cv2.imshow(title, bgr_image)
    # cv2.waitKey(0)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    if win_name:
        cv_show_image(win_name, rgb_image, waitKey=waitKey)
    return rgb_image


def draw_points_text(img, points, texts=None, color=(0, 0, 255), drawType="custom"):
    '''

    :param img:
    :param points:
    :param texts:
    :param color:
    :param drawType: custom or simple
    :return:
    '''
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
                image = draw_points_text(image, [point], texts=str(i), color=point_color, drawType="simple")
    return image


def draw_text(img, point, text, bg_color=(255, 0, 0), drawType="custom"):
    '''
    在目标点输出一行文字,并可以对文字画框
    :param img:
    :param point:
    :param text:
    :param drawType: custom or simple
    :return:
    '''
    fontScale = 0.4
    thickness = 5
    text_thickness = 1
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    # fontFace=cv2.FONT_HERSHEY_SIMPLEX
    if drawType == "custom":
        text_size, baseline = cv2.getTextSize(str(text), fontFace, fontScale, thickness)
        text_loc = (point[0], point[1] + text_size[1])
        cv2.rectangle(img, (text_loc[0] - 2 // 2, text_loc[1] - 2 - baseline),
                      (text_loc[0] + text_size[0], text_loc[1] + text_size[1]), bg_color, -1)
        # draw score value
        cv2.putText(img, str(text), (text_loc[0], text_loc[1] + baseline), fontFace, fontScale,
                    (255, 255, 255), text_thickness, 8)
    elif drawType == "simple":
        cv2.putText(img, str(text), point, fontFace, 0.5, (255, 0, 0))
    return img

def draw_text_line(img, point, text_line: str, bg_color=(255, 0, 0), drawType="custom"):
    '''
    在目标点输出多行文字
    :param img:
    :param point:
    :param text:
    :param drawType: custom or custom
    :return:
    '''
    fontScale = 0.4
    thickness = 5
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    # fontFace=cv2.FONT_HERSHEY_SIMPLEX
    text_line = text_line.split("\n")
    # text_size, baseline = cv2.getTextSize(str(text_line), fontFace, fontScale, thickness)
    text_size, baseline = cv2.getTextSize(str(text_line), fontFace, fontScale, thickness)
    for i, text in enumerate(text_line):
        if text:
            draw_point = [point[0], point[1] + (text_size[1] + 2 + baseline) * i]
            img = draw_text(img, draw_point, text, bg_color, drawType)
    return img


def draw_key_point_in_image(image, key_points, pointline=[]):
    '''
    :param key_points: list(ndarray(19,2)) or ndarray(n_person,19,2)
    :param image:
    :param pointline: `auto`->pointline = circle_line(len(points), iscircle=True)
    :return:
    '''
    img = copy.deepcopy(image)
    person_nums = len(key_points)
    for person_id, points in enumerate(key_points):
        if points is None:
            continue
        color = get_color(person_id)
        img = draw_point_line(img, points, pointline, color, check=True)
    return img


def draw_point_line(img, points, pointline=[], color=(0, 255, 0), texts=None, drawType="simple", check=True):
    '''
    在图像中画点和连接线
    :param img:
    :param points: 点列表
    :param pointline: `auto`->pointline = circle_line(len(points), iscircle=True)
    :param color:
    :param texts:
    :param drawType: simple or custom
    :param check:
    :return:
    '''
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
    '''
    产生连接线的点,用于绘制连接线
    points_line=circle_line(len(points),iscircle=True)
    >> [(0, 1), (1, 2), (2, 0)]
    :param num_point:
    :param iscircle: 首尾是否相连
    :return:
    '''
    start = 0
    end = num_point - 1
    points_line = []
    for i in range(start, end + 1):
        if i == end and iscircle:
            points_line.append([end, start])
        elif i != end:
            points_line.append([i, i + 1])
    return points_line
