# -*- coding: UTF-8 -*-
import os
import shutil
import json, csv, pickle, yaml
import zipfile
import xml.etree.ElementTree as ET
from .Convertion import xywh2xyxy



'''
JSON文件读写
'''
def read_json(json_path, mode='all'):
    '''读取json文件

    Args:
        json_path: str, json文件路径
        mode: str, 'all'模式代表一次性读取json文件全部内容,只存在一个字典；'line'模式代表按行读取json文件内容,每行为一个字典

    Returns:
        json_data: list, json文件内容
    '''
    json_data = []
    with open(json_path, 'r',encoding="UTF-8") as json_file:
        if mode == 'all':
            # 把读取内容转换为python字典
            json_data = json.loads(json_file.read())
        elif mode == 'line':
            for line in json_file:
                json_line = json.loads(line)
                json_data.append(json_line)

    return json_data


def save_json(json_path, info, indent=4, mode='w', with_return_char=False):
    '''保存json文件

    Args:
        json_path: str, json文件路径
        info: dict, json文件内容
        indent: int, 缩进量,默认为4；None代表不缩进
        mode: str, 'w'代表覆盖写；'a'代表追加写
        with_return_char: bool, 写文件时是否在结尾添加换行符
    '''
    #os.makedirs(os.path.split(json_path)[0], exist_ok=True)
    
    # 把python字典转换为字符串
    json_str = json.dumps(info, indent=indent,ensure_ascii=False)
    if with_return_char:
        json_str += '\n'
    
    with open(json_path, mode,encoding="UTF-8") as json_file:
        json_file.write(json_str)
    
    json_file.close()


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
    with open(yaml_path, 'r',encoding="UTF-8") as yaml_file:
        yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    
    return yaml_data



def save_yaml(yaml_path, data, header=''):
    """
    Save YAML data to a file.

    Args:
        file (str, optional): File name. Default is 'data.yaml'.
        data (dict): Data to save in YAML format.
        header (str, optional): YAML header to add.

    Returns:
        (None): Data is saved to the specified file.
    """

    # Convert Path objects to strings
    valid_types = int, float, str, bool, list, tuple, dict, type(None)
    for k, v in data.items():
        if not isinstance(v, valid_types):
            data[k] = str(v)

    # Dump data to file in YAML format
    with open(yaml_path, 'w', errors='ignore', encoding='utf-8') as f:
        if header:
            f.write(header)
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

'''
CSV文件读写；EXCEL大文件用openpyxl/pandas等加载很慢,建议转成CSV再处理
'''
def read_csv(csv_path):
    '''读取csv文件

    Args:
        csv_path: str, csv文件路径

    Returns:
        reader_data: list, csv文件内容
    '''
    csv_file = open(csv_path, "r",encoding="UTF-8")
    reader = csv.reader(csv_file)
    return list(reader)


def save_csv(csv_path, info, mode='w'):
    '''保存csv文件

    Args:
        csv_path: str, csv文件路径
        info: list, csv文件内容
        mode: str, 'w'代表覆盖写；'a'代表追加写
    '''
    
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
    txt_file = open(txt_path, "r",encoding="UTF-8")
    return [line.replace('\n', '') for line in txt_file]

def save_txt(txt_path, info, mode='w'):
    '''保存txt文件

    Args:
        txt_path: str, txt文件路径
        info: list, txt文件内容
        mode: str, 'w'代表覆盖写；'a'代表追加写
    '''
    with open(txt_path, mode) as txt_file:
        for line in info:
            txt_file.write(line + '\n')
    
    
def read_yolo_txt(txt_path, width, height):
    '''读取yolo_txt文件

    Args:
        txt_path: str, yolo_txt文件路径
        width: int, 图像的宽
        height: int, 图像的高


    Returns:
        txt_data: list, yolo_txt文件内容
    '''
    txt_file = open(txt_path, 'r')
    txt_data = []
    for line in txt_file:
        line = line.split()
        cls_id = int(line[0])
        box_x = float(line[1]) * width
        box_y = float(line[2]) * height
        box_w = float(line[3]) * width
        box_h = float(line[4]) * height

        txt_data.append(xywh2xyxy([box_x, box_y, box_w, box_h]) + [cls_id])


    return txt_data



