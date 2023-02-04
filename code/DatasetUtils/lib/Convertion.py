import os
import cv2
import math
import numpy as np

from .FileUtils import *


'''
控制台输出颜色转换
'''
def colorstr(*input):
    '''修改字符串输出时的字体颜色。Colors a string https://en.wikipedia.org/wiki/ANSI_escape_code
    或者使用rich库丰富控制台输出：如不同颜色输出、进度条、Log着色、表格、Markdown等

    Args:
        input: 颜色及字符串，如colorstr('blue', 'bold', 'underline', 'hello world')，注意用在fstring内的话需要把'改为"

    Returns:
        str, 带颜色的字符串
    '''
    *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])  # color arguments, string
    colors = {'black': '\033[30m',  # 字体颜色
              'red': '\033[31m',
              'green': '\033[32m',
              'yellow': '\033[33m',
              'blue': '\033[34m',
              'magenta': '\033[35m',
              'cyan': '\033[36m',
              'white': '\033[37m',
              'bright_black': '\033[90m',  # 高亮字体颜色
              'bright_red': '\033[91m',
              'bright_green': '\033[92m',
              'bright_yellow': '\033[93m',
              'bright_blue': '\033[94m',
              'bright_magenta': '\033[95m',
              'bright_cyan': '\033[96m',
              'bright_white': '\033[97m',
              'bg_red': '\033[41m',    # 背景颜色
              'bg_green': '\033[42m',
              'bg_yellow': '\033[43m',
              'bg_blue': '\033[44m',
              'bg_magenta': '\033[45m',
              'bg_cyan': '\033[46m',
              'bg_white': '\033[47m',
              'end': '\033[0m',  # 属性重置
              'bold': '\033[1m',  # 加粗
              'underline': '\033[4m',  # 下划线
              'twinkle': '\033[5m',  # 闪烁，vscode终端不支持，bash/zsh支持
              }
    return ''.join(colors[x] for x in args) + f'{string}' + colors['end']


'''
List、Dict、Set、Tuple常用数据结构格式转换
'''
def get_index_of_value_from_list(list, spec_value):
    '''从List中获取指定值对应的下标

    Args:
        list: list, 列表
        spec_value: type(list[0]), 指定值对应的下标

    Returns:
        index_list: list, 指定值对应的下标
    '''
    index_list = [index for index, value in enumerate(list) if value == spec_value]

    return index_list

def get_value_of_index_from_list(list, index_list):
    '''从List中获取指定下标对应的值

    Args:
        list: list, 列表
        index_list: list, 下标列表

    Returns:
        value_list: list, 指定下标对应的值
    '''
    value_list = [list[index] for index in index_list]

    return value_list

def get_mcount_value_index_from_list(list, mode='max'):
    '''从List中获取数量最多/最少(mcount: max/mincount)的值及其对应的下标

    Args:
        list: list, 列表
        mode: str, 'max'代表取最多数量的值；'min'代表取最少数量的值；

    Returns:
        m_value: type(list[0]), 最值
        m_count: int, 最值对应的数量
        index_list: list, 最值对应的下标
    '''
    from collections import Counter
    list_count = Counter(list)

    m_count = 0 if mode == 'max' else float('inf')
    for value in list_count:
        if (mode == 'max' and list_count[value] > m_count) or (mode == 'min' and list_count[value] < m_count):
            m_value = value
            m_count = list_count[value]
    index_list = get_index_of_value_from_list(list, m_value)

    return m_value, m_count, index_list

def map_dict_index_key(src_dict):
    '''构造字典中index-key与key-index的映射关系，index范围[0, len(src_dict)-1]

    Args:
        src_dict: dict, 字典

    Returns:
        index_key_dict: dict, index:key字典
        key_index_dict: dict, key:index字典
    '''
    _zip = zip(list(src_dict.keys()), list(range(len(src_dict))))
    key_index_dict = dict((key, value) for key, value in _zip)
    index_key_dict = {value:key for key, value in key_index_dict.items()}

    return index_key_dict, key_index_dict

def is_xyxy_valid(xyxy):
    '''判断box的宽和高是否小于0，0则返回False

    Args:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]

    Returns:
        bool, True代表合法，反之不合法
    '''
    width = xyxy[2] - xyxy[0]
    height = xyxy[3] - xyxy[1]
    if width <= 0 or height <= 0:
        return False
    else:
        return True

