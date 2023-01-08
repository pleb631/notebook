import glob
import cv2
import shutil
import random
import numpy as np

from functools import reduce

from .FileUtils import *
from .ImageVideoUtils import *
from .DataVisualization import *
from .Convertion import YoloVocConvert, VocCocoConvert, is_xyxy_valid


class BasicDataset:
    """数据集基础类
    """
    def label_json_2_traindata(self):
        '''标注json转为训练数据
        '''

    def traindata_2_prelabel_json(self):
        '''训练数据转为标注json
        '''

    def extract_image_every_interval(self, videos_path, interval, save_dir_path, fps=30):
        '''读取视频，每隔interval秒存储一张图像

        Args:
            videos_path: str, 需要提取图像的视频路径列表
            interval: float, 帧间隔时长
            save_dir_path: str, 保存帧路径
            fps: int, 默认视频帧率
        '''
        for video_path in videos_path:
            print('Extracting images from video %s every %f second' % (os.path.basename(video_path), interval))
            capture = cv2.VideoCapture(video_path)
            assert capture.isOpened()

            try:
                fps, width, height, whole_frame_num, current_frame_num, duration, fourcc = get_video_features(capture)
            except (IOError, OverflowError):
                whole_frame_num = -1
            frame_count = 0
            ret, frame = capture.read()
            os.makedirs(save_dir_path, exist_ok=True)

            while ret:
                print('frame_count:', frame_count, ' | ', whole_frame_num)
                if frame_count % int(interval * fps) == 0:
                    cv2.imwrite(os.path.join(save_dir_path, '%s_%06d.jpg' % (os.path.basename(video_path).replace('.mp4', ''),  frame_count)), frame)
                ret, frame = capture.read()
                frame_count += 1
            
            capture.release()

    def filter_gray_error_image(self, image_dir):
        '''删除视频保存中错误的图片，全图大部分为灰色

        Args:
            image_dir: str, 需要进行筛选的图像路径
        '''
        files = os.listdir(image_dir)
        count = 0
        for index, file in enumerate(files):
            print(index)
            image = cv2.imread(image_dir + file)
            if fftCacul(image)[1] < 10:
                count += 1
                print(index, image_dir + file)
                os.remove(image_dir + file)
        print('rm num', count)

    def filter_incomplete_image(self, image_dir_path):
        '''删除指定目录下保存不完整的图像，即无法读取的图像

        Args:
            image_dir_path: str, 需要进行筛选的图像目录路径
        '''
        images_path = glob.glob(image_dir_path + '*.jpg')
        count = 0
        for index, image_path in enumerate(images_path):
            if not is_valid_jpg(image_path):
                count += 1
                print(index, image_path, get_str_of_size(os.path.getsize(image_path)))
                os.remove(image_path)

        print('error num:', count)

    def filter_similar_image(self, image_dir_path, save_image_dir_path, threshold=5):
        '''感知哈希算法去除相似图像。如果不相同的数据位小于等于5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片。
        每张图片计算哈希值，计算两两图像的汉明距离，记录小于阈值的图像对，遍历删除相似图像，得到最终需要保留的图像，保存在同级目录'filtered_images/'下

        Args:
            image_dir_path: str, 需要进行筛选的图像路径
            save_image_dir_path: str, 筛选过的图像保存路径
            threshold: int, 汉明距离阈值
        '''
        # 计算图像哈希值
        def avhash(image):
            if not isinstance(image, Image.Image):
                image = Image.open(image)
            image = image.resize((8, 8), Image.ANTIALIAS).convert('L')
            avg = reduce(lambda x, y: x + y, image.getdata()) / 64.
            return reduce(lambda x, y_z : x | y_z[1] << y_z[0], enumerate(map(lambda i: 0 if i < avg else 1, image.getdata())), 0)

        # 计算哈希值汉明距离
        def hamming(h1, h2):
            h, d = 0, h1 ^ h2
            while d:
                h += 1
                d &= d - 1
            return h

        image_names = glob.glob(image_dir_path+'/*.jpg')

        print('Caculating hash value of images...')
        image_hash_list = []
        for index, image_name in enumerate(image_names):
            print(index, image_name)
            if not is_valid_jpg(image_name):
                image_names.remove(image_name)
                continue
            h_value = avhash(image_name)
            image_hash_list.append((image_name, h_value))

        print('Caculating hamming distance...')
        hamming_list = np.zeros(shape=(len(image_hash_list), len(image_hash_list)))
        for index_i in range(len(image_hash_list)):
            for index_j in range(index_i + 1, len(image_hash_list)):
                hamming_list[index_i, index_j] = hamming(image_hash_list[index_i][1], image_hash_list[index_j][1])

        print('Deleting duplicates')
        remaining_list = image_names.copy()
        for index_i in range(len(image_hash_list)):
            for index_j in range(index_i + 1, len(image_hash_list)):
                if hamming_list[index_i, index_j] <= threshold and (image_hash_list[index_j][0] in remaining_list):
                    print('delete %d %s' % (index_j, image_hash_list[index_j][0]))
                    remaining_list.remove(image_hash_list[index_j][0])

        print('Copying remaining images...')
        for index in range(len(remaining_list)):
            print('keep %s' % (remaining_list[index]))
            os.makedirs(save_image_dir_path, exist_ok=True)
            print(remaining_list[index], os.path.join(save_image_dir_path, os.path.basename(remaining_list[index])))
            shutil.copyfile(remaining_list[index], os.path.join(save_image_dir_path, os.path.basename(remaining_list[index])))


