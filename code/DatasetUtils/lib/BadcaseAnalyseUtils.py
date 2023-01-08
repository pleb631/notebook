import glob
import cv2
import numpy as np
import os
import pandas as pd

from .FileUtils import *
from .ImageVideoUtils import *
from .DataVisualization import *
from .Math import Distance
from .Convertion import get_xyxy_center


class BadcaseAnalyseUtils:
    """Badcase分析工具基础类

    Attributes:
        distance: Distance, 距离计算类
        vis_utils: DataVisualization, 数据可视化类
    """
    def __init__(self):
        self.distance = Distance()
        self.vis_utils = None

    def match_boxes_hungarian(self, boxes_a, boxes_b):
        '''单张图像中，利用匈牙利匹配匹配两个box集合

        Args:
            boxes_a: list, boxes集合a
            boxes_b: list, boxes集合b

        Returns:
            matched_boxes: list, 匹配上的boxes
            unmatched_boxes_a: list, boxes集合a中未匹配上的
            unmatched_boxes_b: list, boxes集合b中未匹配上的
        '''
        from scipy.optimize import linear_sum_assignment
        matched_boxes= []

        boxes_a_xy = [line[:4] for line in boxes_a]
        boxes_b_xy = [line[:4] for line in boxes_b]

        idxes_a = list(range(len(boxes_a)))
        idxes_b = list(range(len(boxes_b)))

        distance_matrix = self.distance.calcu_boxes_ab_distance(boxes_a_xy, boxes_b_xy)

        rows, cols = linear_sum_assignment(distance_matrix)

        for box_a_idx, box_b_idx in zip(rows, cols):
            if distance_matrix[box_a_idx, box_b_idx] != 999999:
                matched_boxes.append(boxes_a[box_a_idx]+boxes_b[box_b_idx])
                idxes_a.remove(box_a_idx)
                idxes_b.remove(box_b_idx)

        unmatched_boxes_a = [boxes_a[idx] for idx in idxes_a]
        unmatched_boxes_b = [boxes_b[idx] for idx in idxes_b]

        return matched_boxes, unmatched_boxes_a, unmatched_boxes_b

    def match_boxes_iou(self, boxes_a, boxes_b, iou_mode='iou', iou_threshold=0.5):
        '''单张图像中，利用iou匹配两个box集合

        Args:
            boxes_a: list, boxes集合a
            boxes_b: list, boxes集合b
            iou_mode: str, 'iou'代表iou
                            'diou'代表diou
            iou_threshold: float, iou阈值，默认为0.5

        Returns:
            matched_boxes: list, 匹配上的boxes
            unmatched_boxes_a: list, boxes集合a中未匹配上的
            unmatched_boxes_b: list, boxes集合b中未匹配上的
        '''
        matched_boxes= []

        boxes_a_xy = [line[:4] for line in boxes_a]
        boxes_b_xy = [line[:4] for line in boxes_b]

        idxes_a = list(range(len(boxes_a)))
        idxes_b = list(range(len(boxes_b)))

        iou_list = self.distance.calcu_boxes_ab_iou(boxes_a_xy, boxes_b_xy, iou_mode, 'list')

        iou_list.sort(key = cmp_to_key(lambda a,b:b[2]-a[2]))

        for idx, elem in enumerate(iou_list):
            box_a_idx, box_b_idx, iou = elem
            if (box_a_idx in idxes_a) and (box_b_idx in idxes_b):
                if iou > iou_threshold:
                    matched_boxes.append(boxes_a[box_a_idx]+boxes_b[box_b_idx]+[iou])
                    idxes_a.remove(box_a_idx)
                    idxes_b.remove(box_b_idx)

        unmatched_boxes_a = [boxes_a[idx] for idx in idxes_a]
        unmatched_boxes_b = [boxes_b[idx] for idx in idxes_b]

        return matched_boxes, unmatched_boxes_a, unmatched_boxes_b

class ClsBadcaseUtils(BadcaseAnalyseUtils):
    '''分类模型Badcase工具类

    Attributes:
        root: str, 根目录路径
        save_dir_path: str, 需要保存文件的路径
    '''
    def __init__(self):
        super().__init__()
        self.vis_utils = ClsDataVis()