def xyxy2xywh_min(xyxy):
    '''[xmin, ymin, xmax, ymax]转为[xmin, ymin, w, h]

    Args:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]

    Returns:
        xywh_min: list, 格式[xmin, ymin, w, h]
    '''
    xmin = xyxy[0]
    ymin = xyxy[1]
    width = xyxy[2] - xyxy[0]
    height = xyxy[3] - xyxy[1]
    xywh_min = [xmin, ymin, width, height]

    return xywh_min

def xywh_min2xyxy(xyxy):
    '''[xmin, ymin, w, h]转为[xmin, ymin, xmax, ymax]

    Args:
        xywh_min: list, 格式[xmin, ymin, w, h]

    Returns:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]
    '''
    xmin = xyxy[0]
    ymin = xyxy[1]
    xmax = xmin + xyxy[2]
    ymax = ymin + xyxy[3]
    xyxy = [xmin, ymin, xmax, ymax]

    return xyxy

def xywh_center2xyxy(xywh):
    '''[x_center, y_center, w, h]转为[xmin, ymin, xmax, ymax]

    Args:
        xywh: list, 格式[x_center, y_center, w, h]

    Returns:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]
    '''
    xmin = int(xywh[0] - xywh[2] / 2)
    ymin = int(xywh[1] - xywh[3] / 2)
    xmax = int(xywh[0] + xywh[2] / 2)
    ymax = int(xywh[1] + xywh[3] / 2)
    xyxy = [xmin, ymin, xmax, ymax]

    return xyxy

def xyxy2xywh_center(xyxy):
    '''[xmin, ymin, xmax, ymax]转为[x_center, y_center, w, h]

    Args:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]

    Returns:
        xywh_center: list, 格式[x_center, y_center, w, h]
    '''
    x_center = int((xyxy[0] + xyxy[2]) / 2)
    y_center = int((xyxy[1] + xyxy[3]) / 2)
    width = xyxy[2] - xyxy[0]
    height = xyxy[3] - xyxy[1]
    xywh_center = [x_center, y_center, width, height]

    return xywh_center

def xyxy2points(xyxy):
    '''[xmin, ymin, xmax, ymax]转为[[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]，逆时针排序

    Args:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]

    Returns:
        points: list, 格式[[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]
    '''
    xmin, ymin, xmax, ymax = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
    points = [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]

    return points

def points2xyxy(points):
    '''[[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]逆时针排序，转为[xmin, ymin, xmax, ymax]

    Args:
        points: list, 格式[[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]

    Returns:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]
    '''
    xmin, ymin, xmax, ymax = points[0][0], points[0][1], points[2][0], points[2][1]
    xyxy = [xmin, ymin, xmax, ymax]

    return xyxy

def xy_pixel2xy_ratio(xy_pixel, width, height):
    '''xy_pixel[x1,y1,x2,y2,x3,y3,x4,y4]（像素表示[124,2763,422,899...]），转为xy_ratio[x1,y1,x2,y2,x3,y3,x4,y4]（比例表示[0.211,0.78334,0.1242,0.564...]）

    Args:
        xy_pixel: list, 像素表示的xy，格式[x1,y1,x2,y2,x3,y3,x4,y4]（像素表示[124,2763,422,899...]）
        width: int, 图像宽
        height: int, 图像高

    Returns:
        xy_ratio: list, 比例表示的xy，格式xy_ratio[x1,y1,x2,y2,x3,y3,x4,y4]（比例表示[0.211,0.78334,0.1242,0.564...]）
    '''
    x1,y1,x2,y2,x3,y3,x4,y4 = xy_pixel
    xy_ratio = [x1/width, y1/height, x2/width, y2/height, x3/width, y3/height, x4/width, y4/height]

    return xy_ratio

def get_xyxy_center(xyxy):
    '''[xmin, ymin, xmax, ymax]获取[x_center, y_center]

    Args:
        xyxy: list, 格式[xmin, ymin, xmax, ymax]

    Returns:
        center: list, 格式[x_center, y_center]
    '''
    return xyxy2xywh_center(xyxy)[:2]

