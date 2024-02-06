import cv2
import numpy as np

from .FileUtils import read_json
from .Convertion import colorstr
from .BadcaseAnalyseUtils import *
from .Math import Distance


class EvalFunc:
    """评估方法基础类
    指标评估类函数输入格式统一为字典images_gts_preds:
    {
        'image_path' : {
            'gts':...,
            'preds':...
        },
        ...
    }

    Args:
        distance: Distance, 距离与相似度工具
        badcase_utils: BadcaseAnalyseUtils, badcase图像分析工具
    """
    def __init__(self):
        self.distance = Distance()
        self.badcase_utils = BadcaseAnalyseUtils()

    def calcu_topk_acc(self, images_gts_preds, k):
        """计算topk准确率
        {
            'image_path' : {
                'gts':class,
                'preds':[class,...]
            },
            ...
        }

        Args:
            images_gts_preds: dict, 图像-标注-预测值
            k: int, topk的k值

        Returns:
            topk_acc: list, topk准确率
            correct_num: int, topk正确数量
            correct_idx: list, topk正确图像的索引
            all_num: int, 总数量
        """
        correct_num = 0
        topk_acc = 0
        correct_idx = set()

        for idx, image_path in enumerate(images_gts_preds):
            gts = images_gts_preds[image_path]['gts']
            preds = images_gts_preds[image_path]['preds']
            if gts in preds[:k]:
                correct_num += 1
                correct_idx.add(idx)

        topk_acc = round((float(correct_num) / len(images_gts_preds) * 100), 2)
        all_num = len(images_gts_preds)
        
        return topk_acc, correct_num, correct_idx, all_num

    def calcu_topk_soft_acc(self, images_gts_preds, k, m, mode='std'):
        """计算topk soft准确率，认为编辑距离<=m的均为正确预测
        {
            'image_path' : {
                'gts':class,
                'preds':[class,...]
            },
            ...
        }

        Args:
            images_gts_preds: dict, 图像-标注-预测值
            k: int, topk的k值
            m: int, 编辑距离
            mode: str, 'std'代表标准编辑距离
                        'wo_delete'代表距离为1时不包含删除操作的编辑距离

        Returns:
            topk_soft_acc: list, topk soft准确率
            correct_num: int, topk正确数量
            correct_idx: list, topk正确图像的索引
            all_num: int, 总数量
        """
        correct_num = 0
        topk_soft_acc = 0
        correct_idx = set()

        for idx, image_path in enumerate(images_gts_preds):
            gts = images_gts_preds[image_path]['gts']
            preds = images_gts_preds[image_path]['preds']
            for pred in preds[:k]:
                edit_distance = self.distance.calcu_edit_distance(gts, pred)
                if mode == 'std':
                    if edit_distance <= m:
                        # print(gts, pred, edit_distance)
                        correct_num += 1
                        correct_idx.add(idx)
                        break
                elif mode == 'wo_delete':
                    if edit_distance <= m and len(gts)!=len(pred):
                        # print(gts, pred, edit_distance)
                        correct_num += 1
                        correct_idx.add(idx)
                        break

        topk_soft_acc = round((float(correct_num) / len(images_gts_preds) * 100), 2)
        all_num = len(images_gts_preds)
        
        return topk_soft_acc, correct_num, correct_idx, all_num


class ClsEvalFunc(EvalFunc):
    """分类评估方法类

    Args:
        badcase_utils: ClsBadcaseUtils, 分类数据badcase类
    """
    def __init__(self):
        super().__init__()
        self.badcase_utils = ClsBadcaseUtils()

    def eval(self, json_path, k=1, vis_flag=False, save_dir_path=None):
        """计算topk准确率，可视化
        {
            'image_path' : {
                'gts':class,
                'preds':[class,...]
            },
            ...
        }

        Args:
            json_path: str, 结果json文件路径
            vis_flag: bool, 是否可视化
        """
        images_gts_preds = read_json(json_path)

        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_acc(images_gts_preds, k)
        print(f'{colorstr("blue", "bold", f"Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')

        # if vis_flag:
        #     vis_data = {}
        #     for idx, image_path in enumerate(images_gts_preds):
        #         if idx not in correct_idx:
        #             vis_data[image_path] = images_gts_preds[image_path]

        #     self.cls_badcase_utils.vis(vis_data, save_dir_path)


