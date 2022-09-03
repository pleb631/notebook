import os
import json
import numpy as np
import pickle
import yaml
import csv


__all__ = ["txt","pkl","json","csv",
           "byte_to_base64","download_url"]


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