def quadrilateral_points2rectangle_xyxy(quadrilateral_points):
    '''[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]逆时针排序，转为矩形box[xmin, ymin, xmax, ymax]

    Args:
        quadrilateral_points: list, 格式[[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]

    Returns:
        rectangle_xyxy: list, 格式[xmin, ymin, xmax, ymax]
    '''
    xmin = min(quadrilateral_points[0][0], quadrilateral_points[1][0], quadrilateral_points[2][0], quadrilateral_points[3][0])
    ymin = min(quadrilateral_points[0][1], quadrilateral_points[1][1], quadrilateral_points[2][1], quadrilateral_points[3][1])
    xmax = max(quadrilateral_points[0][0], quadrilateral_points[1][0], quadrilateral_points[2][0], quadrilateral_points[3][0])
    ymax = max(quadrilateral_points[0][1], quadrilateral_points[1][1], quadrilateral_points[2][1], quadrilateral_points[3][1])
    rectangle_xyxy = [xmin, ymin, xmax, ymax]

    return rectangle_xyxy

def quadrilateral_points2left_top_first_quadrilateral(quadrilateral_points, mode='left_top_euclidean'):
    '''凸四边形[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]。以左上角点为起始点，按顺时针排序，转为新四边形[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        确定左上角点，再与剩余三个点连线。连线后，如果存在一个点在线上方，一个点在线下方。那么线上的点为右上，线下的点为左下，连接点为右下
        
        定理：向量a×向量b（×为向量叉乘），若结果小于0，表示向量b在向量a的顺时针方向；若结果大于0，表示向量b在向量a的逆时针方向；若等于0，表示向量a与向量b平行
        跨立实验：如果线段CD的两个端点C和D，与另一条线段的一个端点（A或B，只能是其中一个）连成的向量，与向量AB做叉乘，
            若结果异号，表示C和D分别在直线AB的两边，若结果同号，则表示CD两点都在AB的一边，则肯定不相交。
        https://blog.csdn.net/qq_40733911/article/details/99121758

    Args:
        quadrilateral_points: list, 原始四边形。格式[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        mode: str, 若为'left_top_euclidean'，则认为离原点欧氏距离最小的为左上角；若为'left_top_position'，则先找最上的两个点，再找最左的点作为左上角（比如行人框）

    Returns:
        left_top_first_points: list, 左上角为起始点，顺时针排序的新四边形。格式[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    '''
    quadrilateral_points = np.array(quadrilateral_points)

    if mode == 'left_top_euclidean':
        # 认为离原点欧氏距离最小的为左上角
        origin_dist = np.sqrt(np.sum(np.square(quadrilateral_points),1))
        left_top_index = np.argmin(origin_dist)
    elif mode == 'left_top_position':
        # 先找最上的两个点，再找最左的点作为左上角（比如行人框）
        quadrilateral_points_for_lt = quadrilateral_points.copy()
        ymin2_index = np.argpartition(quadrilateral_points_for_lt[:,1], -2)
        ymin2_index = ymin2_index[-2:]
        quadrilateral_points_for_lt[ymin2_index] = [1e6, 1e6]
        left_top_index = np.argmin(quadrilateral_points_for_lt[:,0])
    
    # # 如果本来第一位就是左上角的点
    # if left_top_index == 0:
    #     return quadrilateral_points

    for index in range(quadrilateral_points.shape[0]):
        if index == left_top_index:
            continue
        remaining_points = list(range(quadrilateral_points.shape[0]))
        remaining_points.remove(index)
        remaining_points.remove(left_top_index)

        # 左上角点为A点
        line_AB = np.array((quadrilateral_points[index][0] - quadrilateral_points[left_top_index][0], quadrilateral_points[index][1] - quadrilateral_points[left_top_index][1]))
        line_AC = np.array((quadrilateral_points[remaining_points[0]][0] - quadrilateral_points[left_top_index][0], quadrilateral_points[remaining_points[0]][1] - quadrilateral_points[left_top_index][1]))
        line_AD = np.array((quadrilateral_points[remaining_points[1]][0] - quadrilateral_points[left_top_index][0], quadrilateral_points[remaining_points[1]][1] - quadrilateral_points[left_top_index][1]))
        cross_ABC = np.cross(line_AB, line_AC)
        cross_ABD = np.cross(line_AB, line_AD)
        # 如果两线段叉乘异号，代表两线段相交
        if cross_ABC * cross_ABD < 0:
            # 叉积小于0，代表AC在AB顺时针方向，因为图像坐标系原点在左上角，顺逆时针与人看的时候相反，所以C为右上角点
            if cross_ABC < 0:
                right_top_index = remaining_points[0]
                right_bottom_index = index
                left_bottom_index = remaining_points[1]
            else:
                right_top_index = remaining_points[1]
                right_bottom_index = index
                left_bottom_index = remaining_points[0]

    left_top_first_points = quadrilateral_points[[left_top_index, right_top_index, right_bottom_index, left_bottom_index], :]

    return left_top_first_points