class STREvalFunc(ClsEvalFunc):
    """字符识别评估方法类

    Args:
        badcase_utils: ClsBadcaseUtils, 字符识别数据badcase类
    """
    def __init__(self):
        super().__init__()
        self.badcase_utils = ClsBadcaseUtils()

    def eval(self, json_path, k=1, m=1, vis_flag=False, save_dir_path=None):
        """计算topk准确率，可视化
        {
            'image_path' : {
                'gts':class,
                'preds':[class,...]
            },
            ...
        }

        Args:
            json_path: str, 结果json文件路径
            k: int, topk的k值
            m: int, soft topk编辑距离阈值
            vis_flag: bool, 是否可视化
        """
        images_gts_preds = read_json(json_path)

        images_gts_preds_src, images_gts_preds_occ, images_gts_preds_none_occ, images_gts_preds_image_occ, images_gts_preds_4letter_occ = {}, {}, {}, {}, {}

        # 测试集字符准确率
        for image_path in images_gts_preds.keys():
            images_gts_preds_src[image_path] = {'gts':None, 'preds':None}
            images_gts_preds_src[image_path]['gts'] = images_gts_preds[image_path]['gts'].replace('?', '').replace('？', '')
            images_gts_preds_src[image_path]['preds'] = [pred.split(',')[0].replace('?', '').replace('？', '') for pred in images_gts_preds[image_path]['preds']]

        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_acc(images_gts_preds_src, k)
        print(f'{colorstr("blue", "bold", f"Src Data Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')
        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_soft_acc(images_gts_preds_src, k, m)
        print(f'{colorstr("blue", "bold", f"Src Data Soft Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')

        # 测试集非遮挡图像字符准确率
        for image_path in images_gts_preds.keys():
            if '?' in images_gts_preds[image_path]['gts']:
                continue
            images_gts_preds_none_occ[image_path] = {'gts':None, 'preds':None}
            images_gts_preds_none_occ[image_path]['gts'] = images_gts_preds[image_path]['gts'].replace('?', '').replace('？', '')
            images_gts_preds_none_occ[image_path]['preds'] = [pred.split(',')[0].replace('?', '').replace('？', '') for pred in images_gts_preds[image_path]['preds']]

        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_acc(images_gts_preds_none_occ, k)
        print(f'{colorstr("blue", "bold", f"None Occ Data Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')
        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_soft_acc(images_gts_preds_none_occ, k, m)
        print(f'{colorstr("blue", "bold", f"None Occ Data Soft Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')

        # 测试集遮挡图像字符准确率
        for image_path in images_gts_preds.keys():
            if '?' not in images_gts_preds[image_path]['gts']:
                continue
            images_gts_preds_occ[image_path] = {'gts':None, 'preds':None}
            images_gts_preds_occ[image_path]['gts'] = images_gts_preds[image_path]['gts'].replace('?', '').replace('？', '')
            images_gts_preds_occ[image_path]['preds'] = [pred.split(',')[0].replace('?', '').replace('？', '') for pred in images_gts_preds[image_path]['preds']]

        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_acc(images_gts_preds_occ, k)
        print(f'{colorstr("blue", "bold", f"Occ Data Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')
        topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_soft_acc(images_gts_preds_occ, k, m)
        print(f'{colorstr("blue", "bold", f"Occ Data Soft Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')

        # 测试集遮挡类别准确率
        # for image_path in images_gts_preds.keys():
        #     images_gts_preds_image_occ[image_path] = {'gts':None, 'preds':None}
        #     images_gts_preds_image_occ[image_path]['gts'] = 'occ' if '?' in images_gts_preds[image_path]['gts'] else 'none_occ'
        #     # images_gts_preds_image_occ[image_path]['preds'] = [pred.split(',')[1] for pred in images_gts_preds[image_path]['preds']]
        #     images_gts_preds_image_occ[image_path]['preds'] = ['occ' if 'occ' in images_gts_preds[image_path]['preds'][0].split(',') else 'none_occ']

        # topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_acc(images_gts_preds_image_occ, k)
        # print(f'{colorstr("blue", "bold", f"Image Occ Cls Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')

        # 测试集字符位置遮挡类别准确率
        # for i in range(4):
        #     for image_path in images_gts_preds.keys():
        #         images_gts_preds_4letter_occ[image_path] = {'gts':None, 'preds':None}
        #         images_gts_preds_4letter_occ[image_path]['gts'] = 'occ' if '?' == images_gts_preds[image_path]['gts'][i] else 'none_occ'
        #         images_gts_preds_4letter_occ[image_path]['preds'] = ['occ' if 'occ' == images_gts_preds[image_path]['preds'][0].split(',')[i+1] else 'none_occ']

        #     topk_acc, correct_num, correct_idx, all_num = self.calcu_topk_acc(images_gts_preds_4letter_occ, k)
        #     print(f'{colorstr("blue", "bold", f"Letter{i} Occ Cls Top{k}:")} Correct num: {correct_num}, All num: {all_num}, {colorstr("green", "bold", f"Acc:{topk_acc:.2f}%")}')

        # if vis_flag:
        #     vis_data = {}
        #     for idx, image_path in enumerate(images_gts_preds):
        #         if idx not in correct_idx:
        #             vis_data[image_path] = images_gts_preds[image_path]

        #     self.str_cls_badcase_utils.vis(vis_data, save_dir_path)


