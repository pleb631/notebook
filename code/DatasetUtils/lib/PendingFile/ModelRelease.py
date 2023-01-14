from asyncore import write
from genericpath import exists
import os
import json
import cv2
import numpy as np

from .FileUtils import *
from .ImageVideoUtils import *


class ModelRelease:
    """模型发版基础类

    注意：发版前处理逻辑为：
        1.BGR模式读入图像
        2.BGR模式裁剪、resize图像
        3.不论rgb选项是true还是false，都是在BGR模式下减均值、除以标准差
        4.判断是否需要转换为RGB图像
        pytorch训练如果需要和发版前处理对齐，需要保证读图-resize-均值步骤同在BGR/RGB模式下进行，不能读图-resize在bgr下，均值在rgb下。
        发版时rgb选项尽量为false

    Attributes:
        root: str, 根目录路径
    """
    def __init__(self, root=''):
        self.root = root

    def save_pytorch_weights_cpu(self, ):
        '''cpu模式下只保存pytorch的state_dict()权重
        '''
        pass
        # net_cpu = models.build_model()
        # net = net_cpu().to('cuda:0')
        # torch.save(net_cpu.state_dict(), model_name)

    def downgrade_pth(self, src_pth_file_path, dst_pth_file_path):
        '''将高版本（>1.3）pytorch权重文件降级为低版本（<1.3）可使用的文件，方便低版本pytorch转caffe
        '''
        import torch

        torch.save(torch.load(src_pth_file_path) , dst_pth_file_path, _use_new_zipfile_serialization=False)

    def convert_rgb_to_bgr(self, src_prototxt_file_path, src_caffemodel_file_path, dst_caffemodel_file_path):
        '''模型第一层由rgb转为bgr

        Args:
            src_prototxt_file_path: str, 原始模型prototxt文件路径
            src_caffemodel_file_path: str, 原始模型caffemodel文件路径
            dst_caffemodel_file_path: str, 转换后模型caffemodel文件路径
        '''
        import caffe
        net = caffe.Net(src_prototxt_file_path, src_caffemodel_file_path, caffe.TEST)
        name = 'ConvNd_1'
        weight = net.params[name][0].data
        weight = weight[:,::-1]
        net.params[name][0].data[...] = weight
        net.save(dst_caffemodel_file_path)

    def resize_calibset(self, calibset_path, width, height):
        '''校准集图像修改尺寸

        Args:
            calibset_path: str, 生成校准集路径
            width: int, 校准集图像宽
            height: int, 校准集图像高
        '''
        images_paths = glob.glob(os.path.join(calibset_path, 'calibset_images', '*jpg'))
        for idx, image_path in enumerate(images_paths):
            print(colorstr('Resize Calib Images:'), idx, len(images_paths), get_last_k_dir_path(image_path, 3))
            cv2.imwrite(image_path, cv2.resize(cv2.imread(image_path), (width, height)))

    def gen_calibset_json(self, calibset_path):
        '''生成线上校准集json文件，并自动打包

        Args:
            calibset_path: str, 校准集路径
        '''
        images_paths = os.listdir(os.path.join(calibset_path, 'calibsets', 'calibset_images'))
        for idx, image_path in enumerate(images_paths):
            print(colorstr('Write Json Lines:'), idx, len(images_paths), get_last_k_dir_path(image_path, 3))
            save_json(os.path.join(calibset_path, 'calibsets', 'calibset.json'), {"image":"calibset_images/" + image_path}, None, 'a', True)

        print(colorstr(f"cd {calibset_path} && tar -czvf calibsets.tar.gz calibsets"))
        os.system(f"cd {calibset_path} && tar -czvf calibsets.tar.gz calibsets")


    def gen_calibset(self, file_txt_path, image_prefix, calibset_path, resize_wh=None):
        '''生成线上校准集图片及json文件

        Args:
            file_txt_path: str, 所选中的校准集图片txt文件路径，可用shuf等命令生成
            image_prefix: str, 校准集图片前缀
            calibset_path: str, 生成校准集路径
            resize_wh: tuple(w, h), 校准集图片缩放尺寸
        '''
        os.makedirs(os.path.join(calibset_path, 'calibsets', 'calibset_images'), exist_ok=True)

        images_paths = read_txt(file_txt_path)

        for idx, image_path in enumerate(images_paths):
            print(colorstr('Copy Calib Images:'), idx, len(images_paths), get_last_k_dir_path(image_path, 3))
            src_image_path = os.path.join(image_prefix, image_path)
            dst_image_path = os.path.join(calibset_path, 'calibsets', 'calibset_images', os.path.basename(image_path))
            
            shutil.copyfile(src_image_path, dst_image_path)

        if resize_wh:
            (width, height) = resize_wh
            self.resize_calibset(os.path.join(calibset_path, 'calibsets'), width, height)

        self.gen_calibset_json(calibset_path)