class ClsDataset(BasicDataset):
    """分类模型数据集类
    """
    def label_json_2_traindata(self, json_path, train_data_path, ratio):
        '''将标注结果json文件，转换为训练用图片及训练测试txt

        Args:
            json_path: str, json文件路径
            train_data_path: str, 训练数据保存路径
            ratio: float, 测试集比例
        '''
        json_data = read_json(json_path, 'line')
        img_dir_path = os.path.dirname(json_path) + '/jersey_images/'
        # img_dir_path = '/yuanzifu_data/dataset/physical/jersey_number/src_data/net_20220113/jersey_images/'
        image_types = ['affine_extend_images', 'affine_images', 'bounding_rect_extend_images', 'bounding_rect_images']
        txt_data = []
        error_data = []
        empty_data = []
        train_data = []
        test_data = []
        for idx, line in enumerate(json_data):
            if len(line['result'])==0:
                continue
            image_name = os.path.basename(line['url_image'])
            class_name = line['result'][0]['tagtype']

            print(idx, len(json_data), image_name, class_name)
            
            for image_type in image_types:
                if os.path.exists(os.path.join(img_dir_path, image_type, image_name)):
                    os.makedirs(os.path.join(train_data_path, image_type, class_name), exist_ok=True)
                    shutil.copyfile(os.path.join(img_dir_path, image_type, image_name), 
                                    os.path.join(train_data_path, image_type, class_name, image_name))

            if 'error'==class_name:
                error_data.append('%s,%s' % (image_name, class_name))
            elif 'empty'==class_name:
                empty_data.append('%s,%s' % (image_name, class_name))
            else:
                txt_data.append('%s,%s' % (image_name, class_name))
        
        test_len = max(int(ratio * len(txt_data)), 1)
        rand_list = random.sample(range(0,len(txt_data)), test_len)

        for index in range(len(txt_data)):
            if index in rand_list:
                test_data.append(txt_data[index])
            else:
                train_data.append(txt_data[index])

        save_txt(os.path.join(train_data_path, 'train.txt'), train_data)
        save_txt(os.path.join(train_data_path, 'test.txt'), test_data)
        save_txt(os.path.join(train_data_path, 'error.txt'), error_data)
        save_txt(os.path.join(train_data_path, 'empty.txt'), empty_data)


class ReIDDataset(BasicDataset):
    '''ReID模型数据集类
    '''