'''
XML文件读写
'''
def read_xml(xml_path):
    '''读取xml文件

    Args:
        xml_path: str, xml文件路径


    Returns:
        xml_data: list, xml文件内容
    '''
    def convert_box(size, box):
          dw, dh = 1. / size[0], 1. / size[1]
          x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
          return x * dw, y * dh, w * dw, h * dh
      
    xml_target = ET.parse(xml_path).getroot()
    file_name = xml_target.find('filename').text
    xml_data = {'file_name': file_name}
    # for size_node in xml_target.iter('size'):
    width =  int(xml_target.find('size').find('width').text)
    height =  int(xml_target.find('size').find('height').text)
    depth =  int(xml_target.find('size').find('depth').text)
    xml_data['size'] = [width, height, depth]

    bndboxes = []
    for obj_node in xml_target.iter('object'):
        name = obj_node.find('name').text
        xmlbox = obj_node.find('bndbox')
        box_xyxy = [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')]
        #box_xywh = convert_box((width, height),box_xyxy)
        bndboxes.append((*box_xyxy,name))

    xml_data['bndboxes'] = bndboxes

    return xml_data


def save_xml(data, xml_path, width, height, classes=None):
    '''保存xml文件

    Args:
        data: list, xml文件内容
        xml_path: str, xml文件路径
        width: int, 图像的宽
        height: int, 图像的高

    '''

    with open(xml_path, 'w') as xml_file:
        xml_file.write('<annotation>\n')
        xml_file.write('    <folder>VOC2007</folder>\n')
        xml_file.write('    <filename>' + os.path.basename(xml_path).replace('xml', 'jpg') + '</filename>\n')
        xml_file.write('    <size>\n')
        xml_file.write(f'        <width>{str(width)}' + '</width>\n')
        xml_file.write(f'        <height>{str(height)}' + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')

        for obj_index in range(len(data)):
            xml_file.write('    <object>\n')
            if classes is not None:
                xml_file.write(f'        <name>{classes[data[obj_index][4]]}' + '</name>\n')
            else:
                xml_file.write(f'        <name>{data[obj_index][4]}' + '</name>\n')
            xml_file.write('        <pose>Unspecified</pose>\n')
            xml_file.write('        <truncated>0</truncated>\n')
            xml_file.write('        <difficult>0</difficult>\n')
            xml_file.write('        <bndbox>\n')
            xml_file.write(f'            <xmin>{int(data[obj_index][0])}' + '</xmin>\n')
            xml_file.write(f'            <ymin>{int(data[obj_index][1])}' + '</ymin>\n')
            xml_file.write(f'            <xmax>{int(data[obj_index][2])}' + '</xmax>\n')
            xml_file.write(f'            <ymax>{int(data[obj_index][3])}' + '</ymax>\n')
            xml_file.write('        </bndbox>\n')
            xml_file.write('    </object>\n')

        xml_file.write('</annotation>')


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

def save_pkl(pkl_path, pkl_data):
    '''保存pkl文件

    Args:
        pkl_path: str, pickle文件路径
        pkl_data: list, txt文件内容
    '''
    with open(pkl_path, 'wb') as pkl_file:
        pickle.dump(pkl_data, pkl_file)

def list_files(basePath, validExts=None, contains=None):
    '''
    遍历文件夹basePath中的文件,如果validExts不为空,则只返回文件扩展名为validExts的文件,
    如果contains不为空,则只返回文件名包含contains的文件
    '''
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        for filename in filenames:
            if contains is not None and filename.find(contains) == -1:
                continue
            ext = filename[filename.rfind("."):].lower()
            if validExts is None or ext.endswith(validExts):
                yield os.path.join(rootDir, filename)



def get_last_k_dir_path(path, k):
    '''获取目录中最后k个目录

    Args:
        path: str, 目录路径
        k: int, 获取目录数量

    Returns:
        last_k_dir_path: str, 最后k个目录
    '''
    last_k_dir_path = os.sep.join(path.split(os.sep)[-k:])

    return last_k_dir_path


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


def is_file_empty(file_path):
    '''判断文件是否是空文件

    Args:
        file_path: str, 文件路径

    Returns:
        bool, 为空则为True,否则为False
    '''
    return not (size := os.path.getsize(file_path))


def get_str_of_size(size):
    '''字节大小自适应转换为B/KB/MB/GB。递归实现,精确为最大单位值 + 小数点后三位

    Args:
        size: int, 字节大小

    Returns:
        str, 转换后的大小,如39.421 KB
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





def exractfile(file, dest):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dest)

def others(src_path, dst_path):
    '''文件处理相关的小功能,一两行能实现的
    '''
    # copy file
    shutil.copyfile(src_path, dst_path)
    # copy dir, os.path.mkdir is not needed
    shutil.copytree(src_path, dst_path)
    # move dir
    shutil.move(src_path, dst_path)
    # remove dir
    shutil.rmtree(src_path)
    # remove file
    os.remove(src_path, exist_ok=True)
