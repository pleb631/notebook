# -*- coding: UTF-8 -*-
import os
import abc
import shutil
import glob
import json, csv, pickle, yaml
import random
import numpy as np
import xml.etree.ElementTree as ET


'''
JSON文件读写
'''
def read_json(json_path, mode='all'):
    '''读取json文件

    Args:
        json_path: str, json文件路径
        mode: str, 'all'模式代表一次性读取json文件全部内容，只存在一个字典；'line'模式代表按行读取json文件内容，每行为一个字典

    Returns:
        json_data: list, json文件内容
    '''
    json_data = []
    with open(json_path, 'r') as json_file:
        if mode == 'all':
            # 把读取内容转换为python字典
            json_data = json.loads(json_file.read())
        elif mode == 'line':
            for line in json_file.readlines():
                json_line = json.loads(line)
                json_data.append(json_line)
    
    return json_data


def save_json(json_path, info, indent=4, mode='w', with_return_char=False):
    '''保存json文件

    Args:
        json_path: str, json文件路径
        info: dict, json文件内容
        indent: int, 缩进量，默认为4；None代表不缩进
        mode: str, 'w'代表覆盖写；'a'代表追加写
        with_return_char: bool, 写文件时是否在结尾添加换行符
    '''
    os.makedirs(os.path.split(json_path)[0], exist_ok=True)
    
    # 把python字典转换为字符串
    json_str = json.dumps(info, indent=indent)
    if with_return_char:
        json_str += '\n'
    
    with open(json_path, mode) as json_file:
        json_file.write(json_str)
    
    json_file.close()


class SaveJson(metaclass=abc.ABCMeta):
    """保存Json文件抽象类

    Attributes:
        save_json_path: str, 保存json文件路径
        json_data: list, json文件内容
    """
    def __init__(self, save_json_path):
        self.save_json_path = save_json_path
        self.json_data = []

    @abc.abstractmethod
    def parse_info(self):
        '''传入json文件内容
        '''
        pass

    def save_json_data(self, mode='all'):
        '''保存json文件

        Args:
            mode: str, 'all'代表一次性存储所有数据；'line'代表分行存储数据
        '''
        if mode == 'all':
            save_json(self.save_json_path, self.json_data, 4, 'w', False)
            # for json_line_data in self.json_data:
            #     save_json(self.save_json_path, json_line_data, None, 'a', True)
        elif mode == 'line':
            json_line_data = self.json_data[0]
            save_json(self.save_json_path, json_line_data, None, 'a', True)
            self.json_data.pop(0)


class SaveCocoPredJson(SaveJson):
    """保存COCO格式预测结果文件类
    """
    def __init__(self, save_json_path):
        super().__init__(save_json_path)

    def parse_info(self, info):
        '''传入json文件内容

        Args:
            info: tuple, 文件内容，格式为[{"image_id": 42, "category_id": 18, "bbox": [258.15, 41.29, 348.26, 243.78], "score": 0.236}, ...
                                                          注意coco的bbox格式为: [xmin, ymin, w, h]！！！！！！而非[xmin, ymin, xmax, ymax]
        '''
        (image_id, category_id, bbox, score) = info
        self.json_data.append({'image_id': image_id, 'category_id': category_id, 'bbox': bbox, 'score': score})


class SavePreLabelJson(SaveJson):
    """保存预标注结果文件类
    """
    def __init__(self, save_json_path):
        super().__init__(save_json_path)

    def parse_info(self, info):
        '''传入json文件内容

        Args:
            info: tuple, 文件内容：图像路径url_image '/sample/path'
                                标注方法datatype: detectbox为标框, dot为标点, contour为标多边形
                                标记点data: [[x1, y1, x2, y2, comment], [x1, y1, x2, y2, comment]...]
                                标注信息tagtype: 标注人员显示的中文信息
                                说明comment: 标注人员自定义录入的信息
                                检测预标注格式：datatype='detectbox', data=[x1, y1, x2, y2], tagtype='box1'
                                关键点预标注格式：datatype='dot', data=[x1, y1, x2, y2, x3, y3, x4, y4]顺时针关键点, tagtype
        '''
        (url_image, datatype, data, tagtype) = info

        result = []
        for line in data:
            result.append({"comment": line[4],  "datatype": datatype,  "data": line[:4],  "tagtype": tagtype})
        
        self.json_data.append({"sha1_image": "5a4e513ed6f491b86e34a8ab6826d35f7289b5df", 
                                "result": result,
                                "dt_checked": "2021-03-14 13:05:55",
                                "uid_tagger": 2926, 
                                "jid_job": 28342377, 
                                "sid_sample": 28342377, 
                                "url_image": url_image, 
                                "uid_checker1": 1048})


