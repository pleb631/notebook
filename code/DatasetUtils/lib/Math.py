import math
import cmath
import itertools
import numpy as np
import torch
# import torch

from .Convertion import xyxy2xywh, xywh2xyxy, get_xyxy_center


class Distance:
    """距离与相似度类"""

    def calcu_euclidean_distance(self, vector_a, vector_b):
        """计算向量之间的欧式距离

        Args:
            vector_a: np.array/list, 向量a
            vector_b: np.array/list, 向量b

        Returns:
            distance: float, 向量之间的欧式距离
        """
        # return np.sqrt(np.sum(np.square(vector_a - vector_b)))
        return np.linalg.norm(np.asarray(vector_a) - np.asarray(vector_b))

    def calcu_iou(self, box1, box2, mode="iou"):
        """计算两个box之间的iou

        Args:
            box1: list, [xmin1, ymin1, xmax1, ymax1]
            box2: list, [xmin2, ymin2, xmax2, ymax2]
            mode: str, 'iou'代表iou
                        'diou'代表diou

        Returns:
            iou: float, 交并比
        """
        xmin1, ymin1, xmax1, ymax1 = box1
        xmin2, ymin2, xmax2, ymax2 = box2

        # 计算每个矩形的面积
        s1 = (xmax1 - xmin1) * (ymax1 - ymin1)
        s2 = (xmax2 - xmin2) * (ymax2 - ymin2)

        # 计算相交矩形及面积
        xmin = max(xmin1, xmin2)
        ymin = max(ymin1, ymin2)
        xmax = min(xmax1, xmax2)
        ymax = min(ymax1, ymax2)
        w = max(0, xmax - xmin)
        h = max(0, ymax - ymin)
        area = w * h

        iou = area / (s1 + s2 - area)

        if mode == "diou":
            c_xmin = min(xmin1, xmin2)
            c_ymin = min(ymin1, ymin2)
            c_xmax = max(xmax1, xmax2)
            c_ymax = max(ymax1, ymax2)
            c_center_len = self.calcu_euclidean_distance(
                get_xyxy_center(box1), get_xyxy_center(box2)
            )
            c_diagonal_len = self.calcu_euclidean_distance(
                [c_xmin, c_ymin], [c_xmax, c_ymax]
            )

            diou = iou - math.pow(c_center_len, 2) / math.pow(c_diagonal_len, 2)
            iou = diou

        return iou

    def calcu_boxes_iou_matrix(
        self, boxes, iou_mode="iou", mode="diagonal", extend_params=None
    ):
        """计算多个box之间的iou矩阵

        Args:
            boxes: list, [[xmin1, ymin1, xmax1, ymax1],...]
            iou_mode: str, 'iou'代表iou
                            'diou'代表diou
            mode: str, 'diagonal'代表为对角矩阵，即(box1, box3)的iou和(box3, box1)的iou相同；
                        'extend'代表先对当前box扩边，再计算与其他box的iou；
            extend_params: tuple, (width, height, extend_ratio_width, extend_ratio_height)图像宽高和宽高扩边比例

        Returns:
            iou_matrix: np.array, iou矩阵
        """
        iou_matrix = np.zeros((len(boxes), len(boxes)), float)

        for i in range(len(boxes)):
            if mode == "diagonal":
                for j in range(i + 1, len(boxes)):
                    iou = self.calcu_iou(boxes[i], boxes[j], iou_mode)
                    iou_matrix[i][j] = iou
                    iou_matrix[j][i] = iou
            elif mode == "extend":
                (width, height, extend_ratio_width, extend_ratio_height) = extend_params
                bbox = boxes[i]
                bbox_xywh_center = xyxy2xywh(bbox)
                bbox_xywh_center[2] = bbox_xywh_center[2] * (1 + extend_ratio_width)
                bbox_xywh_center[3] = bbox_xywh_center[3] * (1 + extend_ratio_height)
                bbox_xyxy = xywh2xyxy(bbox_xywh_center)
                bbox = [
                    max(min(bbox_xyxy[0], width), 0),
                    max(min(bbox_xyxy[1], height), 0),
                    max(min(bbox_xyxy[2], width), 0),
                    max(min(bbox_xyxy[3], height), 0),
                ]
                for j in range(len(boxes)):
                    iou = self.calcu_iou(bbox, boxes[j], iou_mode) if (i != j) else 0.0
                    iou_matrix[i][j] = iou

        return iou_matrix

    def calcu_boxes_ab_iou(self, boxes_a, boxes_b, iou_mode="iou", mode="matrix"):
        """计算两个box集合之间的iou矩阵

        Args:
            boxes_a: list, [[xmin1, ymin1, xmax1, ymax1],...]
            boxes_b: list, [[xmin2, ymin2, xmax2, ymax2],...]
            iou_mode: str, 'iou'代表iou
                            'diou'代表diou
            mode: str, 'matrix'代表返回iou矩阵；
                        'list'代表返回iou列表

        Returns:
            iou_list/iou_matrix: list/np.array, iou列表/矩阵
        """
        if mode == "list":
            iou_list = []
        elif mode == "matrix":
            iou_matrix = np.zeros((len(boxes_a), len(boxes_b)), float)

        for i in range(len(boxes_a)):
            for j in range(len(boxes_b)):
                iou = self.calcu_iou(boxes_a[i], boxes_b[j], iou_mode)

                if mode == "list":
                    iou_list.append([i, j, iou])
                elif mode == "matrix":
                    iou_matrix[i][j] = iou

        if mode == "list":
            return iou_list
        elif mode == "matrix":
            return iou_matrix

    def calcu_boxes_ab_distance(self, boxes_a, boxes_b):
        """计算两个box集合之间的距离矩阵
        示例为号码牌和人体框之间的距离

        Args:
            boxes_a: list, [[xmin1, ymin1, xmax1, ymax1],...]
            boxes_b: list, [[xmin2, ymin2, xmax2, ymax2],...]

        Returns:
            distance_matrix: np.array, 距离矩阵
        """
        y_ratio = 1 / 4

        distance_x_matrix = np.zeros((len(boxes_a), len(boxes_b)), float)
        distance_y_matrix = np.zeros((len(boxes_a), len(boxes_b)), float)
        boxes_a = np.asarray(boxes_a)
        boxes_b = np.asarray(boxes_b)

        boxes_a_xywh = self._extracted_from_calcu_boxes_ab_distance_19(boxes_a)
        boxes_b_xywh = self._extracted_from_calcu_boxes_ab_distance_19(boxes_b)
        distance_x_matrix = np.fabs(
            np.repeat(boxes_a_xywh[:, :1], len(boxes_b), axis=1)
            - np.repeat(boxes_b_xywh[:, :1].T, len(boxes_a), axis=0)
        ) / np.repeat(boxes_a_xywh[:, 2:3] / 2, len(boxes_b), axis=1)
        # x出界
        distance_x_matrix_out_range = distance_x_matrix > 1
        distance_x_matrix *= np.repeat(boxes_a_xywh[:, 2:3] / 2, len(boxes_b), axis=1)

        distance_y_matrix = -(
            np.repeat(
                boxes_a[:, 1:2] + boxes_a_xywh[:, 3:4] * y_ratio, len(boxes_b), axis=1
            )
            - np.repeat(boxes_b_xywh[:, 1:2].T, len(boxes_a), axis=0)
        ) / np.repeat(boxes_a_xywh[:, 3:4] / 2, len(boxes_b), axis=1)
        # y出界
        distance_y_matrix_out_range = (distance_y_matrix > (2 * (1 - y_ratio))) | (
            distance_y_matrix < (-2 * y_ratio)
        )
        distance_y_matrix = np.fabs(distance_y_matrix)
        distance_y_matrix *= np.repeat(boxes_a_xywh[:, 3:4] / 2, len(boxes_b), axis=1)

        distance_matrix = distance_x_matrix + distance_y_matrix

        distance_matrix[distance_x_matrix_out_range] = 999999
        distance_matrix[distance_y_matrix_out_range] = 999999

        return distance_matrix

    # TODO Rename this here and in `calcu_boxes_ab_distance`
    def _extracted_from_calcu_boxes_ab_distance_19(self, arg0):
        result = np.zeros_like(arg0)
        result[:, 0] = (arg0[:, 0] + arg0[:, 2]) / 2
        result[:, 1] = (arg0[:, 1] + arg0[:, 3]) / 2
        result[:, 2] = arg0[:, 2] - arg0[:, 0]
        result[:, 3] = arg0[:, 3] - arg0[:, 1]

        return result

    def calcu_diou_matrix_torch(self, bboxes1, bboxes2):
        rows = bboxes1.shape[0]
        cols = bboxes2.shape[0]
        dious = torch.zeros((rows, cols))
        if rows * cols == 0:  #
            return dious
        exchange = False
        if bboxes1.shape[0] > bboxes2.shape[0]:
            bboxes1, bboxes2 = bboxes2, bboxes1
            dious = torch.zeros((cols, rows))
            exchange = True
        # #xmin,ymin,xmax,ymax->[:,0],[:,1],[:,2],[:,3]
        w1 = bboxes1[:, 2] - bboxes1[:, 0]
        h1 = bboxes1[:, 3] - bboxes1[:, 1]
        w2 = bboxes2[:, 2] - bboxes2[:, 0]
        h2 = bboxes2[:, 3] - bboxes2[:, 1]

        area1 = w1 * h1
        area2 = w2 * h2

        center_x1 = (bboxes1[:, 2] + bboxes1[:, 0]) / 2
        center_y1 = (bboxes1[:, 3] + bboxes1[:, 1]) / 2
        center_x2 = (bboxes2[:, 2] + bboxes2[:, 0]) / 2
        center_y2 = (bboxes2[:, 3] + bboxes2[:, 1]) / 2

        inter_max_xy = torch.min(bboxes1[:, 2:], bboxes2[:, 2:])
        inter_min_xy = torch.max(bboxes1[:, :2], bboxes2[:, :2])
        out_max_xy = torch.max(bboxes1[:, 2:], bboxes2[:, 2:])
        out_min_xy = torch.min(bboxes1[:, :2], bboxes2[:, :2])

        inter = torch.clamp((inter_max_xy - inter_min_xy), min=0)
        inter_area = inter[:, 0] * inter[:, 1]
        inter_diag = (center_x2 - center_x1) ** 2 + (center_y2 - center_y1) ** 2
        outer = torch.clamp((out_max_xy - out_min_xy), min=0)
        outer_diag = (outer[:, 0] ** 2) + (outer[:, 1] ** 2)
        union = area1 + area2 - inter_area
        dious = inter_area / union - (inter_diag) / outer_diag
        dious = torch.clamp(dious, min=-1.0, max=1.0)
        if exchange:
            dious = dious.T
        return dious

    def calcu_edit_distance(self, str_a, str_b):
        """计算两个字符串的编辑距离
        编辑距离：一个字符串转为（插入、替换、删除一个字符）另一个字符串的最少操作步骤

        Args:
            str_a: str, 字符串a
            str_b: str, 字符串b

        Returns:
            edit_distance: int, 两个字符串的编辑距离
        """
        n = len(str_a)
        m = len(str_b)

        # 有一个字符串为空串
        if n * m == 0:
            return n + m

        # 初始化DP数组
        D = [[0] * (m + 1) for _ in range(n + 1)]

        # 边界状态初始化
        for i in range(n + 1):
            D[i][0] = i
        for j in range(m + 1):
            D[0][j] = j

        # 计算所有 DP 值
        for i, j in itertools.product(range(1, n + 1), range(1, m + 1)):
            left = D[i - 1][j] + 1
            down = D[i][j - 1] + 1
            left_down = D[i - 1][j - 1]
            if str_a[i - 1] != str_b[j - 1]:
                left_down += 1
            D[i][j] = min(left, down, left_down)

        return D[n][m]

    def calcu_cosine_similarity_np(self, matrix_a, matrix_b):
        """计算两矩阵的cosine相似度

        Args:
            matrix_a: np.array, 矩阵a
            matrix_b: np.array, 矩阵b

        Returns:
            cosine_similarity: float, 矩阵相似度
        """
        # from numpy.linalg import norm
        from sklearn.metrics.pairwise import cosine_similarity

        vector_a = np.expand_dims(matrix_a.flatten(), 0)
        vector_b = np.expand_dims(matrix_b.flatten(), 0)

        return cosine_similarity(vector_a, vector_b)

    def calcu_diff_npy(self, npy_a_path, npy_b_path):
        """计算两个npy文件的相似度

        Args:
            npy_a_path: str, npy文件a的路径
            npy_b_path: str, npy文件b的路径

        Returns:
            npy_diff: float, 两个npy的差
            npy_similarity: float, 两个npy的相似度
        """
        # print时全部输出
        # np.set_printoptions(threshold=1e6)
        npy_a_data = np.load(npy_a_path, allow_pickle=True)
        npy_b_data = np.load(npy_b_path, allow_pickle=True)
        npy_diff = npy_a_data - npy_b_data
        npy_similarity = self.calcu_cosine_similarity_np(npy_a_data, npy_b_data)

        return npy_diff, npy_similarity