class DetEvalFunc(EvalFunc):
    """检测模型评估方法类

    Args:
        badcase_utils: DetBadcaseUtils, 检测模型badcase类
    """
    def __init__(self):
        super().__init__()
        self.badcase_utils = DetBadcaseUtils()

    def calcu_map_coco(self, coco_eval_gt_path, coco_eval_pred_path):
        '''利用cocoapi计算map，注意生成coco_eval_pred_json文件时imageid要与gt文件中对应上
        所以最好gt与pred均用test.txt生成，保持一致性

        Args:
            coco_eval_gt_path: str, coco格式gt json文件路径
            coco_eval_pred_path: str, coco格式pred json文件路径

        Returns:
            map50: float, mAP@0.5值
            map50_95: float, mAP@0.5:0.95值
        '''
        from pycocotools.coco import COCO
        from pycocotools.cocoeval import COCOeval

        cocoGt = COCO(coco_eval_gt_path)  # initialize COCO ground truth api
        cocoDt = cocoGt.loadRes(coco_eval_pred_path)  # initialize COCO pred api

        cocoEval = COCOeval(cocoGt, cocoDt, 'bbox')
        cocoEval.params.imgIds = list(range(len(cocoGt.imgs)))  # image IDs to evaluate
        cocoEval.evaluate()
        cocoEval.accumulate()
        cocoEval.summarize()
        map50_95, map50 = cocoEval.stats[:2]  # update results (mAP@0.5:0.95, mAP@0.5)

        return map50, map50_95

    def calcu_map(self, pr_result_json_path):
        '''根据pr曲线计算map

        Args:
            pr_result_json_path: str, pr曲线json文件路径
        '''
        json_data = read_json(pr_result_json_path)
        precision = []
        recall = []
        for index, line in enumerate(json_data[0][0]['result']):
            recall.append(line['Recall'])
            precision.append(line['Precision'])

        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.asarray(list(reversed(recall)))
        mpre = np.asarray(list(reversed(precision)))
        mrec = np.concatenate(([0.], mrec, [1.]))
        mpre = np.concatenate(([0.], mpre, [0.]))

        # compute the precision 曲线值（也用了插值）
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])

        print('ap50:', ap)