def head_shoulder_box2person_box(head_shoulder_box, ratio, height, width=1920):
    '''head_shoulder_box[xmin, ymin, xmax, ymax]高扩大为ratio倍，转为person_box[xmin, ymin, xmax, ymax]

    Args:
        head_shoulder_box: list, 头肩框，格式[xmin, ymin, xmax, ymax]
        ratio: float, 扩大比例，一般侧视角为4.0，顶视角为3.0
        height: int, 图像高，防止person_box越界
        width: int, 图像宽，防止person_box越界

    Returns:
        person_box: list, 格式[xmin, ymin, xmax, ymax]
    '''
    box_height = xyxy2xywh_center(head_shoulder_box)[3]
    person_box = [head_shoulder_box[0], head_shoulder_box[1], head_shoulder_box[2], min(int(head_shoulder_box[3] + box_height * (ratio - 1)), height)]

    # 关键点提标用
    bbox_xywh_center = xyxy2xywh_center(person_box)
    bbox_xywh_center[2] = bbox_xywh_center[2] * (1 + 0.8)
    bbox_xywh_center[3] = bbox_xywh_center[3] * (1 + 0.15)
    extend_box = xywh_center2xyxy(bbox_xywh_center)
    person_box = [max(0,extend_box[0]),max(0,extend_box[1]),min(extend_box[2],width),min(extend_box[3],height)]

    return person_box

def get_rotated_person_box(HeadShoulderBox, person_hip_mid_keypoint, extend_ratio_width, extend_ratio_height):
    '''利用行人头肩框与臀部中心点，得到旋转行人框。目前是以臀部为中心点，头肩-臀部中心点距离为高的基准

    Args:
        person_headshoulder_mid_keypoint: list, 头肩中心点[x, y]
        person_hip_mid_keypoint: list, 臀部中心点[x, y]
        extend_ratio_width: float, 宽扩边比例。如0.4，则扩边1.4倍
        extend_ratio_height: float, 高扩边比例。如0.4，则扩边1.4倍

    Returns:
        rotated_person_box: list, 旋转行人框
        rotated_person_box_size: tuple, 旋转行人框的尺寸(width, height)
    '''
    from .Math import calcu_vector_angle_np, rotated_rectangle
    HeadShoulderBox_xywh = xyxy2xywh_center(HeadShoulderBox)
    person_headshoulder_mid_keypoint = HeadShoulderBox_xywh[:2]
    headshoulder_width = HeadShoulderBox_xywh[2]
    
    rotated_person_box_width = headshoulder_width * (1 + extend_ratio_width)
    rotated_person_box_height = math.sqrt(math.pow(HeadShoulderBox_xywh[0] - person_hip_mid_keypoint[0], 2) + \
        math.pow(HeadShoulderBox_xywh[1] - person_hip_mid_keypoint[1], 2)) * 2 * (1 + extend_ratio_height)
    
    # 向量a应该为[0, -1], 因为图像左上角为原点，且图像坐标系与直角坐标系顺逆时针关系刚好相反
    vector_a = np.array([0, -1])
    vector_b = np.array([person_headshoulder_mid_keypoint[0] - person_hip_mid_keypoint[0], \
                                                person_headshoulder_mid_keypoint[1] - person_hip_mid_keypoint[1]])
    rotated_person_box_angle = -calcu_vector_angle_np(vector_a, vector_b, mode='degree')
    rotated_person_box_size = (rotated_person_box_width, rotated_person_box_height)
    rotated_person_box = rotated_rectangle(person_hip_mid_keypoint, rotated_person_box_size, rotated_person_box_angle)

    return rotated_person_box, rotated_person_box_size