class ModelReleaseCls(ModelRelease):
    """分类模型发版类
    """
    def gen_testset(self, src_testset_file_path, image_prefix, dst_testset_path):
        '''生成线上测试集格式

        Args:
            src_testset_file_path: str, 测试集文件路径，文件每行内容为"路径,类别id"
            image_prefix: str, 图像路径前缀
            dst_testset_path: str, 生成线上测试集目标路径
        '''
        os.makedirs(dst_testset_path + '/images/', exist_ok=True)
        os.makedirs(dst_testset_path + '/testlist/', exist_ok=True)
        
        src_testset_data = read_txt(src_testset_file_path)

        CLASSES = ['stand', 'less_45', 'empty']
        tagnameid = [1805001001, 1805001002, 1805001003]

        for idx, line in enumerate(src_testset_data):
            print(idx, len(src_testset_data), line)
            src_file = os.path.join(image_prefix, line.split(',')[0])
            class_name = line.split(',')[1]
            class_idx = CLASSES.index(class_name)
            dst_file = dst_testset_path + '/images/' + class_name + '_' + os.path.basename(line.split(',')[0])
            shutil.copyfile(src_file, dst_file)

            # json格式
            # json_data = {"image": "images/" + class_name + '_' + os.path.basename(line.split(',')[0]), "result": [{"tagnameid": 1804001007, "data": [class_idx], "evaltype": "bag_accuracy"}]}
            result = []
            for tag_idx in range(len(tagnameid)):
                data = [1] if tag_idx == class_idx else [0]
                result.append({"tagnameid": tagnameid[tag_idx], "data": data, "evaltype": "classify"})
            json_data = {"image": "images/" + class_name + '_' + os.path.basename(line.split(',')[0]), "result": result}
            save_json(dst_testset_path + 'testlist/test.json', json_data, None, 'a', True)