class DetDataset(BasicDataset):
    """检测数据集类

    Attributes:
        yolo_voc_convert: YoloVocConvert, YOLO VOC标签转换类
        voc_coco_convert: VocCocoConvert, VOC标签转换类
        vis: DetDataVis, 数据可视化类
    """
    def __init__(self):
        self.yolo_voc_convert = YoloVocConvert()
        self.voc_coco_convert = VocCocoConvert()
        self.vis = DetDataVis()

    def label_json_2_traindata(self, dataset_path, json_path, mode='rect'):
        '''将标注结果json文件，转换为VOC的xml格式
        图像存储于dataset_path+'JPEGImages/'
        标注文件存储于dataset_path+'Annotations_XML/'

        Args:
            dataset_path: str, 数据集路径
            json_path: str, json文件路径
            mode: str, rect代表标注为矩形框；poly代表标注为多边形点
        '''
        json_data = read_json(json_path, 'line')

        for idx, image_label_data in enumerate(json_data):
            image_path = image_label_data['url_image']
            labels = image_label_data['result']
            src_image = cv2.imread(os.path.join(dataset_path, 'JPEGImages', os.path.basename(image_path)))
            height, width, _ = get_image_features(src_image)
            save_path = os.path.join(dataset_path, 'Annotations_XML', os.path.basename(image_path).replace('.jpg', '.xml'))
            print(idx, len(json_data), save_path)

            xml_data = []
            for label in labels:
                # tagtype = label['tagtype']
                tagtype = 'box1'
                if mode == 'rect':
                    xmin = min(int(label['data'][0]), int(label['data'][2]))
                    ymin = min(int(label['data'][1]), int(label['data'][3]))
                    xmax = max(int(label['data'][0]), int(label['data'][2]))
                    ymax = max(int(label['data'][1]), int(label['data'][3]))
                elif mode == 'poly':
                    if len(label['data']) != 8:
                        continue
                    xmin = min(int(label['data'][0]), int(label['data'][2]), int(label['data'][4]), int(label['data'][6]))
                    ymin = min(int(label['data'][1]), int(label['data'][3]), int(label['data'][5]), int(label['data'][7]))
                    xmax = max(int(label['data'][0]), int(label['data'][2]), int(label['data'][4]), int(label['data'][6]))
                    ymax = max(int(label['data'][1]), int(label['data'][3]), int(label['data'][5]), int(label['data'][7]))
                box = [xmin, ymin, xmax, ymax, tagtype]
                # 过滤掉误标为点的检测框，box宽乘高像素数量少于20的
                if (box[2] - box[0]) * (box[3] - box[1]) < 20:
                    continue
                xml_data.append(box)

            save_xml(xml_data, save_path, width, height, mode=mode)

    def traindata2prelabel_json(self, subdir, save_json_path):
        '''训练数据转预标注json格式

        Args:
            subdir: str, 子目录路径
            save_json_path: str, 预标注文件保存绝对路径
        '''
        voc_dir_name = 'Annotations_XML'
        save_pre_label_json = SavePreLabelJson(save_json_path)

        datatype = 'detectbox'
        tagtype = 'box1'
        xml_paths = glob.glob(os.path.join(subdir, voc_dir_name, '*.xml'))
        for idx, xml_path in enumerate(xml_paths):
            print(subdir, idx, len(xml_paths), xml_path)
            url_image = '/sample/%s/%s' % (subdir, os.path.basename(xml_path.replace('.xml', '.jpg')))
            xml_data = read_xml(xml_path)
            boxes = []
            for line in xml_data['bndboxes']:
                data = line[:4]
                boxes.append(data)
            info = (url_image, datatype, boxes, tagtype)
            save_pre_label_json.parse_info(info)

        save_pre_label_json.save_json_data()

    def filter_very_small_boxes_in_xml(self, subdirs, area_thresh=20):
        '''过滤xml文件中误标的极小的框（面积小于阈值），新的xml文件存储于'Annotations_XML_nonsmall'目录下

        Args:
            subdirs: list, 子目录名，不同批次的数据
            area_thresh: int, 极小框面积阈值
        '''
        small_count = 0
        for subdir in subdirs:
            src_xml_paths = glob.glob(os.path.join(self.root, subdir, 'Annotations_XML/*'))
            os.makedirs(os.path.join(self.root, subdir, 'Annotations_XML_nonsmall'), exist_ok=True)
            for idx, src_xml_path in enumerate(src_xml_paths):
                src_xml_data = read_xml(src_xml_path)
                nonsmall_xml_data = []
                small_area_list = []
                for line in src_xml_data['bndboxes']:
                    small_area = (line[2] - line[0]) * (line[3] - line[1])
                    if small_area >= area_thresh:
                        nonsmall_xml_data.append(line)
                    else:
                        small_count += 1
                        small_area_list.append(str(small_area))
                save_xml(nonsmall_xml_data, src_xml_path.replace('Annotations_XML', 'Annotations_XML_nonsmall'), src_xml_data['size'][0], src_xml_data['size'][1])
                print(subdir, idx, len(src_xml_paths), src_xml_path, 'small_count:', small_count, 'areas:', ','.join(small_area_list))

    def crop_img_using_xml(self, display_dir_path, save_bag_image_dir_path, site, extend_ratio):
        '''根据xml文件扩边裁剪图像

        Args:
            display_dir_path: str, 陈列图片（子目录Images/site/*.jpg）和标注xml文件（子目录Labels/site+xml/*.xml）目录路径
            save_bag_image_dir_path: str, 保存裁剪图片目录路径
            site: str, 点位
            extend_ratio: int, 扩边比例，如0.4
        '''
        display_images_path = glob.glob(os.path.join(display_dir_path, 'Images', site, '*.jpg'))
        for image_index, display_image_path in enumerate(display_images_path):
            print(site, image_index, len(display_images_path), display_image_path)
            display_image = cv2.imread(display_image_path)
            display_xml_path = display_image_path.replace('Images', 'Labels').replace('/'+site+'/', '/'+site + 'xml/').replace('.jpg', '.xml')
            display_xml_data = read_xml(display_xml_path)
            for index, info in enumerate(display_xml_data['bndboxes']):
                bbox = info[:4]
                if not is_xyxy_valid(bbox):
                    continue
                bag_class = info[4]
                if bag_class is None:
                    continue
                crop_bag_image = crop_image_extend_border(display_image, bbox, extend_ratio, extend_ratio)

                os.makedirs(os.path.join(save_bag_image_dir_path, bag_class), exist_ok=True)
                crop_bag_image_path = os.path.join(save_bag_image_dir_path, bag_class, site + '_' + os.path.basename(display_image_path).replace('.jpg', '_%05d.jpg' %(index)))
                # print('save %s' % (crop_bag_image_path))
                cv2.imwrite(crop_bag_image_path, crop_bag_image)

    def stick_specified_box_images_on_src_dataset(self, src_images_txt_path, box_images_txt_path, roi, ratio, save_images_dir_path):
        '''在现有数据集原始图像上粘贴指定的小框图像，制作新的图像+标注数据

        Args:
            src_images_txt_path: str, 现有数据集原始图像txt文件路径
            box_images_txt_path: str, 指定小框图像txt文件路径
            roi: list, 在roi区域内生成新框
            save_images_dir_path: str, 新数据保存目录路径
        '''
        src_images = read_txt(src_images_txt_path)
        box_images = read_txt(box_images_txt_path)
        os.makedirs(os.path.join(save_images_dir_path, 'JPEGImages'), exist_ok=True)
        os.makedirs(os.path.join(save_images_dir_path, 'Annotations_XML'), exist_ok=True)
        rand_list = random.sample(range(0,len(src_images)), int(ratio * len(src_images)))

        count = 0
        for src_image_idx, src_image_path in enumerate(src_images):
            if src_image_idx not in rand_list:
                continue
            if 'train_64' in src_image_path:
                continue
            print(count, len(rand_list), src_image_path)
            count += 1
            src_image = cv2.imread(src_image_path)
            src_image_shape = get_image_features(src_image)
            src_image_xml_data = read_xml(src_image_path.replace('/JPEGImages/', '/Annotations_XML/').replace('.jpg', '.xml'))
            box_image_indices = random.sample(range(len(box_images)), random.randint(1, 15))
            current_boxes = src_image_xml_data['bndboxes']
            for box_image_idx in box_image_indices:
                box_image = cv2.imread(box_images[box_image_idx])
                box_image_shape = get_image_features(box_image)
                nonoverlap_box, current_boxes = gen_nonoverlap_box(src_image_shape, box_image_shape, current_boxes, roi)
                src_image[nonoverlap_box[1]:nonoverlap_box[3],nonoverlap_box[0]:nonoverlap_box[2],:] = box_image
            cv2.imwrite(os.path.join(save_images_dir_path, 'JPEGImages', os.path.basename(src_image_path).replace('.jpg', '_aritificial.jpg')), src_image)
            shutil.copyfile(src_image_path.replace('/JPEGImages/', '/Annotations_XML/').replace('.jpg', '.xml'),
                                            os.path.join(save_images_dir_path, 'Annotations_XML', os.path.basename(src_image_path).replace('.jpg', '_aritificial.xml')))

    def gen_perspective_image_xml_of_shelf(self, display_image_dir_path, cur_bag_cls_label_whd_path, width, height):
        '''利用相机内参去除畸变，再利用透视变换把货架图变正，生成对应的透视变换后检测框的xml

        Args:
            display_image_dir_path: str, 陈列图像目录路径，子目录格式为(Images/CDS1/*.jpg, ReID_Pred/CDS1xml/*.xml)
            cur_bag_cls_label_whd_path: str, 女包索引、类别名和对应尺寸文件路径。文件内容格式为“类别索引 类别名 宽 高 深”。
            width: int, 保存透视变换图像的宽
            height: int, 保存透视变换图像的高
        '''
        import sys
        sys.path.insert(0, '.')
        from config.config_shelf_perspective_points import config_shelf_perspective_points

        self.labels = self.read_labels_with_index(cur_bag_cls_label_whd_path)
        image_paths = glob.glob(os.path.join(display_image_dir_path, 'Images', '*', '*'))
        image_paths.sort(key = cmp_to_key(lambda a,b:int(a.split('/')[-1].split('_')[2])-int(b.split('/')[-1].split('_')[2])))

        for index, src_image_path in enumerate(image_paths):
            site = src_image_path.split('/')[-2]
            if site != 'SHS3':
                continue
            src_image = cv2.imread(src_image_path)
            points = config_shelf_perspective_points[site]
            src_image_points, dst_image_points = [], []
            # 包含原始点和目标点
            if len(points) == 2:
                src_image_points = points[0]
                dst_image_points = points[1]
            # 只有原始点，目标点由宽高生成
            elif len(points) == 4:
                src_image_points = points
                dst_image_points = [[0,0], [0,height], [width,height], [width,0]]
            
            undistort_image = get_undistort_image_using_A(src_image_path, 'config/calibration/calib_%s.json' % (site))
            perspective_image = gen_perspective_image(src_image, src_image_points, dst_image_points, width, height)
            perspective_undistort_image = gen_perspective_image(undistort_image, src_image_points, dst_image_points, width, height)

            xml_path = src_image_path.replace('Images', 'Labels').replace('.jpg','.xml').replace('/'+src_image_path.split('/')[-2]+'/', '/'+src_image_path.split('/')[-2]+'xml/')
            xml_data = read_xml(xml_path, mode='std')
            bndboxes = xml_data['bndboxes']

            for bndbox_index, bndbox in enumerate(bndboxes):
                gt_box = [bndbox[0], bndbox[1], bndbox[2], bndbox[3]]
                cv2.rectangle(src_image, (int(gt_box[0]), int(gt_box[1])), (int(gt_box[2]),int(gt_box[3])), (0, 0, 255), 2)

                perspective_box = gen_perspective_boxes(src_image_points, dst_image_points, [gt_box], width, height)[0]
                cv2.rectangle(perspective_image, (int(perspective_box[0]), int(perspective_box[1])), (int(perspective_box[2]),int(perspective_box[3])), (0, 0, 255), 2)
                
                undistort_box = get_undistort_box_using_A(gt_box, 'config/calibration/calib_%s.json' % (site), 1920, 1080)
                cv2.rectangle(undistort_image, (int(undistort_box[0]), int(undistort_box[1])), (int(undistort_box[2]),int(undistort_box[3])), (0, 0, 255), 2)
                
                # 先去畸变再仿射变换
                perspective_undistort_box = gen_perspective_boxes(src_image_points, dst_image_points, [undistort_box], width, height)[0]
                cv2.rectangle(perspective_undistort_image, (int(perspective_undistort_box[0]), int(perspective_undistort_box[1])), (int(perspective_undistort_box[2]),int(perspective_undistort_box[3])), (0, 0, 255), 2)

                bndboxes[bndbox_index][:4] = perspective_undistort_box[:4]
            
            xml_data['bndboxes'] = bndboxes
            
            os.makedirs(os.path.dirname(src_image_path.replace('Images', 'Images_undistort_perspective')), exist_ok=True)
            cv2.imwrite(src_image_path.replace('Images', 'Images_undistort_perspective'), perspective_undistort_image)
            
            os.makedirs(os.path.dirname(xml_path.replace('Labels', 'Labels_undistort_perspective')), exist_ok=True)
            save_xml(bndboxes, xml_path.replace('Labels', 'Labels_undistort_perspective'), 1920,1080, 'std')


