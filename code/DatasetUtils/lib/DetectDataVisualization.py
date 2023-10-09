import random
import cv2
import shutil
import numpy as np

from .FileUtils import *
from .ImageVideoUtils import *
from .Convertion import head_shoulder_box2person_box, colorstr


def point_in_mask(point, mask_image):
    ## point (x,y)
    if (
        point[0] < 0
        or point[0] >= mask_image.shape[1]
        or point[1] < 0
        or point[1] >= mask_image.shape[0]
    ):
        return False
    else:
        return mask_image[int(point[1]), int(point[0])] > 128


def draw_box_with_text(image, box, text, color_idx, fontScale=1, fontThickness=2):
    """绘制带文字的box框

    Args:
        image: np.array, 需要绘制的图像
        box: list, 需要绘制的框, [x1, y1, x2, y2]
        text: str, 需要绘制的文字
        color_idx: int , 颜色下标，0-19
        fontScale: float, 字体大小
        fontThickness: int, 字体粗细
    """
    txt_color = (255, 255, 255)
    colors = [
        (132, 56, 255),
        (82, 0, 133),
        (203, 56, 255),
        (255, 149, 200),
        (255, 55, 199),
        (61, 219, 134),
        (26, 147, 52),
        (0, 212, 187),
        (44, 153, 168),
        (0, 194, 255),
        (52, 69, 147),
        (100, 115, 255),
        (0, 24, 236),
        (255, 56, 56),
        (255, 157, 151),
        (255, 112, 31),
        (255, 178, 29),
        (207, 210, 49),
        (72, 249, 10),
        (146, 204, 23),
    ]

    # draw box
    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    cv2.rectangle(image, c1, c2, colors[color_idx], thickness=3, lineType=cv2.LINE_AA)

    # draw text
    w, h = cv2.getTextSize(text, 0, fontScale=fontScale, thickness=fontThickness)[0]
    c2 = c1[0] + w, c1[1] - h - 3
    cv2.rectangle(image, c1, c2, colors[color_idx], -1, cv2.LINE_AA)
    cv2.putText(
        image,
        text,
        (c1[0], c1[1] - 2),
        0,
        fontScale,
        txt_color,
        thickness=fontThickness,
        lineType=cv2.LINE_AA,
    )


def generate_a_heatmap(arr, centers):
    """Generate pseudo heatmap for one keypoint in one frame.

    Args:
        arr (np.ndarray): The array to store the generated heatmaps. Shape: img_h * img_w.
        centers (np.ndarray): The coordinates of corresponding keypoints (of multiple persons). Shape: M * 2.
        max_values (np.ndarray): The max values of each keypoint. Shape: M.

    Returns:
        np.ndarray: The generated pseudo heatmap.
    """
    EPS = 1e-3
    sigma = 1
    img_h, img_w = arr.shape

    for center in zip(centers):
        center = center[0]
        mu_x, mu_y = center[0], center[1]
        st_x = max(int(mu_x - 3 * sigma), 0)
        ed_x = min(int(mu_x + 3 * sigma) + 1, img_w)
        st_y = max(int(mu_y - 3 * sigma), 0)
        ed_y = min(int(mu_y + 3 * sigma) + 1, img_h)
        x = np.arange(st_x, ed_x, 1, np.float32)
        y = np.arange(st_y, ed_y, 1, np.float32)

        # if the keypoint not in the heatmap coordinate system
        if not (len(x) and len(y)):
            continue
        y = y[:, None]

        patch = np.exp(-((x - mu_x) ** 2 + (y - mu_y) ** 2) / 2 / sigma**2)
        # patch = patch * max_value
        arr[st_y:ed_y, st_x:ed_x] = np.maximum(arr[st_y:ed_y, st_x:ed_x], patch)
    return arr


class BasicDataVis:
    """数据可视化基础类"""

    def draw_boxes_ab_with_text(self, boxes_a, boxes_b, ab_relation):
        """绘制两组box，以及boxes_b与boxes_a每个元素的关系"""
        image = np.ones((720, 1280, 3), dtype=np.uint8) * 255

        for box_a_idx, box_a in enumerate(boxes_a):
            draw_box_with_text(
                image, boxes_a[box_a_idx], f"{box_a_idx}", box_a_idx % 20, 0.5, 1
            )

        for box_b_idx, box_b in enumerate(boxes_b):
            text = "".join(
                f"{relation_a_idx}:{relation:.3f};"
                for relation_a_idx, relation_b_idx, relation in ab_relation
                if box_b_idx == relation_b_idx
            )
            draw_box_with_text(image, boxes_b[box_b_idx], text, 19, 0.5, 1)

        return image