class SaveCustomerFlowReIDJson(SaveJson):
    """保存Gucci客流跨境跟踪json文件类
    """
    def __init__(self, save_json_path):
        super().__init__(save_json_path)

    def parse_info(self, info):
        '''传入json文件内容

        Args:
            info: tuple, 文件内容Information:[{"TrackingID": "6",
                                                                            "ImagePath": "path", 
                                                                            "Identity": "Client/Assistant",
                                                                            "HeadShoulderFeature": "base64"}]
        '''
        (device_id, frame_index, Time, Information) = info
        self.json_data.append({"CamSNID": device_id, 
                                                            "FrameNum": frame_index, 
                                                            "Time": Time, 
                                                            "Information": Information})


'''
YAML文件读写
'''
def read_yaml(yaml_path):
    '''读取yaml文件

    Args:
        yaml_path: str, yaml文件路径

    Returns:
        yaml_data: dict, yaml文件内容
    '''
    yaml_data = []
    with open(yaml_path, 'r') as yaml_file:
        yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    
    return yaml_data


'''
CSV文件读写；EXCEL大文件用openpyxl/pandas等加载很慢，建议转成CSV再处理
'''
def read_csv(csv_path):
    '''读取csv文件

    Args:
        csv_path: str, csv文件路径

    Returns:
        reader_data: list, csv文件内容
    '''
    csv_file = open(csv_path, "r")
    reader = csv.reader(csv_file)
    reader_data = list(reader)

    return reader_data


def save_csv(csv_path, info, mode='w'):
    '''保存csv文件

    Args:
        csv_path: str, csv文件路径
        info: list, csv文件内容
        mode: str, 'w'代表覆盖写；'a'代表追加写
    '''
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    csv_file = csv.writer(open(csv_path, mode))
    # csv_file.writerow(['This','is','a','row', 'sample!'])
    csv_file.writerows(info)


'''
TXT文件读写
'''
def read_txt(txt_path):
    '''读取txt文件

    Args:
        txt_path: str, txt文件路径

    Returns:
        txt_data: list, txt文件内容
    '''
    txt_file = open(txt_path, "r")
    txt_data = []
    for line in txt_file.readlines():
        txt_data.append(line.replace('\n', ''))

    return txt_data


def read_yolo_txt(txt_path, width, height, mode='std'):
    '''读取yolo_txt文件

    Args:
        txt_path: str, yolo_txt文件路径
        width: int, 图像的宽
        height: int, 图像的高
        mode: str, 'std'代表标准模式；
                              'with_hip_mid_keypoint'代表包含臀部点

    Returns:
        txt_data: list, yolo_txt文件内容
    '''
    def xywh2xyxy(xywh):
        '''[x, y, w, h]转为[xmin, ymin, xmax, ymax]
        '''
        xmin = int(xywh[0] - xywh[2] / 2)
        ymin = int(xywh[1] - xywh[3] / 2)
        xmax = int(xywh[0] + xywh[2] / 2)
        ymax = int(xywh[1] + xywh[3] / 2)
        xyxy = [xmin, ymin, xmax, ymax]

        return xyxy

    txt_file = open(txt_path, 'r')
    txt_data = []
    for line in txt_file.readlines():
        cls_id = int(line.split(' ')[0])
        box_x = float(line.split(' ')[1]) * width
        box_y = float(line.split(' ')[2]) * height
        box_w = float(line.split(' ')[3]) * width
        box_h = float(line.split(' ')[4]) * height
        if mode == 'std':
            txt_data.append(xywh2xyxy([box_x, box_y, box_w, box_h]) + [cls_id])
        elif mode == 'with_hip_mid_keypoint':
            if float(line.split(' ')[5]) == -1 and float(line.split(' ')[6]) == -1:
                hip_x, hip_y = -1, -1
            else:
                hip_x = float(line.split(' ')[5]) * width
                hip_y = float(line.split(' ')[6]) * height
            txt_data.append(xywh2xyxy([box_x, box_y, box_w, box_h]) + [cls_id] + [hip_x, hip_y])

    return txt_data