class GucciBagDetDataset(DetDataset):
    """Gucci女包检测数据集类
    """
    def merge_boxes_width(self, boxes):
        '''按照检测框的宽合并所有的检测框，返回合并后的线段

        Args:
            boxes: list, 单个图像所有检测框[xmin, ymin, xmax, ymax]的列表

        Returns:
            merge_line_segs: list, 合并后的线段
        '''
        from interval import Interval
        
        # box[xmin, ymin, xmax, ymax]转换为一维宽的线段[xmin, xmax]
        line_segs = []
        for box in boxes:
            line_segs.append(Interval(box[0], box[2]))
        
        # 合并有交集的线段
        line_segs.sort(key = cmp_to_key(lambda a,b:a.lower_bound-b.lower_bound))
        merge_line_segs = []
        for index, line_seg in enumerate(line_segs):
            if len(merge_line_segs) == 0:
                merge_line_segs.append(line_seg)
                continue
            if line_seg.lower_bound not in merge_line_segs[-1]:
                merge_line_segs.append(line_seg)
            else:
                merge_line_segs[-1] = Interval(merge_line_segs[-1].lower_bound, line_seg.upper_bound)
        
        return merge_line_segs

    def gen_perspective_image_of_shelf(self, src_images_dir_path, dst_images_dir_path, width, height):
        '''利用透视变换把货架图变正

        Args:
            src_images_dir_path: str, 原始货架图像目录路径，子目录格式如'CDS1/*.JPG'
            dst_images_dir_path: str, 透视变换后生成的货架图像目录路径
            width: int, 保存透视变换图像的宽
            height: int, 保存透视变换图像的高
        '''
        import sys
        sys.path.insert(0, '.')
        from config.config_shelf_perspective_points import config_shelf_perspective_points

        src_image_paths = glob.glob(src_images_dir_path + '/*/*.jpg')

        for index, src_image_path in enumerate(src_image_paths):
            site = src_image_path.split('/')[-2]
            src_image = cv2.imread(src_image_path)
            points = config_shelf_perspective_points[site]
            # 包含原始点和目标点
            if len(points) == 2:
                src_image_points = points[0]
                dst_image_points = points[1]
            # 只有原始点，目标点由宽高生成
            elif len(points) == 4:
                src_image_points = points
                dst_image_points = [[0,0], [0,height], [width,height], [width,0]]
            perspective_image = gen_perspective_image(src_image, src_image_points, dst_image_points, width, height)
            
            os.makedirs(os.path.dirname(src_image_path.replace(src_images_dir_path, dst_images_dir_path)), exist_ok=True)
            print(index, src_image_path.replace(src_images_dir_path, dst_images_dir_path))
            cv2.imwrite(src_image_path.replace(src_images_dir_path, dst_images_dir_path), perspective_image)

    def analyse_perspective_shelf_cols_from_json(self, json_path, width, height, show_flag=False):
        '''根据女包检测结果json文件，对检测框做透视变换，分析每个图像中货架的列数

        Args:
            json_path: str, 女包检测结果json文件{'image_path':{"box_id":[xmin, ymin, xmax, ymax, conf, cls_id]}}路径
            width: int, 保存透视变换图像的宽
            height: int, 保存透视变换图像的高
            show_flag: bool, 是否将合并后的线段和检测框绘制在图像上，并保存
        '''
        import sys
        sys.path.insert(0, '.')
        from config.config_shelf_perspective_points import config_shelf_perspective_points

        json_data = read_json(json_path, 'all')
        mask_images = get_mask_images(glob.glob(os.getcwd() + '/config/mask/*.jpg'))

        shelf_cols = {}
        for line in json_data:
            site = line.split('/')[-2]
            src_image = cv2.imread(line)
            boxes_info = json_data[line]
            mask_image = mask_images[site]
            
            # 过滤mask外的检测框
            filtered_boxes_info = []
            for box_id in boxes_info:
                box_info = boxes_info[box_id]
                center = get_xyxy_center(box_info[:4])
                if point_in_mask(center, mask_image):
                    filtered_boxes_info.append(box_info[:4])

            points = config_shelf_perspective_points[site]
            # 包含原始点和目标点
            if len(points) == 2:
                src_image_points = points[0]
                dst_image_points = points[1]
            # 只有原始点，目标点由宽高生成
            elif len(points) == 4:
                src_image_points = points
                dst_image_points = [[0,0], [0,height], [width,height], [width,0]]
            
            perspective_boxes = gen_perspective_points(src_image_points, dst_image_points, filtered_boxes_info, width, height)
            perspective_image = gen_perspective_image(src_image, src_image_points, dst_image_points, width, height)
            merge_line_segs = self.merge_boxes_width(perspective_boxes)

            if show_flag:
                img = cv2.imread(line)
                # src image
                # for box in filtered_boxes_info:
                #     cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 2)
                
                # perspective image
                for line_seg in merge_line_segs:
                    cv2.line(perspective_image, (line_seg.lower_bound, int(img.shape[0]/2)), (line_seg.upper_bound, int(img.shape[0]/2)), (0,0,255), 4, 4)

                for box in perspective_boxes:
                    cv2.rectangle(perspective_image, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 2)
                
                os.makedirs(os.path.dirname(line.replace('Images', 'line_segs_show_result/Images')), exist_ok=True)
                # cv2.imwrite(line.replace('Images', 'line_segs_show_result/Images'), img)
                cv2.imwrite(line.replace('Images', 'line_segs_show_result/Images').replace('.jpg', '_perspective.jpg'), perspective_image)
            
            if site not in shelf_cols.keys():
                shelf_cols[site] = []
                shelf_cols[site].append(len(merge_line_segs))
            else:
                shelf_cols[site].append(len(merge_line_segs))
            print("%s\tcols:%d" %(line, len(merge_line_segs)))