"""
math
"""


def rotated_rectangle(center, size, angle):
    """利用中心点、矩形尺寸和旋转角度得到一个旋转矩形的顶点坐标

    Args:
        center: tuple, 旋转矩形中心点(x, y)
        size: tuple, 旋转矩形尺寸(width, height)
        angle: int, 旋转角度，以y轴正方向为准，逆时针方向上的角度

    Returns:
        rotated_rect: list, 旋转矩形, [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    """
    rotated_rect = []
    (width, height) = size

    # 利用宽高构建一个以原点为中心的矩形框
    origin_rect = [
        (0 - int(width / 2), 0 - int(height / 2)),
        (0 + int(width / 2), 0 - int(height / 2)),
        (0 + int(width / 2), 0 + int(height / 2)),
        (0 - int(width / 2), 0 + int(height / 2)),
    ]

    # 旋转角度由角度值转换为弧度制
    rotation = math.radians(angle)

    for point in origin_rect:
        # 直角坐标转换为复数形式
        complex_point = complex(point[0], point[1])

        # 极坐标中，一个复数 z 由模量 r 和相位角 phi 来定义。模量 r 是从 z 到坐标原点的距离，而相位角 phi 是以弧度为单位的，逆时针的，从正X轴到连接原点和 z 的线段间夹角的角度。
        # 笛卡尔坐标系转换为极坐标：模 = √(实部^2+虚部^2), 相位=phase(x) 相当于 math.atan2(实部, 虚部)
        # 点旋转的过程：旋转后的点位置 = 极坐标相位+要旋转的弧度制角度，再由极坐标转换为直角坐标
        point = cmath.rect(abs(complex_point), cmath.phase(complex_point) + rotation)

        # 平移中心点
        point = [point.real + center[0], point.imag + center[1]]
        rotated_rect.append(point)

    return rotated_rect