def gen_nonoverlap_box(image_shape, box_image_shape, current_boxes, roi):
    '''在roi区域内，生成与现有框不重叠的新框

    Args:
        image_shape: tuple, (height, width, channel)，原图尺寸
        box_image_shape: tuple, (height, width, channel)，新框尺寸
        current_boxes: list, 现有框
        roi: list, roi区域[x1,y1,x2,y2]
    
    Returns:
        nonoverlap_box: list, 非重叠的新框
        all_boxes: list, 添加新框后的所有框
    '''
    current_boxes_image = np.zeros(image_shape, dtype=np.uint8) * 255
    invalid_flag = True

    for box in current_boxes:
        cv2.rectangle(current_boxes_image, (int(box[0]), int(box[1])), (int(box[2]),int(box[3])), (255, 255, 255), -1)

    while invalid_flag:
        box_image = np.zeros(image_shape, dtype=np.uint8) * 255
        random_x1, random_y1 = random.randint(roi[0], roi[2] - box_image_shape[1]), random.randint(roi[1], roi[3] - box_image_shape[0])
        cv2.rectangle(box_image, (int(random_x1), int(random_y1)), (int(random_x1 + box_image_shape[1]),int(random_y1 + box_image_shape[0])), (255, 255, 255), -1)
        merge_image = cv2.bitwise_and(current_boxes_image, box_image)
        invalid_flag = np.any(merge_image)

    new_box = [random_x1, random_y1, random_x1 + box_image_shape[1], random_y1 + box_image_shape[0]]
    current_boxes.append(new_box)
    
    return new_box, current_boxes


'''
文件格式转换
'''
class YoloVocConvert:
    """YoloVoc标注转换类
    """
    def yolo2voc(self, root, classes, width, height):
        '''YOLO格式（路径'Annotations/'）转为VOC格式（路径'Annotations_XML/'）
        
        Args:
            width: int, 图像宽
            height: int, 图像高
        '''
        yolo_path = root + '/Annotations/'
        voc_path = root + '/Annotations_XML/'

        txt_files = os.listdir(yolo_path)
        for index, txt_file in enumerate(txt_files):
            print(index, txt_file)
            os.makedirs(voc_path, exist_ok=True)
            
            txt_data = read_yolo_txt(yolo_path + txt_file, width, height)
            save_xml(txt_data, voc_path + txt_file.replace('.txt', '.xml'), width, height, classes)

    def voc_box_2_yolo_box(self, size, box, mode = 'std'):
        '''voc_box转为yolo_box
        
        Args:
            size: tuple, 宽高尺寸(width, height)
            box: list, voc格式检测框[xmin, ymin, xmax, ymax]
            mode: str, 'std'代表只包含检测框；
                        'with_hip_mid_keypoint'代表只包含检测框与臀部关键点；

        Returns:
            box: list, yolo格式检测框[x_center, y_center, width, height]，均为归一化值
        '''
        dw = 1./size[0]
        dh = 1./size[1]

        x = (box[0] + box[2])/2.0
        y = (box[1] + box[3])/2.0
        # abs防止检测框xymin-xymax位置放反
        w = abs(box[2] - box[0])
        h = abs(box[3] - box[1])
        
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh

        if mode == 'std':
            return (x, y, w, h)
        elif mode == 'with_hip_mid_keypoint':
            if box[4] == -1 and box[5] == -1:
                hip_mid_x = -1
                hip_mid_y = -1
            else:
                hip_mid_x = box[4] * dw
                hip_mid_y = box[5]* dh
            return (x, y, w, h, hip_mid_x, hip_mid_y)

    def voc2yolo(self, root, classes, mode='std'):
        '''VOC格式（路径'Annotations_XML/'）转为YOLO格式（路径'Annotations/'）

        Args:
            root: str, 根目录路径
            mode: str, 'std'代表只包含类别与检测框；
                        'with_hip_mid_keypoint'代表只包含类别、检测框与臀部关键点；
        '''
        yolo_path = root + '/Annotations/'
        voc_path = root + '/Annotations_XML/'

        xml_files = os.listdir(voc_path)
        for index, xml_file in enumerate(xml_files):
            print(index, len(xml_files), xml_file)
            os.makedirs(yolo_path, exist_ok=True)
            txt_file = open(yolo_path + xml_file.replace('.xml', '.txt'), 'w')

            if mode == 'std':
                xml_data = read_xml(voc_path + xml_file)
            elif mode == 'with_hip_mid_keypoint':
                xml_data = read_xml(voc_path + xml_file, 'with_hip_mid_keypoint')
            width = int(xml_data['size'][0])
            height = int(xml_data['size'][1])
            for box in xml_data['bndboxes']:
                cls_name = box[4]
                cls_id = classes.index(cls_name)

                if mode == 'std':
                    yolo_box = self.voc_box_2_yolo_box((width, height), box[:4])
                elif mode == 'with_hip_mid_keypoint':
                    yolo_box = self.voc_box_2_yolo_box((width, height), box[:4] + box[5:], 'with_hip_mid_keypoint')
                txt_file.write(str(cls_id) + " " + " ".join([str(element) for element in yolo_box]) + '\n')

            txt_file.close()