class ModelReleaseDet(ModelRelease):
    """检测模型发版类
    """
    def gen_testset(self, src_testset_file_path, dst_testset_path, tagnameid):
        '''生成线上测试集格式

        Args:
            src_testset_file_path: str, 测试集文件路径
            dst_testset_path: str, 生成测试集路径
            tagnameid: int, 线上编号
        '''
        os.makedirs(dst_testset_path + '/images/', exist_ok=True)
        os.makedirs(dst_testset_path + '/testlist/', exist_ok=True)
        
        images_paths = read_txt(src_testset_file_path)

        for idx, image_path in enumerate(images_paths):
            print(idx, len(images_paths), image_path)
            
            src_file = image_path
            dst_file = dst_testset_path + '/images/' + os.path.basename(src_file)
            shutil.copyfile(src_file, dst_file)

            # gt
            gts = read_xml(src_file.replace('JPEGImages', 'Annotations_XML').replace('.jpg', '.xml'))
            result = []
            for gt in gts['bndboxes']:
                result.append({"tagnameid": tagnameid, "data": gt[:4], "evaltype": "map", "difficult": 0})

            # json格式
            json_data = {"image": "images/" + os.path.basename(src_file), "result": result}
            save_json(dst_testset_path+'/testlist/test.json', json_data, indent=None, mode='a', with_return_char=True)

    def show_test_results(self, root_path, gt_json, pred_json):
        test_gt_results = read_json(root_path + 'testlist/' + gt_json)
        test_results = read_json(root_path + pred_json)
        for index in range(len(test_results)):
            result = test_results[index]
            gt_result = test_gt_results[index]
            image_path = root_path + result['image']
            image = cv2.imread(image_path)
            # gts
            # for box_index in range(len(gt_result['result'])):
            #     gt_box = gt_result['result'][box_index]['data']
            #     cv2.rectangle(image, (int(gt_box[0]), int(gt_box[1])), (int(gt_box[2]), int(gt_box[3])), (0, 255, 0), 2)
            # preds
            for box_index in range(len(result['result'])):
                box = result['result'][box_index]['data']
                conf = result['result'][box_index]['confidence'][0]
                # cv2.putText(image, str(conf), (int(box[0]), int(box[1])), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 0), 2)
                cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
            cv2.imshow('show', image)
            cv2.waitKey(0)

    def convert_result_json_2_coco_json(self, testset_json_path, ezi_result_json_path, save_coco_json_path, box_threshold=0.3):
        '''发版平台生成的检测结果json转换为coco格式
        注意coco的bbox格式为: [xmin, ymin, w, h]！！！！！！而非[xmin, ymin, xmax, ymax]
        
        Args:
            testset_json_path: str, 测试集json文件路径，为了与coco gt json中图像index保持一致
            save_coco_json_path: str, coco文件保存路径
            ezi_result_json_path: str, 发版平台结果json文件路径
            box_threshold: float, 检测框阈值
        '''
        save_coco_pred_json = SaveCocoPredJson(save_coco_json_path)

        testset_json_data = read_json(testset_json_path, 'line')
        ezi_result_json_data = read_json(ezi_result_json_path, 'line')

        images_path = []
        for line in testset_json_data:
            images_path.append(line['image'])

        results = {}
        for line in ezi_result_json_data:
            results['/'.join(line['image'].split('/')[-2:])] = line['result']

        category_id = 0
        for image_id, image_path in enumerate(images_path):
            print(image_id, len(images_path))
            result = results[image_path]
            for box in result:
                bbox = xyxy2xywh_min([round(box['data'][0]), round(box['data'][1]), round(box['data'][2]), round(box['data'][3])])
                score = round(box['confidence'][0], 5)
                if score >= box_threshold:
                    info = (image_id, category_id, bbox, score)
                    save_coco_pred_json.parse_info(info)

        print('saving coco json')
        save_coco_pred_json.save_json_data()


class ModelReleaseSTR(ModelRelease):
    """字符识别模型发版类
    """
    def gen_testset(self, src_testset_file_path, image_prefix, dst_testset_path, tagnameid):
        '''生成线上测试集格式

        Args:
            src_testset_file_path: str, 测试集文件路径，文件每行内容为"路径,类别"
            image_prefix: str, 图像路径前缀
            dst_testset_path: str, 生成线上测试集目标路径
            tagnameid: int, 线上编号
        '''
        os.makedirs(dst_testset_path + '/images/', exist_ok=True)
        os.makedirs(dst_testset_path + '/testlist/', exist_ok=True)
        
        src_testset_data = read_txt(src_testset_file_path)
        
        for idx, src_file in enumerate(src_testset_data):
            print(idx, len(src_testset_data), src_file)

            gt = src_file.split(',')[-1].replace('?', '').replace('？', '')

            src_file = image_prefix + src_file.split(',')[0]
            dst_file = dst_testset_path + '/images/' + os.path.basename(src_file)
            shutil.copyfile(src_file, dst_file)
            
            json_data = {'image': '', 'result': [{"evaltype": "plate_accuracy", "tagnameid": tagnameid, "data": []}]}
            json_data['image'] = "images/" + os.path.basename(src_file)
            for i in range(len(gt)):
                json_data['result'][0]['data'].append(int(gt[i])+1)
                
            save_json(dst_testset_path+'/testlist/test.json', json_data, indent=None, mode='a', with_return_char=True)