def save_txt(txt_path, info, mode='w'):
    '''保存txt文件

    Args:
        txt_path: str, txt文件路径
        info: list, txt文件内容
        mode: str, 'w'代表覆盖写；'a'代表追加写
    '''
    os.makedirs(os.path.split(txt_path)[0], exist_ok=True)
    
    txt_file = open(txt_path, mode)
    for line in info:
        txt_file.write(line + '\n')
    txt_file.close()


'''
XML文件读写
'''
def read_xml(xml_path, mode='std'):
    '''读取xml文件

    Args:
        xml_path: str, xml文件路径
        mode: str, 'std'标准模式读取file_name、size、bndboxes；
                                'with_pred_topk'模式读取时在bndboxes中添加了预测的topk类别；
                                'with_pred_topk_keypoints'模式读取时在bndboxes中添加了预测的topk类别和关键点；
                                'with_hip_mid_keypoint'模式读取时在bndboxes中添加了臀部关键点；
                                'with_headshoulder_box'模式读取时添加了头肩box；

    Returns:
        xml_data: list, xml文件内容
    '''
    xml_target = ET.parse(xml_path).getroot()
    xml_data = {}

    file_name = xml_target.find('filename').text
    xml_data['file_name'] = file_name

    # for size_node in xml_target.iter('size'):
    width =  int(xml_target.find('size').find('width').text)
    height =  int(xml_target.find('size').find('height').text)
    depth =  int(xml_target.find('size').find('depth').text)
    xml_data['size'] = [width, height, depth]

    bndboxes = []
    keypoints = []
    for obj_node in xml_target.iter('object'):
        name = obj_node.find('name').text
        bbox = obj_node.find('bndbox')

        pts = ['xmin', 'ymin', 'xmax', 'ymax']
        bndbox = []
        for i, pt in enumerate(pts):
            cur_pt = int(bbox.find(pt).text)
            bndbox.append(cur_pt)
        bndbox.append(name)

        if mode == 'with_pred_topk':
            pred_cls = obj_node.find('pred_cls')
            classes_name = pred_cls.findall('cls_name')
            for class_name in classes_name:
                bndbox.append(class_name.text)
        elif mode == 'with_pred_topk_keypoints':
            keypoint = obj_node.find('keypoint')
            pred_cls = obj_node.find('pred_cls')
            classes_name = pred_cls.findall('cls_name')
            for class_name in classes_name:
                bndbox.append(class_name.text)
            kpts = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']
            for i, kpt in enumerate(kpts):
                cur_kpt = int(keypoint.find(kpt).text)
                bndbox.append(cur_kpt)
        elif mode == 'with_hip_mid_keypoint':
            keypoint = obj_node.find('midpoint')
            kpts = ['xm', 'ym']
            for i, kpt in enumerate(kpts):
                cur_kpt = int(keypoint.find(kpt).text)
                bndbox.append(cur_kpt)
        elif mode == 'with_headshoulder_box':
            hs_bbox = obj_node.find('hsbndbox')
            pts = ['xmin', 'ymin', 'xmax', 'ymax']
            for i, pt in enumerate(pts):
                cur_pt = int(hs_bbox.find(pt).text)
                bndbox.append(cur_pt)

        bndboxes.append(bndbox)
    
    xml_data['bndboxes'] = bndboxes

    return xml_data