def get_segs_intersect(line1, line2):
    """判断两线段是否相交
    https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/

    Args:
        line1: tuple, ((Ax, Ay), (Bx, By))，线段AB
        line2: tuple, ((Cx, Cy), (Dx, Dy))，线段CD

    Returns:
        bool, 两线段是否相交
    """

    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(line1[0], line2[0], line2[1]) != ccw(
        line1[1], line2[0], line2[1]
    ) and ccw(line1[0], line1[1], line2[0]) != ccw(line1[0], line1[1], line2[1])


"""
numpy
"""


def calcu_vector_angle_np(vector_a, vector_b, with_character_flag=True, mode="radian"):
    """计算两向量的夹角；若需要带正负号，得到的是向量a沿顺时针方向到向量b的夹角，坐标系为正常的直角坐标系，要与图像坐标系（左上角为原点）区分开
    定理：向量a×向量b（×为向量叉乘），若结果小于0，表示向量b在向量a的顺时针方向；若结果大于0，表示向量b在向量a的逆时针方向；若等于0，表示向量a与向量b平行

    Args:
        vector_a: np.array, 向量a
        vector_b: np.array, 向量b
        with_character_flag: bool, 是否带正负号，即向量a到向量b的角度，取值范围[-π,π]; 不带正负号，取值范围[0,π]
        mode: str, 'radian'输出弧度制；'degree'输出角度制

    Returns:
        angle: float, 两向量夹角
    """
    cos_angle = vector_a.dot(vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )
    angle_radian = np.arccos(cos_angle)
    if with_character_flag:
        cross_ab = np.cross(vector_a, vector_b)
        if cross_ab > 0:
            angle_radian = -angle_radian
    if mode == "radian":
        return angle_radian
    elif mode == "degree":
        return np.rad2deg(angle_radian)