class DetBadcaseUtils(BadcaseAnalyseUtils):
    '''检测模型Badcase工具类
    '''
    def __init__(self):
        super().__init__()
        self.vis_utils = DetDataVis()

    def filter_box_out_of_mask(self, boxes_list, mask_image):
        '''过滤mask外的检测框

        Args:
            boxes_list: list, 检测框列表，格式[[xmin,ymin,xmax,ymax,...],]
            mask_image: np.array, mask图像

        Returns:
            filtered_boxes: list, 正确检测到的框(pred_box)
        '''
        filtered_boxes = []
        for box_info in boxes_list:
            center = get_xyxy_center(box_info[:4])
            if point_in_mask(center, mask_image):
                filtered_boxes.append(box_info)

        return filtered_boxes

    def analyse_false_miss_box(self, gt_boxes, pred_boxes, iou_threshold=0.5):
        '''分析单张图像pred框相对于gt框的误检和漏检框

        Args:
            gt_boxes: list, gt检测框，格式[[xmin,ymin,xmax,ymax,cls_id],]
            pred_boxes: list, pred检测框，格式[[xmin,ymin,xmax,ymax,conf,cls_id],]
            iou_threshold: float, iou阈值，判断pred检测框是否匹配上某一gt检测框

        Returns:
            correct_boxes: list, 正确检测到的框(pred_box+gt_box)
            incorrect_boxes: list, 误检的框(pred_box)
            missed_boxes: list, 漏检的框(gt_box)
            misclassified_boxes: list, 位置检测正确、类别预测错的框(pred_box)
        '''
        # 预测框按照置信度大小排序
        gt_boxes_array = np.array(gt_boxes)
        pred_boxes.sort(key = cmp_to_key(lambda a,b:b[4]-a[4]))
        pred_boxes_array = np.array(pred_boxes)

        correct_boxes = []
        missed_boxes = []
        incorrect_boxes = []
        
        nd = len(pred_boxes_array)
        gt_len = len(gt_boxes_array)
        flag_gt = np.zeros(gt_len)
        if gt_len > 0:
            for index in range(nd):
                pre_box = pred_boxes_array[index, :].astype(float)
                
                ixmin = np.maximum(gt_boxes_array[:, 0], pre_box[0])
                iymin = np.maximum(gt_boxes_array[:, 1], pre_box[1])
                ixmax = np.minimum(gt_boxes_array[:, 2], pre_box[2])
                iymax = np.minimum(gt_boxes_array[:, 3], pre_box[3])
                iw = np.maximum(ixmax - ixmin + 1., 0.)
                ih = np.maximum(iymax - iymin + 1., 0.)
                inters = iw * ih
                uni = ((pre_box[2] - pre_box[0] + 1.) * (pre_box[3] - pre_box[1] + 1.) +
                    (gt_boxes_array[:, 2] - gt_boxes_array[:, 0] + 1.) *
                    (gt_boxes_array[:, 3] - gt_boxes_array[:, 1] + 1.) - inters)

                overlaps = inters / uni
                ovmax = np.max(overlaps)
                jmax = np.argmax(overlaps)
                
                if ovmax >= iou_threshold:
                    if flag_gt[jmax] < 1:
                        correct_boxes.append(pre_box.tolist() + gt_boxes_array[jmax, :].tolist())
                        flag_gt[jmax] = 1
                    else:
                        incorrect_boxes.append(pre_box.tolist())
                else:
                    incorrect_boxes.append(pre_box.tolist())
            for id in range(gt_len):
                if flag_gt[id] < 1:
                    missed_boxes.append(gt_boxes_array[id, :])
       
        return correct_boxes, incorrect_boxes, missed_boxes

    def save_false_miss_det_image(self, pred_json_path, save_dir_path, crop_bad_box_flag=False):
        '''保存误检和漏检的badcase图像；绿框代表正确预测框，红框代表误检框，蓝框代表漏检框

        Args:
            pred_json_path: str, 检测结果json文件路径；gt从图片路径对应的Annotations文件夹txt文件中读取
            save_dir_path: str, 保存图像的路径
            crop_bad_box_flag: str, 是否裁剪出误检和漏检框
        '''
        json_data = read_json(pred_json_path, 'all')
        os.makedirs(os.path.join(save_dir_path, 'draw_box'), exist_ok=True)
        if crop_bad_box_flag:
            os.makedirs(os.path.join(save_dir_path, 'false_box'), exist_ok=True)
            os.makedirs(os.path.join(save_dir_path, 'miss_box'), exist_ok=True)

        for index, image_path in enumerate(json_data.keys()):
            correct_boxes, false_boxes, missed_boxes = [], [], []
            imageName = os.path.basename(image_path)
            assert os.path.exists(image_path), 'image_path: {} is not exists! '.format(image_path)
            image = cv2.imread(image_path)
            if image is None:
                continue
            txtPath =  image_path.replace('JPEGImages', 'Annotations').replace('.jpg', '.txt')
            gt_boxes = read_yolo_txt(txtPath, image.shape[1], image.shape[0])
            pred_boxes_list =  json_data[image_path]

            if len(gt_boxes) == 0 and len(pred_boxes_list) == 0:
                continue

            correct_boxes, false_boxes, missed_boxes = self.analyse_false_miss_box(gt_boxes, pred_boxes_list)

            if len(false_boxes) != 0 or len(missed_boxes) != 0:
                print('count %d/%d in %s' % (index, len(json_data.keys()), image_path))
                show_image = self.vis_utils.badcase_det_box_vis(image.copy(), correct_boxes, false_boxes, missed_boxes)
                cv2.imwrite(os.path.join(save_dir_path, 'draw_box', imageName), show_image)

            if crop_bad_box_flag:
                if len(false_boxes) != 0:
                    for idx, false_box in enumerate(false_boxes):
                        if float(false_box[4]) > 0.5:
                            continue
                        false_box_img = crop_image_extend_border(image, false_box[:4], .0, .0)
                        cv2.imwrite(os.path.join(save_dir_path, 'false_box', f'{idx}_{imageName}'), false_box_img)
                if len(missed_boxes) != 0:
                    for idx, missed_box in enumerate(missed_boxes):
                        missed_box_img = crop_image_extend_border(image, missed_box, .0, .0)
                        cv2.imwrite(os.path.join(save_dir_path, 'miss_box', f'{idx}_{imageName}'), missed_box_img)