class DetKeypointDataset(BasicDataset):
    """检测+关键点数据集类
    """
    def __init__(self, root):
        super().__init__(root)
        self.vis = DetDataVis()

    def crop_image_using_headshoulder_xml_for_keypoint_label(self, src_images_dir_name, src_xmls_dir_name, crop_images_dir_name, crop_xmls_dir_name):
        '''利用头肩框xml裁剪人体小图，并存储小图xml，用于关键点标注

        Args:
            src_images_dir_name: str, 原始图像目录名
            src_xmls_dir_name: str, 原始图像头肩xml目录名
            crop_images_dir_name: str, 裁剪图像目录名
            crop_xmls_dir_name: str, 裁剪图像xml目录名
        '''
        src_images_paths = glob.glob(os.path.join(self.root, src_images_dir_name, '*'))
        for idx, src_image_path in enumerate(src_images_paths):
            print(idx, len(src_images_paths), src_image_path)
            src_image = cv2.imread(src_image_path)
            src_xml_path = src_image_path.replace(src_images_dir_name, src_xmls_dir_name).replace('jpg', 'xml')
            if not os.path.exists(src_xml_path):
                continue
            headshoulder_xml_data = read_xml(src_xml_path)
            src_image_width = headshoulder_xml_data['size'][0]
            src_image_height = headshoulder_xml_data['size'][1]
            for hs_idx, headshoulderbox in enumerate(headshoulder_xml_data['bndboxes']):
                src_image_copy = src_image.copy()
                cv2.rectangle(src_image_copy, (headshoulderbox[0], headshoulderbox[1]), (headshoulderbox[2], headshoulderbox[3]), (0, 0, 255), 3)
                person_box = head_shoulder_box2person_box(headshoulderbox, 4.0, src_image_height, src_image_width)
                crop_image_path = src_image_path.replace(src_images_dir_name, crop_images_dir_name).replace('.jpg','_') + str(hs_idx) + '.jpg'
                crop_xml_path = crop_image_path.replace(crop_images_dir_name, crop_xmls_dir_name).replace('.jpg','.xml')
                crop_image = src_image_copy[person_box[1]:person_box[3],person_box[0]:person_box[2]]
                cv2.imwrite(crop_image_path, crop_image)
                save_xml([person_box + ['box1'] + headshoulderbox[:-1]], crop_xml_path, get_image_features(crop_image)[1], get_image_features(crop_image)[0], mode='with_headshoulder_box')

    def convert_json_2_xml(self, json_path, src_image_dir_path, crop_xml_dir_path, save_dir_path):
        '''将标注结果json文件，转换为VOC的xml格式
        遍历每张原始大图，从json中找到对应的裁剪小图及标注关键点，寻找对应小图xml的头肩框，存储为大图对应的xml文件
        删除无标注结果的对应图像（图像存储于root+'JPEGImages/'，标注文件存储于root+'Annotations_XML/'）

        Args:
            json_path: str, 标注json文件路径
            src_image_dir_path: str, 原始大图目录路径
            crop_xml_dir_path: str, 裁剪图xml目录路径
            save_dir_path: str, 原始大图xml保存路径
        '''
        src_image_2_crop_image = {}
        json_data = read_json(json_path, 'line')
        empty_count = 0
        delete_count = 0
        pass_count = 0
        for line in json_data:
            src_image_name = '_'.join(line['url_image'].split('/')[-1].split('_')[:-1])
            if src_image_name not in src_image_2_crop_image.keys():
                src_image_2_crop_image[src_image_name] = []
            
            if len(line['result']) == 0:
                empty_count += 1
                src_image_2_crop_image[src_image_name].append([line['url_image'].split('/')[-1], [-1, -1]])
            elif line['result'][0]['tagtype'] == 'delete':
                delete_count += 1
                src_image_2_crop_image[src_image_name].append([line['url_image'].split('/')[-1], [-1, -1]])
            else:
                src_image_2_crop_image[src_image_name].append([line['url_image'].split('/')[-1], line['result'][0]['data']])

        src_images_path = os.listdir(src_image_dir_path)
        for idx, src_image_path in enumerate(src_images_path):
            if src_image_path.split('.')[0] not in src_image_2_crop_image.keys():
                continue
            crop_images = src_image_2_crop_image[src_image_path.split('.')[0]]
            for crop_image_idx, info in enumerate(crop_images):
                crop_image_name = info[0]
                # crop_image_xml_data = read_xml(os.path.join(crop_xml_dir_path, '_'.join(crop_image_name.split('_')[:-1])+'#'+crop_image_name.split('_')[-1].replace('jpg', 'xml')), 'with_headshoulder_box')
                crop_image_xml_data = read_xml(os.path.join(crop_xml_dir_path, crop_image_name.replace('jpg', 'xml')), 'with_headshoulder_box')
                crop_images[crop_image_idx].append(crop_image_xml_data['bndboxes'][0])

        os.makedirs(os.path.join(save_dir_path, 'JPEGImages'), exist_ok=True)
        os.makedirs(os.path.join(save_dir_path, 'Annotations_XML'), exist_ok=True)
        for idx, src_image_name in enumerate(src_image_2_crop_image.keys()):
            print(idx, len(src_image_2_crop_image.keys()), src_image_name)
            if not os.path.exists(os.path.join(src_image_dir_path, src_image_name+'.jpg')):
                pass_count += 1
                continue
            shutil.copyfile(os.path.join(src_image_dir_path, src_image_name+'.jpg'), os.path.join(save_dir_path, 'JPEGImages', src_image_name+'.jpg'))
            xml_data = []
            for line in src_image_2_crop_image[src_image_name]:
                if line[1][0] == -1 and line[1][1] == -1:
                    xml_data.append(line[2][5:] + ['box1'] + [-1, -1])
                else:
                    xml_data.append(line[2][5:] + ['box1'] + [line[2][0] + line[1][0], line[2][1] + line[1][1]])
            save_xml(xml_data, os.path.join(save_dir_path, 'Annotations_XML', src_image_name+'.xml'), 1920, 1080, mode='with_hip_mid_keypoint')

        print('pass_count: ', pass_count)