class DetDataVis(BasicDataVis):
    """检测数据可视化类"""

    def show_yolo_txt(self, root, ratio, classes, mode="show", mode2="std"):
        """读取txt文件内容，绘制检测框到图片上，用于验证标注文件正确性

        Args:
            root: str, 根目录路径
            ratio: float, 需要可视化的数据集比例
            classes: list, 类别列表
            mode: str, 'show'代表窗口显示结果，'write'代表存储图片至同级show_result_txt目录下
            mode2: str, 'std'代表只包含类别与检测框；
                        'with_hip_mid_keypoint'代表只包含类别、检测框与臀部关键点；
        """
        if mode == "show":
            cv2.namedWindow("show", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("show", int(1920 / 1.5), int(1080 / 1.5))

        yolo_path = f"{root}/Annotations/"
        txt_files = os.listdir(os.path.join(yolo_path))
        rand_list = random.sample(range(len(txt_files)), int(len(txt_files) * ratio))
        for index, txt_file in enumerate(txt_files):
            if index not in rand_list:
                continue
            print(index, txt_file)
            image = cv2.imread(
                os.path.join(
                    yolo_path.replace("Annotations", "JPEGImages"),
                    txt_file.replace(".txt", ".jpg"),
                )
            )
            width = image.shape[1]
            height = image.shape[0]
            txt_data = read_yolo_txt(
                os.path.join(yolo_path, txt_file), width, height, mode2
            )

            for box in txt_data:
                cv2.rectangle(
                    image,
                    (int(box[0]), int(box[1])),
                    (int(box[2]), int(box[3])),
                    (0, 255, 0),
                    3,
                    lineType=cv2.LINE_AA,
                )
                cv2.putText(
                    image,
                    classes[box[4]],
                    (int(box[0]), int(box[1])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1,
                )
                if len(box) == 7 and (box[5] != -1) and (box[6] != -1):
                    cv2.circle(
                        image,
                        (int(box[5]), int(box[6])),
                        radius=5,
                        color=(0, 255, 0),
                        thickness=-1,
                    )
                    cv2.line(
                        image,
                        (int(box[5]), int(box[6])),
                        (int((box[0] + box[2]) / 2), box[3]),
                        color=(0, 255, 0),
                        thickness=3,
                        lineType=cv2.LINE_AA,
                    )

            if mode == "show":
                cv2.imshow("show", image)
                cv2.waitKey(0)
            elif mode == "write":
                os.makedirs(
                    os.path.join(yolo_path.replace("Annotations", "show_result_txt")),
                    exist_ok=True,
                )
                cv2.imwrite(
                    os.path.join(
                        yolo_path.replace("Annotations", "show_result_txt"),
                        txt_file.replace(".txt", ".jpg"),
                    ),
                    image,
                )

    def show_voc_xml(self, root, ratio, mode="show"):
        """读取xml文件内容，绘制检测框到图片上，用于验证标注文件正确性

        Args:
            root, str, 数据集文件路径
            ratio: float, 需要可视化的数据集比例
            mode: str, 'show'代表窗口显示结果，'write'代表存储图片至同级show_result_xml目录下
        """
        if mode == "show":
            cv2.namedWindow("show", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("show", int(1920 / 1.5), int(1080 / 1.5))

        xml_files = os.listdir(os.path.join(root, "Annotations_XML"))
        rand_list = random.sample(range(len(xml_files)), int(len(xml_files) * ratio))
        for idx, xml_file in enumerate(xml_files):
            if idx not in rand_list:
                continue
            print(idx, xml_file)
            xml_data = read_xml(os.path.join(root, "Annotations_XML", xml_file), "std")
            image = cv2.imread(
                os.path.join(root, "JPEGImages", xml_file.replace(".xml", ".jpg"))
            )

            for box in xml_data["bndboxes"]:
                cv2.rectangle(
                    image,
                    (int(box[0]), int(box[1])),
                    (int(box[2]), int(box[3])),
                    (0, 255, 0),
                    2,
                )
                cv2.putText(
                    image,
                    box[4],
                    (int(box[0]), int(box[1])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1,
                )
                # cv2.circle(image, (int(box[5]),int(box[6])), radius = 6, color = (0,0,255), thickness=-1)

            if mode == "show":
                cv2.imshow("show", image)
                cv2.waitKey(0)
            elif mode == "write":
                os.makedirs(os.path.join(root, "show_result_xml"), exist_ok=True)
                cv2.imwrite(
                    os.path.join(
                        root, "show_result_xml", xml_file.replace(".xml", ".jpg")
                    ),
                    image,
                )

    def show_prelabel(
        self, prelabel_json_path, img_dir_path, save_img_dir_path, ratio, mode="show"
    ):
        """读取预标注文件内容，绘制检测框到图片上，用于验证预标注文件正确性

        Args:
            prelabel_json_path: str, 预标注文件路径
            img_dir_path: str, 图片文件路径
            save_img_dir_path: str, 存储图片路径
            ratio: float, 需要可视化的数据集比例
            mode: str, 'show'代表窗口显示结果，'write'代表存储图片至同级show_prelabel目录下
        """
        if mode == "show":
            cv2.namedWindow("show", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("show", int(1920 / 1.5), int(1080 / 1.5))
        elif mode == "write":
            os.makedirs(save_img_dir_path, exist_ok=True)

        prelabel_json_data = read_json(prelabel_json_path, "line")
        rand_list = random.sample(
            range(len(prelabel_json_data)), int(len(prelabel_json_data) * ratio)
        )
        for idx, image_info in enumerate(prelabel_json_data):
            if idx not in rand_list:
                continue
            print(idx, len(prelabel_json_data))
            image_path = os.path.join(
                img_dir_path, os.path.basename(image_info["url_image"])
            )
            image = cv2.imread(image_path)

            boxes = image_info["result"]
            for info in boxes:
                box = info["data"]
                comment = info["comment"]
                color_idx = int(comment) % 20 if comment != "" else 0
                draw_box_with_text(image, box, comment, color_idx)

            if mode == "show":
                cv2.imshow("show", image)
                cv2.waitKey(0)
            elif mode == "write":
                cv2.imwrite(
                    os.path.join(
                        save_img_dir_path, os.path.basename(image_info["url_image"])
                    ),
                    image,
                )

    def badcase_det_box_vis(self, image, correct_boxes, incorrect_boxes, missed_boxes):
        """可视化检测模型的badcase框；绿框表示正确检测到的框，红框代表误检框，蓝框代表漏检框

        Args:
            image: np.array, 原始图像
            correct_boxes: list, 正确检测到的框(pred_box)
            incorrect_boxes: list, 误检的框(pred_box)
            missed_boxes: list, 漏检的框(gt_box)

        Returns:
            image: np.array, 绘制badcase框的图像
        """

        for correct_box in correct_boxes:
            cv2.rectangle(
                image,
                (int(correct_box[0]), int(correct_box[1])),
                (int(correct_box[2]), int(correct_box[3])),
                (0, 255, 0),
                2,
            )

        for incorrect_box in incorrect_boxes:
            cv2.rectangle(
                image,
                (int(incorrect_box[0]), int(incorrect_box[1])),
                (int(incorrect_box[2]), int(incorrect_box[3])),
                (0, 0, 255),
                2,
            )

        for missed_box in missed_boxes:
            cv2.rectangle(
                image,
                (int(missed_box[0]), int(missed_box[1])),
                (int(missed_box[2]), int(missed_box[3])),
                (255, 0, 0),
                2,
            )

        return image

    def badcase_det_box_hip_vis(self, image, gt_box_hip, pred_box_hip):
        """可视化检测+臀部点的badcase框；绿框表示正确检测到的框，红框代表误检框，蓝框代表漏检框

        Args:
            image: np.array, 原始图像
            gt_box_hip: list, gt框+hip
            pred_box_hip: list, 预测框+hip

        Returns:
            image: np.array, 绘制badcase框的图像
        """
        # gt
        cv2.rectangle(
            image,
            (int(gt_box_hip[0]), int(gt_box_hip[1])),
            (int(gt_box_hip[2]), int(gt_box_hip[3])),
            (0, 255, 0),
            3,
        )
        cv2.circle(
            image,
            (int(gt_box_hip[5]), int(gt_box_hip[6])),
            radius=5,
            color=(0, 255, 0),
            thickness=-1,
        )
        cv2.line(
            image,
            (int(gt_box_hip[5]), int(gt_box_hip[6])),
            (int((gt_box_hip[0] + gt_box_hip[2]) / 2), int(gt_box_hip[3])),
            color=(0, 255, 0),
            thickness=3,
            lineType=cv2.LINE_AA,
        )

        # pred
        cv2.rectangle(
            image,
            (int(pred_box_hip[0]), int(pred_box_hip[1])),
            (int(pred_box_hip[2]), int(pred_box_hip[3])),
            (0, 0, 255),
            3,
        )
        if pred_box_hip[6] != -1:
            cv2.circle(
                image,
                (int(pred_box_hip[6]), int(pred_box_hip[7])),
                radius=5,
                color=(0, 0, 255),
                thickness=-1,
            )
            cv2.line(
                image,
                (int(pred_box_hip[6]), int(pred_box_hip[7])),
                (int((pred_box_hip[0] + pred_box_hip[2]) / 2), int(pred_box_hip[3])),
                color=(0, 0, 255),
                thickness=3,
                lineType=cv2.LINE_AA,
            )

        person_box = head_shoulder_box2person_box(gt_box_hip[:4], 4.0, 1080, 1920)
        return crop_image_extend_border(image, person_box, 0.4, 0.4)


class ReIDDataVis(BasicDataVis):
    """ReID数据可视化类

    Attributes:
        root: str, 根目录路径
        save_dir_path: str, 需要保存文件的路径
    """

    def __init__(self, root, save_dir_path=None):
        self.root = root
        self.save_dir_path = save_dir_path


class DetKeypointDataVis(BasicDataVis):
    """检测+关键点数据可视化类

    Attributes:
        root: str, 根目录路径
        save_dir_path: str, 需要保存文件的路径
    """

    def __init__(self, root, save_dir_path=None):
        self.root = root
        self.save_dir_path = save_dir_path

    def show_voc_xml(self, mode="show"):
        """读取xml文件内容，绘制检测框到图片上，用于验证标注文件正确性

        Args:
            mode: str, 'show'代表窗口显示结果，'write'代表存储图片至同级show_result_xml目录下
        """
        if mode == "show":
            cv2.namedWindow("show", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("show", int(1920 / 1.5), int(1080 / 1.5))

        xml_files = os.listdir(os.path.join(self.root, "Annotations_XML"))
        for index, xml_file in enumerate(xml_files):
            print(index, xml_file)
            xml_data = read_xml(
                os.path.join(self.root, "Annotations_XML", xml_file),
                "with_hip_mid_keypoint",
            )
            image = cv2.imread(
                os.path.join(self.root, "JPEGImages", xml_file.replace(".xml", ".jpg"))
            )

            for box in xml_data["bndboxes"]:
                cv2.rectangle(
                    image,
                    (int(box[0]), int(box[1])),
                    (int(box[2]), int(box[3])),
                    (0, 255, 0),
                    3,
                    lineType=cv2.LINE_AA,
                )
                cv2.putText(
                    image,
                    box[4],
                    (int(box[0]), int(box[1])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    1,
                )
                if (box[5] != -1) and (box[6] != -1):
                    cv2.circle(
                        image,
                        (int(box[5]), int(box[6])),
                        radius=5,
                        color=(0, 255, 0),
                        thickness=-1,
                    )
                    cv2.line(
                        image,
                        (int(box[5]), int(box[6])),
                        (int((box[0] + box[2]) / 2), box[3]),
                        color=(0, 255, 0),
                        thickness=3,
                        lineType=cv2.LINE_AA,
                    )

            if mode == "show":
                cv2.imshow("show", image)
                cv2.waitKey(0)
            elif mode == "write":
                os.makedirs(os.path.join(self.root, "show_result_xml"), exist_ok=True)
                cv2.imwrite(
                    os.path.join(
                        self.root, "show_result_xml", xml_file.replace(".xml", ".jpg")
                    ),
                    image,
                )


class KeypointDataVis(BasicDataVis):
    """关键点数据可视化类

    Attributes:
        root: str, 根目录路径
        save_dir_path: str, 需要保存文件的路径
    """

    def __init__(self, root, save_dir_path=None):
        self.root = root
        self.save_dir_path = save_dir_path

    def draw_bag_keypoint_using_txt(self, txt_path):
        """可视化训练数据txt中的关键点

        Args:
            txt_path: str, 训练数据txt路径
        """
        txt_data = read_txt(txt_path)

        for index, line in enumerate(txt_data):
            image_path, x1, y1, x2, y2, x3, y3, x4, y4 = line.split(",")
            x1, y1, x2, y2, x3, y3, x4, y4 = (
                float(x1),
                float(y1),
                float(x2),
                float(y2),
                float(x3),
                float(y3),
                float(x4),
                float(y4),
            )

            # image = cv2.imread(image_path)
            image = cv2.imread(
                os.path.join(self.root, "女包高清大图_v10", image_path.split("/")[-1][9:])
            )
            print(index, image_path)
            height, width, channel = image.shape
            points_array = np.array(
                [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]], dtype=np.int32
            )
            cv2.polylines(image, [points_array], True, (255, 255, 255), 2)
            cv2.circle(
                image, (int(x1), int(y1)), radius=4, color=(0, 0, 255), thickness=-1
            )
            cv2.circle(
                image, (int(x2), int(y2)), radius=4, color=(0, 255, 0), thickness=-1
            )
            cv2.circle(
                image, (int(x3), int(y3)), radius=4, color=(255, 0, 0), thickness=-1
            )
            cv2.circle(
                image, (int(x4), int(y4)), radius=4, color=(0, 255, 255), thickness=-1
            )

            show_image_path = os.path.join(
                self.save_dir_path, os.path.basename(image_path)
            )
            os.makedirs(os.path.dirname(show_image_path), exist_ok=True)
            cv2.imwrite(show_image_path, image)