class ReIDEvalFunc(EvalFunc):
    """ReID评估方法类
    """
    def eval_func_gpu(self, distmat, q_pids, g_pids, max_rank=50):
        import torch
        
        num_q, num_g = distmat.size()
        if num_g < max_rank:
            max_rank = num_g
            print("Note: number of gallery samples is quite small, got {}".format(num_g))
        _, indices = torch.sort(distmat, dim=1)
        matches = g_pids[indices] == q_pids.view([num_q, -1]) 

        results = []
        num_rel = []
        for i in range(num_q):
            m = matches[i]
            if m.any():
                num_rel.append(m.sum())
                results.append(m[:max_rank].unsqueeze(0))
        matches = torch.cat(results, dim=0).float()
        num_rel = torch.Tensor(num_rel)

        cmc = matches.cumsum(dim=1)
        cmc[cmc > 1] = 1
        all_cmc = cmc.sum(dim=0) / cmc.size(0)

        pos = torch.Tensor(range(1, max_rank+1))
        temp_cmc = matches.cumsum(dim=1) / pos * matches
        AP = temp_cmc.sum(dim=1) / num_rel
        mAP = AP.sum() / AP.size(0)
        return all_cmc.numpy(), mAP.item()

    def calcu_acc_from_features(self, gallery_features_npy_path, query_features_npy_path, gallery_label_ids_npy_path, query_label_ids_npy_path, ranks=[1, 2, 4, 5,8, 10, 16, 20]):
        '''根据模型提取到的query和gallery特征npy文件，计算topk准确率

        Args:
            gallery_features_npy_path: str, gallery特征的npy文件路径
            query_features_npy_path: str, query特征的npy文件路径
            gallery_label_ids_npy_path: str, gallery label_ids的npy文件路径
            query_label_ids_npy_path: str, query label_ids的npy文件路径
            ranks: list, 需要输出topk的k值列表
        '''
        import torch
        gallery_features = torch.from_numpy(np.load(gallery_features_npy_path))
        query_features = torch.from_numpy(np.load(query_features_npy_path))
        gallery_label_ids = torch.from_numpy(np.load(gallery_label_ids_npy_path))
        query_label_ids = torch.from_numpy(np.load(query_label_ids_npy_path))

        # 计算距离矩阵
        m, n = query_features.size(0), gallery_features.size(0)
        query_gallery_dist_mat = torch.pow(query_features, 2).sum(dim=1, keepdim=True).expand(m, n) + \
                                                                torch.pow(gallery_features, 2).sum(dim=1, keepdim=True).expand(n, m).t()
        query_gallery_dist_mat.addmm_(1, -2, query_features, gallery_features.t())

        cmc, mAP = self.eval_func_gpu(query_gallery_dist_mat, query_label_ids, gallery_label_ids)

        print("Results ----------")
        print("mAP: {:.1%}".format(mAP))
        print("CMC curve")
        for r in ranks:
            print("Rank-{:<3}: {:.1%}".format(r, cmc[r - 1]))
        print("------------------")


