"""图像标注脚本, 生成json格式的标注文件"""

import cv2
import glob
import os
import numpy as np
import json
import argparse
from pathlib import Path

ix, iy = -1, -1


# 目标框标注程序
class CLabeled:
    def __init__(self, args):
        # 存放需要标注图像的文件夹
        self.image_folder = args.image_folder
        # 任务类型
        self.task = args.task
        # 需要标注图像的总数量
        self.total_image_number = 0
        # 需要标注图像的地址列表
        self.images_list = list()
        # 当前标注图片的索引号，也是已标注图片的数量
        self.current_label_index = 0
        # 待标注图片
        self.image = None
        # 目标框的分类索引号
        self.label_index = 0
        # 当前图片
        self.current_image = None
        # 标注框的保存文件地址
        self.label_path = None
        # 记录历史标注位置的文本文件地址
        self.checkpoint_path = os.path.join(args.image_folder, f"checkpoint_{args.task}")
        self.annotation = None
        # 标注框信息
        self.boxes = list()
        # 类别信息
        self.classes = list()
        self.cls = args.category
        self.types = list()
        # 图像宽
        self.width = 320
        # 图像高
        self.height = 288
        self.scale = args.scale
        # 显示窗口的名称
        self.windows_name = "image"
        self.auto_play_flag = False
        self.decay_time = 33 if self.auto_play_flag else 0
        self._may_make_dir()
        self.labeled()

    # 重置
    def _reset(self):
        self.image = None
        self.current_image = None
        self.label_path = None
        self.boxes = list()
        self.classes = list()
        self.types = list()

    # 统计所有图片个数
    def _compute_total_image_number(self):
        self.total_image_number = len(self.images_list)

    def _may_make_dir(self):
        if not os.path.exists(self.image_folder):
            print(self.image_folder, " does not exists! please check it !")
            exit(-1)
        path = os.path.join(self.image_folder, "annotations")
        if not os.path.exists(path):
            os.makedirs(path)

    # 当前标注位置倒退一个
    def _backward(self):
        self.current_label_index -= 1
        self.current_label_index = max(0, self.current_label_index)

    # 限定鼠标坐标区域的大小
    def _roi_limit(self, x, y):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.width:
            x = self.width
        if y > self.height:
            y = self.height
        return x, y

    # box标准化
    def box_fix(self, box):
        left_top_x = min(box[0], box[2])
        left_top_y = min(box[1], box[3])
        right_bottom_x = max(box[0], box[2])
        right_bottom_y = max(box[1], box[3])
        return [left_top_x, left_top_y, right_bottom_x, right_bottom_y]

    # 标注感兴趣区域
    def _draw_roi(self, event, x, y, flags, param, mode=True):
        global ix, iy
        dst = self.image.copy()
        self._draw_box_on_image(dst, self.boxes, self.classes, self.types)
        if event == cv2.EVENT_LBUTTONDOWN:  # 按下鼠标左键
            x, y = self._roi_limit(x, y)
            ix, iy = x, y
            cv2.imshow(self.windows_name, dst)
        elif event == cv2.EVENT_MOUSEMOVE and not (flags and cv2.EVENT_FLAG_LBUTTON):  # 鼠标移动
            x, y = self._roi_limit(x, y)
            if mode:
                cv2.line(dst, (x, 0), (x, self.height), (255, 0, 0), 1, 8, )
                cv2.line(dst, (0, y), (self.width, y), (255, 0, 0), 1, 8)
            else:
                cv2.circle(dst, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow(self.windows_name, dst)
        elif event == cv2.EVENT_MOUSEMOVE and (flags and cv2.EVENT_FLAG_LBUTTON):  # 按住鼠标左键进行移动
            x, y = self._roi_limit(x, y)
            if mode:
                cv2.rectangle(dst, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                cv2.circle(dst, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow(self.windows_name, dst)
        elif event == cv2.EVENT_LBUTTONUP:  # 鼠标左键松开
            x, y = self._roi_limit(x, y)
            if mode:
                if abs(x - ix) > 10 and abs(y - iy) > 10:
                    cv2.rectangle(self.current_image, (ix, iy), (x, y), (0, 255, 0), 2)
                    cv2.putText(self.current_image, str(self.cls), (ix + 5, iy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    cv2.putText(self.current_image, "simple", (ix + 15, iy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    self.boxes.append([ix / self.width, iy / self.height, x / self.width, y / self.height])
                    self.classes.append(self.cls)
                    self.types.append(0)
            else:
                cv2.circle(self.current_image, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow(self.windows_name, self.current_image)
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            self.types[-1] = int(not self.types[-1])
            self._draw_box_on_image(self.current_image, self.boxes, self.classes, self.types)
        elif event == cv2.EVENT_RBUTTONDOWN:  # 删除(中心点或左上点)距离当前鼠标最近的框
            x, y = self._roi_limit(x, y)
            self.current_image = self.image.copy()
            if len(self.boxes):
                if len(self.boxes) > 1:
                    current_point = np.array([x / self.width, y / self.height])
                    current_center_point = (np.array([box[0:2] for box in self.boxes]) + np.array([box[2:4] for box in self.boxes])) / 2  # 中心点
                    square1 = np.sum(np.square(current_center_point), axis=1)
                    square2 = np.sum(np.square(current_point), axis=0)
                    squared_dist = - 2 * np.matmul(current_center_point, current_point.T) + square1 + square2
                    sort_index = np.argsort(squared_dist)
                    if self.classes[sort_index[0]] == self.cls:
                        del self.boxes[sort_index[0]]
                        del self.classes[sort_index[0]]
                        del self.types[sort_index[0]]
                else:
                    if self.classes[-1] == self.cls:
                        del self.boxes[-1]
                        del self.classes[-1]
                        del self.types[-1]
                self._draw_box_on_image(self.current_image, self.boxes, self.classes, self.types)

    # 将标注框显示到图像上
    def _draw_box_on_image(self, image, boxes, classes, types):
        for box, cls, hard in zip(boxes, classes, types):
            x1, y1 = (int(image.shape[1] * box[0]), int(image.shape[0] * box[1]))
            x2, y2 = (int(image.shape[1] * box[2]), int(image.shape[0] * box[3]))
            if cls == self.cls:
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.putText(image, str(cls), (x1 + 5, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            else:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(image, str(cls), (x1 + 5, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            if hard:
                cv2.putText(image, "hard", (x1 + 15, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            else:
                cv2.putText(image, "simple", (x1 + 15, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.imshow(self.windows_name, image)

    # 从文本读取标注框信息
    def read_label_file(self, label_file_path):
        boxes = []
        classes = []
        types = []
        label_file = open(label_file_path, 'r', encoding='utf-8')
        self.annotation = json.load(label_file)
        label_file.close()
        if self.task not in self.annotation["annotation"]:
            annotations = []
        else:
            annotations = self.annotation["annotation"][self.task]
        for bbox in annotations:
            if 'box' in bbox:
                boxes.append(bbox["box"])
            if 'type' in bbox:
                types.append(bbox['type'])
            else:
                types.append(0)
            if 'class' in bbox:
                classes.append(int(bbox["class"]))
            else:
                classes.append(self.cls)
        self.boxes = boxes
        self.classes = classes
        self.types = types
    
    def generate_label(self, image):
        anno = {
            "image": {
                "information": {}
            },
            "annotation": {}
        }
        img_h, img_w = image.shape[:2]
        anno["image"]["information"]["path"] = ""
        anno["image"]["information"]["height"] = img_h
        anno["image"]["information"]["width"] = img_w
        return anno
        
    # 将标注框信息保存到文本
    def write_label_file(self, label_file_path):
        ann_boxes = []
        for box, cls, hard in zip(self.boxes, self.classes, self.types):
            ann_boxes.append({
                "box": self.box_fix(box),
                "class": cls,
                "type": hard
            })
        self.annotation["annotation"][self.task] = ann_boxes
        save_file = open(label_file_path, 'w', encoding="utf-8")
        json.dump(self.annotation, save_file, indent=4, ensure_ascii=False)
        save_file.close()

    # 记录当前已标注位置，写到文本
    def write_checkpoint(self, checkpoint_path):
        if not os.path.exists(os.path.dirname(checkpoint_path)):
            os.makedirs(os.path.dirname(checkpoint_path))
        checkpoint_file = open(checkpoint_path, "w")
        checkpoint_file.writelines(str(self.current_label_index))

    # 从文本读取当前已标注位置
    def read_checkpoint(self, checkpoint_path):
        checkpoint_file = open(checkpoint_path, "r")
        for line in checkpoint_file.readlines():
            self.current_label_index = int(line.strip())
        checkpoint_file.close()

    # 标注程序运行部分
    def labeled(self):
        labeled_index, labeled_num, labeled_person = self.current_label_index, 0, 0
        self.images_list = sorted(glob.glob(F"{self.image_folder}/*/*.jpg") + glob.glob(F"{self.image_folder}/*/*.png"))
        self._compute_total_image_number()
        print("需要标注的图片总数为: ", self.total_image_number)
        if os.path.exists(self.checkpoint_path):
            self.read_checkpoint(self.checkpoint_path)
        while True:
            self.current_label_index = min(self.current_label_index, self.total_image_number - 1)
            print(F"当前图像ID: {self.current_label_index}")
            print(F"当前图像地址: {self.images_list[self.current_label_index]}\n")
            self.write_checkpoint(self.checkpoint_path)
            self._reset()
            self.image = cv2.imdecode(np.fromfile(self.images_list[self.current_label_index], dtype=np.uint8), 1)
            self.current_image = self.image.copy()
            filepath, filename = os.path.split(self.images_list[self.current_label_index])
            self.label_path = os.path.join(filepath.replace("images", "annotations"), filename.replace(Path(filename).suffix, ".json"))
            if os.path.exists(self.label_path):
                self.read_label_file(self.label_path)
            else:
                self.annotation = self.generate_label(self.image)
            self.width = self.image.shape[1]
            self.height = self.image.shape[0]
            if self.scale:
                cv2.namedWindow(self.windows_name, 0)
            self._draw_box_on_image(self.current_image, self.boxes, self.classes, self.types)
            cv2.setMouseCallback(self.windows_name, self._draw_roi)
            key = cv2.waitKey(self.decay_time)
            self.write_label_file(self.label_path)

            if self.current_label_index >= labeled_index:
                labeled_index = self.current_label_index
                labeled_num += 1
                labeled_person += len(self.boxes)
                print(F"已标注张数: {labeled_num}; 已标注人数: {labeled_person}")

            if key == 32:
                self.auto_play_flag = not self.auto_play_flag
                self.decay_time = 10 if self.auto_play_flag else 0
            if key == ord('a') or key == ord('A'):  # 后退一张
                self._backward()
                continue
            if key == ord('l') or key == ord('L'):  # 删除当前图
                os.remove(self.images_list[self.current_label_index])
                os.remove(self.label_path)
                del self.images_list[self.current_label_index]
                self._compute_total_image_number()
                self._backward()
                self.current_label_index += 1
                continue
            elif key == 27:  # 退出
                break
            else:  # 其他按键
                self.current_label_index += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_folder", type=str, help="the path of reviewed images")
    parser.add_argument("--task", type=str, default="pedestrain", help="task name")
    parser.add_argument("--scale", action="store_true", help="whether to show original images")
    parser.add_argument("--category", type=int, default=0, help="the category of processed objects")
    args = parser.parse_args()
    CLabeled(args)


if __name__ == '__main__':
    main()