def save_xml(data, xml_path, width, height, classes=None, mode='std'):
    '''保存xml文件

    Args:
        data: list, xml文件内容
        xml_path: str, xml文件路径
        width: int, 图像的宽
        height: int, 图像的高
        mode: str, 'std'标准模式读取file_name、size和bndboxes；
                    'with_pred_topk'模式读取时在bndboxes中添加了预测的topk类别；
                    'with_hip_mid_keypoint'模式添加了臀部关键点；
                    'with_headshoulder_box'模式用于臀部关键点提标时personbox+headshoulderbox记录
    '''
    os.makedirs(os.path.dirname(xml_path), exist_ok=True)

    xml_file = open(xml_path, 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + os.path.basename(xml_path).replace('xml', 'jpg') + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    for obj_index in range(len(data)):
            xml_file.write('    <object>\n')
            if classes is not None:
                xml_file.write('        <name>' + classes[data[obj_index][4]] + '</name>\n')
            else:
                xml_file.write('        <name>' + data[obj_index][4] + '</name>\n')
            xml_file.write('        <pose>Unspecified</pose>\n')
            xml_file.write('        <truncated>0</truncated>\n')
            xml_file.write('        <difficult>0</difficult>\n')
            xml_file.write('        <bndbox>\n')
            xml_file.write('            <xmin>' + str(int(data[obj_index][0])) + '</xmin>\n')
            xml_file.write('            <ymin>' + str(int(data[obj_index][1])) + '</ymin>\n')
            xml_file.write('            <xmax>' + str(int(data[obj_index][2])) + '</xmax>\n')
            xml_file.write('            <ymax>' + str(int(data[obj_index][3])) + '</ymax>\n')
            xml_file.write('        </bndbox>\n')
            if mode == 'with_pred_topk':
                xml_file.write('        <pred_cls>\n')
                for cls_name_index in range(5, len(data[obj_index])):
                    xml_file.write('            <cls_name>' + str(data[obj_index][cls_name_index]) + '</cls_name>\n')
                xml_file.write('        </pred_cls>\n')
            if mode == 'with_hip_mid_keypoint':
                xml_file.write('        <midpoint>\n')
                xml_file.write('            <xm>' + str(data[obj_index][5]) + '</xm>\n')
                xml_file.write('            <ym>' + str(data[obj_index][6]) + '</ym>\n')
                xml_file.write('        </midpoint>\n')
            if mode == 'with_headshoulder_box':
                xml_file.write('        <hsbndbox>\n')
                xml_file.write('            <xmin>' + str(int(data[obj_index][5])) + '</xmin>\n')
                xml_file.write('            <ymin>' + str(int(data[obj_index][6])) + '</ymin>\n')
                xml_file.write('            <xmax>' + str(int(data[obj_index][7])) + '</xmax>\n')
                xml_file.write('            <ymax>' + str(int(data[obj_index][8])) + '</ymax>\n')
                xml_file.write('        </hsbndbox>\n')
            xml_file.write('    </object>\n')

    xml_file.write('</annotation>')
    xml_file.close()


'''
pkl文件读写
'''
def read_pkl(pkl_path):
    '''读取txt文件

    Args:
        pkl_path: str, pickle文件路径

    Returns:
        pkl_data: list, txt文件内容
    '''
    with open(pkl_path, 'rb') as pkl_file:
        pkl_data = pickle.load(pkl_file)

    return pkl_data


'''
杂项
'''
def byte_to_base64(byte_data):
    '''字节转base64编码

    Args:
        file_url: str, 网络文件url
        save_file_path: str, 文件存储路径
    '''
    import base64
    base64_data = base64.b64encode(byte_data)
    base64_data = base64_data.decode()  # 等同于 str(base64_data)
    return base64_data


def download_url(file_url, save_file_path):
    '''下载并存储网络文件

    Args:
        file_url: str, 网络文件url
        save_file_path: str, 文件存储路径
    '''
    import requests
    file_object = requests.get(file_url)
    with open(save_file_path, 'wb') as local_file:
        local_file.write(file_object.content)


def get_last_k_dir_path(path, k):
    '''获取目录中最后k个目录

    Args:
        path: str, 目录路径
        k: int, 获取目录数量

    Returns:
        last_k_dir_path: str, 最后k个目录
    '''
    last_k_dir_path = '/'.join(path.split('/')[-k:])

    return last_k_dir_path


def is_file_empty(file_path):
    '''判断文件是否是空文件

    Args:
        file_path: str, 文件路径

    Returns:
        bool, 为空则为True，否则为False
    '''
    size = os.path.getsize(file_path)
    if size:
        return False
    else:
        return True


def get_str_of_size(size):
    '''字节大小自适应转换为B/KB/MB/GB。递归实现，精确为最大单位值 + 小数点后三位

    Args:
        size: int, 字节大小

    Returns:
        str, 转换后的大小，如39.421 KB
    '''
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return '{}.{:>03d} {}'.format(integer, remainder, units[level])


def others():
    '''文件处理相关的小功能，一两行能实现的
    '''
    # copy file
    shutil.copyfile(src_file, dst_file)
    # copy dir, os.path.mkdir is not needed
    shutil.copytree(src_path, dst_path)
    # move dir
    shutil.move(src_path, dst_path)
    # remove dir
    shutil.rmtree(src_path)
    # remove file
    os.remove(file_path, exist_ok=True)