class VocCocoConvert:
    """VocCoco标注转换类
    """
    def coco2voc(self):
        pass

    def voc2coco(self, classes, txt_path, save_coco_json_path):
        '''VOC格式（路径'Annotations_XML/'）+train/test.txt转为COCO格式（路径'./label_coco.json'）
        注意coco的bbox格式为: [xmin, ymin, w, h]！！！！！！而非[xmin, ymin, xmax, ymax]
        
        Args:
            classes: list, 类别名称
            txt_path: str, train/val/test.txt
            save_coco_json_path: str, 保存coco格式json文件路径
        '''
        categories, images, annotations = [], [], []

        # read train/val/test.txt
        images_list = read_txt(txt_path)

        # build categories
        for index, category in enumerate(classes):
            category_info = {}
            category_info['supercategory'] = category
            category_info['name'] = category
            category_info['id'] = index
            categories.append(category_info)

        # build images, annotations
        box_id = 0
        for image_id, image_file in enumerate(images_list):
            print(image_id, image_file)
            image_info, anno_info = {}, []
            xml_data = read_xml(image_file.replace('JPEGImages', 'Annotations_XML').replace('.jpg', '.xml'))
            
            image_info['file_name'] = xml_data['file_name']
            image_info['width'] = xml_data['size'][0]
            image_info['height'] = xml_data['size'][1]
            image_info['id'] = image_id
            images.append(image_info)

            for box in xml_data['bndboxes']:
                box_anno = {}
                box_anno['image_id'] =  image_id
                box_anno['category_id'] = classes.index(box[4])
                # box_anno['category_id'] = 0
                box_anno['bbox'] = xyxy2xywh_min(box[:4])
                box_anno['id'] = box_id
                box_anno['area'] = (box[2] - box[0]) * (box[3] - box[1])
                box_anno['iscrowd'] = 0
                anno_info.append(box_anno)
                box_id += 1
            annotations.extend(anno_info)

        save_json(save_coco_json_path, {'images': images, 'categories': categories, 'annotations': annotations})




def coco2yolo(json_path,save_path):
    
    def convert(size, box):
        dw = 1. / (size[0])
        dh = 1. / (size[1])
        x = box[0] + box[2] / 2.0
        y = box[1] + box[3] / 2.0
        w = box[2]
        h = box[3]
    
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
    
        return (x, y, w, h)

    json_file = json_path           # COCO Object Instance 类型的标注
    ana_txt_save_path = save_path     # 保存的路径

    data = json.load(open(json_file, 'r'))
    if not os.path.exists(ana_txt_save_path):
        os.makedirs(ana_txt_save_path)
    
    id_map = {} # coco数据集的id不连续！重新映射一下再输出！
    for i, category in enumerate(data['categories']): 
        id_map[category['id']] = i

    # 通过事先建表来降低时间复杂度
    max_id = 0
    for img in data['images']:
        max_id = max(max_id, img['id'])
    # 注意这里不能写作 [[]]*(max_id+1)，否则列表内的空列表共享地址

    img_ann_dict = [[] for i in range(max_id+1)] 
    for i, ann in enumerate(data['annotations']):
        img_ann_dict[ann['image_id']].append(i)

    for img in tqdm(data['images']):
        
        filename = img["file_name"]
        img_width = img["width"]
        img_height = img["height"]
        img_id = img["id"]
        head, tail = os.path.splitext(filename)
        ana_txt_name = head + ".txt"  # 对应的txt名字，与jpg一致
        f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')

        # 这里可以直接查表而无需重复遍历
        for ann_id in img_ann_dict[img_id]:
            ann = data['annotations'][ann_id]
            box = convert((img_width, img_height), ann["bbox"])
            f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], box[0], box[1], box[2], box[3]))
        f_txt.close()