class GucciHSDetHipBadcaseUtils(DetBadcaseUtils):
    '''Gucci头肩检测+臀部关键点模型Badcase工具类
    '''
    def save_false_miss_det_bad_hip_image(self, images_gts_preds, thresholds):
        '''保存误检和漏检的头肩框和错误臀部关键点图像；绿框代表正确预测框，红框代表误检框，蓝框代表漏检框

        Args:
            images_gts_preds: np.array, 指标评估类函数输入统一为字典images_gts_preds，参考EvalFunc说明
            thresholds: np.array, 关键点阈值
        '''
        os.makedirs(os.path.join(self.save_dir_path, 'hs_det_badcase'), exist_ok=True)
        for idx, image_path in enumerate(images_gts_preds.keys()):
            print('badcase: %d/%d %s' % (idx, len(images_gts_preds.keys()), image_path))
            gts = images_gts_preds[image_path]['gts']
            preds = images_gts_preds[image_path]['preds']
            image = cv2.imread(image_path)
            
            # 匹配头肩框
            correct_boxes, incorrect_boxes, missed_boxes = self.analyse_false_miss_box(gts, preds)

            # 头肩框badcase可视化
            if len(incorrect_boxes) != 0 or len(missed_boxes) != 0:
                show_image = self.vis_utils.badcase_det_box_vis(image.copy(), correct_boxes, incorrect_boxes, missed_boxes)
                cv2.imwrite(os.path.join(self.save_dir_path, 'hs_det_badcase', os.path.basename(image_path)), show_image)

            # 匹配上的计算关键点之间的误差
            if len(correct_boxes) > 0:
                preds_box_hip = np.array(correct_boxes)[:, :8]
                gts_box_hip = np.array(correct_boxes)[:, 8:]
                scale = np.sqrt(np.square(gts_box_hip[:,2] - gts_box_hip[:,0]) + np.square(gts_box_hip[:,3] - gts_box_hip[:,1]))
                hip_dist = np.sqrt(np.square(gts_box_hip[:,5] - preds_box_hip[:,6]) + np.square(gts_box_hip[:,6] - preds_box_hip[:,7])) / scale
                
                for index, threshold in enumerate(list(thresholds)):
                    os.makedirs(os.path.join(self.save_dir_path, 'hip_badcase', '%f'%(threshold)), exist_ok=True)
                    os.makedirs(os.path.join(self.save_dir_path, 'hip_badcase', '%f'%(threshold), 'invalid_hip'), exist_ok=True)
                    badcase_indices = np.where(hip_dist > threshold)

                    for bc_idx in badcase_indices[0].tolist():
                        pred_box_hip = preds_box_hip[bc_idx].tolist()
                        gt_box_hip = gts_box_hip[bc_idx].tolist()
                        person_image = self.vis_utils.badcase_det_box_hip_vis(image.copy(), gt_box_hip, pred_box_hip)
                        if pred_box_hip[6] == -1:
                            cv2.imwrite(os.path.join(self.save_dir_path, 'hip_badcase', '%f'%(threshold), 'invalid_hip', os.path.basename(image_path).split('.jpg')[0] + '_%05d.jpg'%(bc_idx)), person_image)
                        else:
                            cv2.imwrite(os.path.join(self.save_dir_path, 'hip_badcase', '%f'%(threshold), os.path.basename(image_path).split('.jpg')[0] + '_%05d.jpg'%(bc_idx)), person_image)