class KeypointEvalFunc(EvalFunc):
    """关键点评估方法类
    """
    def calcu_oks(self, dt_kpts, gt_kpts, area):
        '''计算关键点OKS(object keypoint similarity)，启发于目标检测中的IoU指标，目的就是为了计算真值和预测人体关键点的相似度。https://blog.csdn.net/ZXF_1991/article/details/104279387
        TODO::需要重构

        Args:
            dt_kpts: 模型输出的一组关键点检测结果　dt_kpts.shape=[3,14],dt_kpts[0]表示14个横坐标值，dt_kpts[1]表示14个纵坐标值，dt_kpts[3]表示14个可见性，
            gt_kpts: groundtruth的一组关键点标记结果 gt_kpts.shape=[3,14],gt_kpts[0]表示14个横坐标值，gt_kpts[1]表示14个纵坐标值，gt_kpts[3]表示14个可见性，
            area: groundtruth中当前一组关键点所在人检测框的面积

        Returns:
            map50: float, 两组关键点的相似度oks
        '''
        oks = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
        sigmas = np.array([.26, .25, .25, .35, .35, .79, .79, .72, .72, .62,.62, 1.07, 1.07, .87, .87, .89, .89])/10.0
        variances = (sigmas * 2)**2
        g = np.array(gt_kpts)
        xg = g[0::3]
        yg = g[1::3]
        vg = g[2::3]
        assert(np.count_nonzero(vg > 0) > 0)
        d = np.array(dt_kpts)
        xd = d[0::3]
        yd = d[1::3]
        dx = xd - xg
        dy = yd - yg
        e = (dx**2 + dy**2) /variances/ (area+np.spacing(1)) / 2 #加入np.spacing()防止面积为零
        e=e[vg > 0]

        return np.sum(np.exp(-e)) / e.shape[0]

    def compute_pck_pckh(dt_kpts,gt_kpts,refer_kpts):
        """计算关键点PCK(Percentage of Correct Keypoints)，正确估计出的关键点比例，https://blog.csdn.net/ZXF_1991/article/details/104279387
        TODO::需要重构
        
        Args:
            dt_kpts:算法检测输出的估计结果,shape=[n,h,w]=[行人数，２，关键点个数]
            gt_kpts: groundtruth人工标记结果,shape=[n,h,w]
            refer_kpts: 尺度因子，用于预测点与groundtruth的欧式距离的scale。
                        pck指标：躯干直径，左肩点-右臀点的欧式距离；
                        pckh指标：头部长度，头部rect的对角线欧式距离；
        
        Returns:
            pck: float, pck指标
        """
        dt=np.array(dt_kpts)
        gt=np.array(gt_kpts)
        assert(len(refer_kpts)==2)
        assert(dt.shape[0]==gt.shape[0])
        ranges=np.arange(0.0,0.1,0.01)
        kpts_num=gt.shape[2]
        ped_num=gt.shape[0]
        #compute dist
        scale=np.sqrt(np.sum(np.square(gt[:,:,refer_kpts[0]]-gt[:,:,refer_kpts[1]]),1))
        dist=np.sqrt(np.sum(np.square(dt-gt),1))/np.tile(scale,(gt.shape[2],1)).T
        #compute pck
        pck = np.zeros([ranges.shape[0], gt.shape[2]+1])
        for idh,trh in enumerate(list(ranges)):
            for kpt_idx in range(kpts_num):
                pck[idh,kpt_idx] = 100*np.mean(dist[:,kpt_idx] <= trh)
            # compute average pck
            pck[idh,-1] = 100*np.mean(dist <= trh)
        
        return pck

    def compute_acc(self, gt_keypoints, pred_keypoints, refer_kpts, images_path):
        """计算关键点准确率，参考PCK指标修改的；需要保证在目标数维度，标注与预测一一对应
        
        Args:
            gt_keypoints: np.array, 标注关键点, shape=[n,2,k]=[目标数, 2, 关键点数量]
            pred_keypoints: np.array, 预测关键点, shape=[n,2,k]=[目标数, 2, 关键点数量]
            refer_kpts: 尺度因子，用于缩放标注与预测关键点的欧式距离；女包指标：对角线长度，gt左上角-右下角的欧式距离
        
        Returns:
            acc: float, 准确率
        """
        thresholds = np.arange(0.0, 1.0, 0.1)
        kpts_num = gt_keypoints.shape[2]
        badcases_index = []
        
        #compute dist
        scale = np.sqrt(np.sum(np.square(gt_keypoints[:,:,refer_kpts[0]] - gt_keypoints[:,:,refer_kpts[1]]),1))
        dist = np.sqrt(np.sum(np.square(pred_keypoints - gt_keypoints),1)) / np.tile(scale, (kpts_num, 1)).T
        object_dist = np.sum(dist, 1)
        
        # compute acc
        acc = np.zeros([thresholds.shape[0], 1])
        for index, threshold in enumerate(list(thresholds)):
            down_threshold = (object_dist[:] <= threshold)
            acc[index] = 100 * np.mean(down_threshold)

            badcases_index.append(np.where(down_threshold==False))

        badcases = badcases_index[2][0].tolist()
        for index in badcases:
            image_path = images_path[index]
            image = cv2.imread('keypoint/' + image_path)
            image_gt_keypoints = gt_keypoints[index]
            image_pred_keypoints = pred_keypoints[index]

            # gt
            x1, x2, x3, x4 = image_gt_keypoints[0][0], image_gt_keypoints[0][1], image_gt_keypoints[0][2], image_gt_keypoints[0][3]
            y1, y2, y3, y4 = image_gt_keypoints[1][0], image_gt_keypoints[1][1], image_gt_keypoints[1][2], image_gt_keypoints[1][3]
            points_array = np.array([[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]], dtype = np.int32)
            cv2.polylines(image, [points_array], True, (255,255,255), 2)
            cv2.circle(image, (int(x1),int(y1)), radius = 4, color = (0,0,255), thickness=-1)
            cv2.circle(image, (int(x2),int(y2)), radius = 4, color = (0,255,0), thickness=-1)
            cv2.circle(image, (int(x3),int(y3)), radius = 4, color = (255,0,0), thickness=-1)
            cv2.circle(image, (int(x4),int(y4)), radius = 4, color = (0,255,255), thickness=-1)

            # pred
            x1, x2, x3, x4 = image_pred_keypoints[0][0], image_pred_keypoints[0][1], image_pred_keypoints[0][2], image_pred_keypoints[0][3]
            y1, y2, y3, y4 = image_pred_keypoints[1][0], image_pred_keypoints[1][1], image_pred_keypoints[1][2], image_pred_keypoints[1][3]
            points_array = np.array([[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]], dtype = np.int32)
            cv2.polylines(image, [points_array], True, (255,0,255), 2)
            cv2.circle(image, (int(x1),int(y1)), radius = 4, color = (0,0,255), thickness=-1)
            cv2.circle(image, (int(x2),int(y2)), radius = 4, color = (0,255,0), thickness=-1)
            cv2.circle(image, (int(x3),int(y3)), radius = 4, color = (255,0,0), thickness=-1)
            cv2.circle(image, (int(x4),int(y4)), radius = 4, color = (0,255,255), thickness=-1)

        
        return acc