class KeypointDataset(BasicDataset):
    """关键点数据集类
    """
    def gen_train_test_using_json(self, image_dir_path, label_json_path, ratio, show_flag):
        '''利用标注的json文件划分训练测试集，并可视化关键点

        Args:
            image_dir_path: str, 关键点图像根目录路径
            label_json_path: str, 关键点标注文件路径
            ratio: float, 测试集所占比例
            show_flag: bool, 是否可视化
        '''
        json_data = read_json(label_json_path)
        rand_list = random.sample(range(0, len(json_data)), int(len(json_data)*ratio))
        
        train_data, test_data = [], []
        for index, line in enumerate(json_data):
            print(index, len(json_data), line['url_image'])
            if len(line['result']) == 0:
                continue
            if line['result'][0]['tagtype'] == 'delete':
                continue
            image_path = os.path.join(image_dir_path, line['url_image'].replace('/sample/', ''))
            if 'bounding_box_test_445ids' in image_path:
                continue
            image = cv2.imread(image_path)
            height, width, channel = image.shape
            keypoint_info = line['result'][0]['data']
            # 顺时针排序(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,0,image_path)，点5、6与点1、2重合
            x1, y1 = keypoint_info[0] / width, keypoint_info[1] / height
            x2, y2 = keypoint_info[2] / width, keypoint_info[3] / height
            x3, y3 = keypoint_info[4] / width, keypoint_info[5] / height
            x4, y4 = keypoint_info[6] / width, keypoint_info[7] / height
            image_label = '%s,%f,%f,%f,%f,%f,%f,%f,%f' % (image_path,x1,y1,x2,y2,x3,y3,x4,y4)

            if index in rand_list:
                test_data.append(image_label)
            else:
                train_data.append(image_label)

            if show_flag:
                points_array = np.array([[[x1*width,y1*height], [x2*width,y2*height], [x3*width,y3*height], [x4*width,y4*height]]], dtype = np.int32)
                cv2.polylines(image, [points_array], True, (0,255,255), 2)
                cv2.circle(image, (int(x1*width),int(y1*height)), radius = 4, color = (255,0,0), thickness=-1)
                cv2.circle(image, (int(x2*width),int(y2*height)), radius = 4, color = (0,255,0), thickness=-1)
                cv2.circle(image, (int(x3*width),int(y3*height)), radius = 4, color = (0,0,255), thickness=-1)
                cv2.circle(image, (int(x4*width),int(y4*height)), radius = 4, color = (255,255,255), thickness=-1)
                show_image_path = os.path.join(image_dir_path, 'show_label', line['url_image'].replace('/sample/', ''))
                os.makedirs(os.path.dirname(show_image_path), exist_ok=True)
                cv2.imwrite(show_image_path, image)

        save_txt(image_dir_path + 'test_tmp.txt', test_data)
        save_txt(image_dir_path + 'train_tmp.txt', train_data)

    def gen_affine_image_of_reid_img_random_transfrom(self, images_with_keypoints_txt_path, save_image_dir_path, bag_cls_2_label_file_path):
        '''利用关键点生成透视变换后的图像，用于ReID训练

        Args:
            images_with_keypoints_txt_path: str, 带关键点的女包图像txt路径
            save_image_dir_path: str, 保存图像路径
            bag_cls_2_label_file_path, str, bag_cls_2_label文件路径
        '''
        txt_data = read_json(images_with_keypoints_txt_path, 'line')
        dst_image_points = [[16,16], [16,240], [240,16]]
        width, height = 256, 256

        labels = self.read_labels_with_index(bag_cls_2_label_file_path)
        
        os.makedirs(save_image_dir_path, exist_ok=True)
        for index, line in enumerate(txt_data):
            image_path = line['url_image'].replace('/sample/', '/yuanzifu_data/dataset/gucci/bag_keypoint/')
            print(index, len(txt_data), image_path)
            image = cv2.imread(image_path)
            keypoint_info = line['result'][0]['data']

            x1, y1 = int(keypoint_info[0]) , int(keypoint_info[1])
            x2, y2 = int(keypoint_info[2]) , int(keypoint_info[3])
            x3, y3 = int(keypoint_info[4]) , int(keypoint_info[5])
            x4, y4 = int(keypoint_info[6]) , int(keypoint_info[7])
            src_image_points = [[x1,y1],[x4,y4],[x2,y2]]

            affine_image = gen_affine_image(image, src_image_points, dst_image_points, width, height)

            cls_name = os.path.basename(image_path).replace('.jpg', '')
            cls_index = labels.index(cls_name)
            save_image_path = os.path.join(save_image_dir_path, '%06d_c6_pred_%s'%(cls_index, os.path.basename(image_path)))
            cv2.imwrite(save_image_path, affine_image)

            for random_id in range(5):
                pixel = 8
                x1, y1 = int(keypoint_info[0] + random.randint(-pixel, pixel)) , int(keypoint_info[1] + random.randint(-pixel, pixel))
                x2, y2 = int(keypoint_info[2] + random.randint(-pixel, pixel)) , int(keypoint_info[3] + random.randint(-pixel, pixel))
                x3, y3 = int(keypoint_info[4] + random.randint(-pixel, pixel)) , int(keypoint_info[5] + random.randint(-pixel, pixel))
                x4, y4 = int(keypoint_info[6] + random.randint(-pixel, pixel)) , int(keypoint_info[7] + random.randint(-pixel, pixel))
                src_image_points = [[x1,y1],[x4,y4],[x2,y2]]

                affine_image = gen_affine_image(image, src_image_points, dst_image_points, width, height)

                cls_name = os.path.basename(image_path).replace('.jpg', '')
                cls_index = labels.index(cls_name)
                save_image_path = os.path.join(save_image_dir_path, '%06d_c6_%s'%(cls_index, str(random_id) + '_' + os.path.basename(image_path)))
                cv2.imwrite(save_image_path, affine_image)