class ReIDBadcaseUtils(BadcaseAnalyseUtils):
    '''ReID模型Badcase工具类
    '''
    def gen_query_topk(self, gallery_features_npy_path, query_features_npy_path, gallery_label_ids_npy_path, query_label_ids_npy_path, 
                                                gallery_images_ids_json_path, query_images_ids_json_path, save_json_path, k=5):
        '''根据距离相似度得到query中每张图像预测的topk类别对应的gallery图像，保存为json文件，图像用绝对路径表示

        Args:
            gallery_features_npy_path: str, gallery特征的npy文件路径
            query_features_npy_path: str, query特征的npy文件路径
            gallery_label_ids_npy_path: str, gallery label_ids的npy文件路径
            query_label_ids_npy_path: str, query label_ids的npy文件路径
            gallery_images_ids_json_path: str, gallery图像路径与id的json文件路径
            query_images_ids_json_path: str, query图像路径与id的json文件路径
            save_json_path: str, 保存query topk图像路径
            k, int, topk值
        '''
        import torch
        gallery_features = torch.from_numpy(np.load(gallery_features_npy_path))
        query_features = torch.from_numpy(np.load(query_features_npy_path))
        gallery_label_ids = torch.from_numpy(np.load(gallery_label_ids_npy_path))
        query_label_ids = torch.from_numpy(np.load(query_label_ids_npy_path))
        gallery_images_ids = read_json(gallery_images_ids_json_path, mode='all')
        query_images_ids = read_json(query_images_ids_json_path, mode='all')

        # 计算距离矩阵
        m, n = query_features.size(0), gallery_features.size(0)
        query_gallery_dist_mat = torch.pow(query_features, 2).sum(dim=1, keepdim=True).expand(m, n) + \
                                                                torch.pow(gallery_features, 2).sum(dim=1, keepdim=True).expand(n, m).t()
        query_gallery_dist_mat.addmm_(1, -2, query_features, gallery_features.t())

        num_q, num_g = query_gallery_dist_mat.size()
        _, indices = torch.sort(query_gallery_dist_mat, dim=1)

        query_gallery_topk_images = []
        for i in range(num_q):
            tmp_query_topk_images = []
            query_image_path = query_images_ids[i][0]
            tmp_query_topk_images.append(query_image_path)
            for j in range(num_g):
                if j < k:
                    gallery_image_path = gallery_images_ids[indices[i][j]][0]
                    tmp_query_topk_images.append(gallery_image_path)
                else:
                    query_gallery_topk_images.append(tmp_query_topk_images)
                    break

        save_json(save_json_path, query_gallery_topk_images)