"""
pytorch
"""


def calcu_tensor_angle_torch(tensor_a, tensor_b, mode="radian"):
    """计算两张量的夹角

    Args:
        tensor_a: tensor, 张量a
        tensor_b: tensor, 张量b
        mode: str, 'radian'输出弧度制；'degree'输出角度制

    Returns:
        angle: float, 两向量夹角
    """
    cos_angle = tensor_a.dot(tensor_b) / (torch.norm(tensor_a) * torch.norm(tensor_b))
    angle_radian = torch.acos(cos_angle)
    if mode == "radian":
        return angle_radian.item()
    elif mode == "degree":
        # # pytorch >= 1.6.0
        # angle_degree = torch.rad2deg(angle_radian)
        angle_degree = torch.Tensor([math.degrees(angle_radian)])
        return angle_degree.item()


def calcu_batch_tensor_angle_torch(tensor_a, tensor_b, mode="radian"):
    """批量计算batch大小的两张量的夹角

    Args:
        tensor_a: tensor, batch张量a
        tensor_b: tensor, batch张量b
        mode: str, 'radian'输出弧度制；'degree'输出角度制，只支持pytorch >= 1.6.0

    Returns:
        angle: tensor, batch个向量夹角
    """
    epsilon = 1e-6

    tensor_ab_mul = tensor_a * tensor_b
    tensor_ab_dot = torch.sum(tensor_ab_mul, 1)

    # 防止除以0
    tensor_a_norm = torch.norm(tensor_a, 2, 1)
    tensor_b_norm = torch.norm(tensor_b, 2, 1)
    tensor_a_norm_clamp = torch.clamp(tensor_a_norm, min=epsilon)
    tensor_b_norm_clamp = torch.clamp(tensor_b_norm, min=epsilon)

    tensor_ab_norm_mul = tensor_a_norm_clamp * tensor_b_norm_clamp
    tensor_ab_norm_mul_reci = torch.reciprocal(tensor_ab_norm_mul)

    tensor_ab_cos_angle = tensor_ab_dot * tensor_ab_norm_mul_reci
    # pytorch 中计算arccos时在输入值接近1或者-1的时候会产生NaN值
    # 解决方法：使用torch.clamp将输入值限定在±1∓(1e-8)范围内
    tensor_ab_angle_radian_clamp = torch.clamp(
        tensor_ab_cos_angle, -1 + epsilon, 1 - epsilon
    )
    tensor_ab_angle_radian = torch.acos(tensor_ab_angle_radian_clamp)

    if mode == "radian":
        return tensor_ab_angle_radian
    elif mode == "degree":
        return torch.rad2deg(tensor_ab_angle_radian)