class ModelReleaseDetWithKpt(ModelRelease):
    """检测模型发版类
    """
    def gen_testset(self, src_testset_file_path, dst_testset_path, tagnameid):
        '''生成线上测试集格式

        Args:
            src_testset_file_path: str, 测试集文件路径
            dst_testset_path: str, 生成测试集路径
            tagnameid: tuple, (box_tagname, kpt_tagname)
        '''
        os.makedirs(dst_testset_path + '/images/', exist_ok=True)
        os.makedirs(dst_testset_path + '/testlist/', exist_ok=True)
        
        # tag_uid = []
        src_testset_file = open(src_testset_file_path, 'r')
        # tag_uid_file = open(tag_uid_path, 'r')
        json_file = open(dst_testset_path + 'testlist/test.json', 'w')

        # for line in tag_uid_file.readlines()[2:]:
        #     id = line.split('\t')[1]
        #     tag_uid.append(int(id))

        lines = src_testset_file.readlines()
        for idx, line in enumerate(lines):
            src_file = line.replace('\n', '')
            print(idx, len(lines), src_file)
            dst_file = dst_testset_path + '/images/' + os.path.basename(src_file)
            shutil.copyfile(src_file, dst_file)

            # gt
            gts = read_xml(src_file.replace('JPEGImages', 'Annotations_XML').replace('.jpg', '.xml'), 'with_hip_mid_keypoint')
            result = []
            for gt in gts['bndboxes']:
                result.append({"tagnameid": tagnameid[0], "data": gt[:4], "evaltype": "map_pck_box", "difficult": 0})
                result.append({"tagnameid": tagnameid[1], "data": gt[5:], "evaltype": "map_pck_kpt"})

            # json格式
            json_data = {"image": "images/" + os.path.basename(src_file), "result": result}
            json_file.write(json.dumps(json_data))
            json_file.write("\n")

        src_testset_file.close()
        # tag_uid_file.close()
        json_file.close()

    def convert_result_json_2_coco_json(self, testset_json_path, ezi_result_json_path, save_coco_only_box_json_path, save_coco_box_with_kpt_json_path, box_threshold=0.3):
        '''发版平台生成的检测结果json转换为coco格式
        注意coco的bbox格式为: [xmin, ymin, w, h]！！！！！！而非[xmin, ymin, xmax, ymax]
        
        Args:
            testset_json_path: str, 测试集json文件路径，为了与coco gt json中图像index保持一致
            ezi_result_json_path: str, 发版平台结果json文件路径
            save_coco_only_box_pred_json: str, coco文件保存路径
            save_coco_box_with_kpt_pred_json: str, 带关键点的coco文件保存路径
            box_threshold: float, 检测框阈值
        '''
        save_coco_only_box_pred_json = SaveCocoPredJson(save_coco_only_box_json_path)
        save_coco_box_with_kpt_pred_json = SaveCocoPredJson(save_coco_box_with_kpt_json_path)

        testset_json_data = read_json(testset_json_path, 'line')
        ezi_result_json_data = read_json(ezi_result_json_path, 'line')

        images_path = []
        for line in testset_json_data:
            images_path.append(line['image'])

        results = {}
        for line in ezi_result_json_data:
            results['/'.join(line['image'].split('/')[-2:])] = line['result']

        category_id = 0
        for image_id, image_path in enumerate(images_path):
            print(image_id, len(images_path), image_path)
            result = results[image_path]
            for idx in range(len(result)//2):
                box = result[idx*2]
                kpt = result[idx*2 + 1]
                bbox = xyxy2xywh_min([round(box['data'][0]), round(box['data'][1]), round(box['data'][2]), round(box['data'][3])])
                bbox_with_kpt = bbox + kpt['data']
                score = round(box['confidence'][0], 5)
                if score >= box_threshold:
                    info = (image_id, category_id, bbox, score)
                    info_with_kpt = (image_id, category_id, bbox_with_kpt, score)
                    save_coco_only_box_pred_json.parse_info(info)
                    save_coco_box_with_kpt_pred_json.parse_info(info_with_kpt)

        print('saving coco json')
        save_coco_only_box_pred_json.save_json_data()
        save_coco_box_with_kpt_pred_json.save_json_data()

class ModelReleaseReID(ModelRelease):
    """ReID模型发版类
    """
    def gen_testset(self, src_query_file_path, src_gallery_file_path, dst_testset_path):
        '''生成线上测试集格式

        Args:
            src_query_file_path: str, 测试集query文件路径
            src_gallery_file_path: str, 测试集gallery文件路径
            dst_testset_path: str, 生成线上测试集目标路径
            mode: str, 若为'basename'，只使用图片名字拷贝；若为'with_sec_dir'，使用'倒数第二层目录+_+图片名字'方式拷贝
        '''
        os.makedirs(dst_testset_path + '/images/', exist_ok=True)
        os.makedirs(dst_testset_path + '/testlist/', exist_ok=True)
        
        src_query_file = open(src_query_file_path, 'r')
        src_gallery_file = open(src_gallery_file_path, 'r')
        json_file = open(dst_testset_path + 'testlist/test.json', 'w')

        # query图像
        for line in src_query_file.readlines():
            src_file = self.root + line.replace('\n', '')
            class_id = int(line.replace('\n', '').split('/')[-1].split('_')[0])
            dst_file = dst_testset_path + '/images/' + line.split('/')[-2] + '_' + os.path.basename(line.replace('\n', ''))
            shutil.copyfile(src_file, dst_file)

            # json格式
            json_data = {"image": "images/" + line.split('/')[-2] + '_' + os.path.basename(line.replace('\n', '')), 
                                        "result": [{"is_query": True, "tagnameid": 2500101001, "data": [class_id], "evaltype": "reid_roc"}]}
            json_file.write(json.dumps(json_data))
            json_file.write("\n")

        # gallery图像
        for line in src_gallery_file.readlines():
            src_file = self.root + line.replace('\n', '')
            class_id = int(line.replace('\n', '').split('/')[-1].split('_')[0])
            dst_file = dst_testset_path + '/images/' + line.split('/')[-2] + '_' + os.path.basename(line.replace('\n', ''))
            shutil.copyfile(src_file, dst_file)

            # json格式
            json_data = {"image": "images/" + line.split('/')[-2] + '_' + os.path.basename(line.replace('\n', '')), 
                                        "result": [{"is_query": False, "tagnameid": 2500101001, "data": [class_id], "evaltype": "reid_roc"}]}
            json_file.write(json.dumps(json_data))
            json_file.write("\n")

        src_query_file.close()
        src_gallery_file.close()
        json_file.close()

class ModelReleaseKeypoint(ModelRelease):
    """检测模型发版类
    """
    def gen_testset(self, src_testset_file_path, dst_testset_path, tagnameid):
        '''生成线上测试集格式

        Args:
            src_testset_file_path: str, 测试集文件路径
            dst_testset_path: str, 生成测试集路径
            tagnameid: int, 线上编号
        '''
        os.makedirs(dst_testset_path + '/images/', exist_ok=True)
        os.makedirs(dst_testset_path + '/testlist/', exist_ok=True)
        
        txt_data = read_txt(src_testset_file_path)
        json_file = open(dst_testset_path + 'testlist/test.json', 'w')

        for line in txt_data:
            image_path = line.split(',')[0]
            image = cv2.imread(image_path)
            height, width, channel = get_image_features(image)
            keypoints_ratio = line.split(',')[1:]
            keypoints = []
            for index, kp in enumerate(keypoints_ratio):
                if index%2 == 0:
                    keypoints.append(int(float(kp) * width))
                else:
                    keypoints.append(int(float(kp) * height))
            
            dst_image_path = os.path.join(dst_testset_path, 'images', image_path.split('/')[-2] + '_' + os.path.basename(image_path))
            print(image_path, dst_image_path)
            shutil.copyfile(image_path, dst_image_path)

            # json格式
            json_data = {"image": "images/" + image_path.split('/')[-2] + '_' + os.path.basename(image_path), 
                                        "result": [{"tagnameid": tagnameid, "data": keypoints, "index":[0,1,2,3], "evaltype": "ned"}]}
            json_file.write(json.dumps(json_data))
            json_file.write("\n")

        json_file.close()