class JerseyCardKeypointDataset(KeypointDataset):
    """球服号牌关键点数据集类
    """
    def label_json_2_traindata(self, json_path, image_prefix, train_data_path, train_affine_data_path):
        '''将标注结果json文件，转换为训练用图片

        Args:
            json_path: str, json文件路径
            image_prefix: str, 图像路径前缀
            train_data_path: str, 训练数据保存路径
            train_affine_data_path: str, 训练仿射变换数据保存路径
        '''
        json_data = read_json(json_path, 'line')
        os.makedirs(train_data_path, exist_ok=True)
        os.makedirs(train_affine_data_path, exist_ok=True)

        for image_idx, image_res in enumerate(json_data):
            image_path = image_res['url_image']
            print(image_idx, len(json_data), os.path.basename(image_path))
            image = cv2.imread(os.path.join(image_prefix, os.path.basename(image_path)))
            for idx, line in enumerate(image_res['result']):
                kpts = line['data']
                num = line['comment']
                if len(num) != 4 or len(kpts) != 8:
                    continue
                rect = [min(kpts[0], kpts[2], kpts[4], kpts[6]),
                        min(kpts[1], kpts[3], kpts[5], kpts[7]),
                        max(kpts[0], kpts[2], kpts[4], kpts[6]),
                        max(kpts[1], kpts[3], kpts[5], kpts[7])]
                card_image = crop_image_extend_border(image, rect, 0, 0)
                ltf_kpts = quadrilateral_points2left_top_first_quadrilateral([[kpts[0], kpts[1]], [kpts[2], kpts[3]], [kpts[4], kpts[5]], [kpts[6], kpts[7]]], 'left_top_position')
                src_image_points = [ltf_kpts[0], ltf_kpts[3], ltf_kpts[1]]
                dst_image_points = [[0,0], [0,100], [120,0]]
                affine_image = gen_affine_image(image, src_image_points, dst_image_points, 120, 100)
                cv2.imwrite(os.path.join(train_data_path, f'{num}_{os.path.basename(image_path)[:-4]}_{idx:04d}.jpg'), card_image)
                cv2.imwrite(os.path.join(train_affine_data_path, f'{num}_{os.path.basename(image_path)[:-4]}_{idx:04d}.jpg'), affine_image)