class Trigonometric:
    """
    三角函数，点线面之间的距离
    """

    @staticmethod
    def define_area(point1, point2, point3):
        """
        法向量    ：n={A,B,C}
        空间上某点：p={x0,y0,z0}
        点法式方程：A(x-x0)+B(y-y0)+C(z-z0)=Ax+By+Cz-(Ax0+By0+Cz0)
        https://wenku.baidu.com/view/12b44129af45b307e87197e1.html
        :param point1:
        :param point2:
        :param point3:
        :param point4:
        :return:（Ax, By, Cz, D）代表：Ax + By + Cz + D = 0
        """
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)
        point3 = np.asarray(point3)
        AB = np.asmatrix(point2 - point1)
        AC = np.asmatrix(point3 - point1)
        N = np.cross(AB, AC)  # 向量叉乘，求法向量
        # Ax+By+Cz
        Ax = N[0, 0]
        By = N[0, 1]
        Cz = N[0, 2]
        D = -(Ax * point1[0] + By * point1[1] + Cz * point1[2])
        return Ax, By, Cz, D

    @staticmethod
    def define_line(point1, point2):
        """
        y-y1=k(x-x1),k=(y2-y1)/(x2-x1)=>
        kx-y+(y1-kx1)=0 <=> Ax+By+C=0
        => A=K=(y2-y1)/(x2-x1)
        => B=-1
        => C=(y1-kx1)
        :param point1:
        :param point2:
        :return:
        """
        x1, y1 = point1[0], point1[1]
        x2, y2 = point2[0], point2[1]
        A = (y2 - y1) / (x2 - x1)  # K
        B = -1
        C = y1 - A * x1
        return A, B, C

    @staticmethod
    def point2line_distance(point1, point2, target_point):
        """
        :param point1: line point1
        :param point2: line point2
        :param target_point: target_point
        :return:
        """
        A, B, C = Trigonometric.define_line(point1, point2)
        mod_d = A * target_point[0] + B * target_point[1] + C
        mod_sqrt = np.sqrt(np.sum(np.square([A, B])))
        return abs(mod_d) / mod_sqrt

    @staticmethod
    def point2area_distance(point1, point2, point3, point4):
        """
        :param point1:数据框的行切片，三维
        :param point2:
        :param point3:
        :param point4:
        :return:点到面的距离
        """
        Ax, By, Cz, D = Trigonometric.define_area(point1, point2, point3)
        mod_d = Ax * point4[0] + By * point4[1] + Cz * point4[2] + D
        mod_area = np.sqrt(np.sum(np.square([Ax, By, Cz])))
        return abs(mod_d) / mod_area

    @staticmethod
    def gen_vector(point1, point2):
        """
        P12 = point2-point1
        :param point1:
        :param point2:
        :return:
        """
        if not isinstance(point1, np.ndarray):
            point1 = np.asarray(point1, dtype=np.float32)
        if not isinstance(point2, np.ndarray):
            point2 = np.asarray(point2, dtype=np.float32)
        return point2 - point1

    @staticmethod
    def radian2angle(radian):
        """弧度->角度"""
        return radian * (180 / np.pi)


    @staticmethod
    def angle2radian(angle):
        """角度 ->弧度"""
        return angle * np.pi / 180.0
    @staticmethod
    def compute_point_angle(P1, P2, Q1, Q2):
        x = Trigonometric.gen_vector(P1, P2)
        y = Trigonometric.gen_vector(Q1, Q2)
        return Trigonometric.compute_vector_angle(x, y, minangle=True)

    @staticmethod
    def compute_vector_angle(a, b, minangle=True):
        """
        cosφ = u·v/|u||v|
        https://wenku.baidu.com/view/301a6ba1250c844769eae009581b6bd97f19bca3.html?from=search
        :param a:
        :param b:
        :return:
        """
        # 两个向量
        x = np.array(a)
        y = np.array(b)
        Lx = np.sqrt(x.dot(x))
        Ly = np.sqrt(y.dot(y))
        value = x.dot(y) / ((Lx * Ly) + 1e-6)  # cosφ = u·v/|u||v|
        radian = np.arccos(value)
        angle = Trigonometric.radian2angle(radian)
        if minangle:
            # angle = np.where(angle > 90, 180 - angle, angle)
            angle = angle if angle < 90 else 180 - angle
        return angle
