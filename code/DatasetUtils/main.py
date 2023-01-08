# -*- coding: UTF-8 -*-
import os
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

# root_dir = os.getcwd()
# add_path(os.path.join(root_dir))

from lib.Convertion import *
from lib.BadcaseAnalyseUtils import *
from lib.DataStructure.Graph import *
from lib.DataVisualization import *
from lib.EvalUtils import *
from lib.FileUtils import *
from lib.FormatDataset import *
from lib.ImageVideoUtils import *
from lib.Math import *
from lib.ModelRelease import *
# from lib.StreamlitUtils import *
from lib.TimeUtils import *

os.environ['CUDA_VISIBLE_DEVICES'] = "4,5"

if __name__ == "__main__":
    # root = '/Users/fuyuanzi/Personal/Data/Physical/JerseyPlateDet/train_data/20220415/'
    root =  '/yuanzifu_data/dataset/physical/jersey_plate/train_data/'
    save_dir_path = '/yuanzifu_data/dataset/'
    CLASSES = ['box1', ]


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Algorithm-Graph
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # vertices_num = 10
    # graph = AdjacencySet(vertices_num, directed_flag=False)
    # # graph = AdjacencyMatrix(vertices_num, directed_flag=False)
    # graph.add_edge(0,3)
    # graph.add_edge(0,6)
    # graph.add_edge(1,4)
    # graph.add_edge(2,7)
    # graph.add_edge(3,5)
    # graph.add_edge(7,9)

    # graph.display()

    # connected_domain = graph.get_connected_domain('bfs')
    # print(connected_domain)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Convertion
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    控制台输出颜色转换
    '''
    # print(colorstr('blue', 'bold', 'underline', 'hello world'))

    '''
    List、Dict、Set、Tuple常用数据结构格式转换
    '''
    # get_index_of_value_from_list(list_a, 1)
    # xyxy = xyxy2xywh_min(xyxy)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Database
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    DataVisualization
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    数据可视化基础类
    '''
    # basic_data_vis = BasicDataVis()
    # distance = Distance()
    # person_wh = [108, 309]
    # plate_wh = [48, 34]
    # boxes_lt_person = [[625,175]]
    # boxes_lt_plate = [
    #                 [131,107], [305,107], [519,107], [653,107], [786,107], 
    #                 [519,222], [653,222], [786,222], 
    #                 [519,300], [653,300], [786,300], 
    #                 [519,381], [653,381], [786,381], 
    #                 [519,515], [653,515], [786,515], 
    # ]
    # boxes_person, boxes_plate = [], []
    # for line in boxes_lt_person:
    #     # boxes_person.append(xywh_min2xyxy(line+person_wh))
    #     boxes_person.append([line[0], line[1]+int(person_wh[1]/10), line[0]+person_wh[0], line[1]+int(person_wh[1]/2)])
    # for line in boxes_lt_plate:
    #     boxes_plate.append(xywh_min2xyxy(line+plate_wh))
    # iou_list = distance.calcu_boxes_ab_iou(boxes_person, boxes_plate, iou_mode='iou', mode='list')
    # vis_img = basic_data_vis.draw_boxes_ab_with_text(boxes_person, boxes_plate, iou_list)
    # cv2.imwrite('./vis_img.jpg', vis_img)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    EvalUtils(EvalUtils->BadcaseAnalyseUtils->DataVisualization)
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    分类指标评估
    '''
    # cls_eval_func = ClsEvalFunc()
    # cls_eval_func.eval(
    #                 '/yuanzifu_data/projects/physical/jersey_number/deep-text-recognition-benchmark/results_json/20220317/result_src.json',
    #                 1,
    #                 # True,
    #                 # '/yuanzifu_data/projects/physical/jersey_number/deep-text-recognition-benchmark/badcase_src_model_release/'
    #                 )

    '''
    字符识别指标评估
    '''
    # str_eval_func = STREvalFunc()
    # str_eval_func.eval(
    #                 '/yuanzifu_data/projects/physical/jersey_number/deep-text-recognition-benchmark/results_json/20220406/result_src_release_focal_a1_g2.json',
    #                 1,
    #                 1,
    #                 # True,
    #                 # '/yuanzifu_data/projects/physical/jersey_number/deep-text-recognition-benchmark/badcase_src_model_release/'
    #                 )

    '''
    检测指标评估
    '''
    # det_eval_func = DetEvalFunc()
    # # det_eval_func.calcu_map_coco(
    # #     '/yuanzifu_data/dataset/physical/jersey_plate/train_data/instances_testset_YQ_81_miss_gt.json',
    # #     '/yuanzifu_data/dataset/physical/jersey_plate/train_data/testset_YQ_81_miss_pred_src_20220406.json'
    # #     )
    # det_eval_func.badcase_utils.save_false_miss_det_image(
    #     '/yuanzifu_data/dataset/physical/jersey_plate/train_data/testset_YQ_81_miss_pred_src_path_keys_20220406.json',
    #     '/yuanzifu_data/dataset/physical/jersey_plate/train_data/YQ_81_miss_test/badcase_20220406/',
    #     False
    #     )

    '''
    ReID指标评估
    '''
    # reid_eval_func = ReIDEvalFunc()
    # reid_eval_func.calcu_acc_from_features(
    #                 root + 'gallery_features_421.npy', 
    #                 root + 'query_features_5070.npy',
    #                 root + 'gallery_label_ids_421.npy', 
    #                 root + 'query_label_ids_5070.npy',
    #                 )
    # # reid_eval_func.badcase_utils.gen_query_topk(
    # #     root + 'gallery_features.npy', root + 'query_features.npy',
    # #     root + 'gallery_label_ids.npy', root + 'query_label_ids.npy',
    # #     root + 'gallery.json', root + 'query.json', root + 'query_gallery_images.json'
    # #     )

    '''
    女包关键点指标评估
    '''
    # gucci_bag_keypoint_eval_func = GucciBagKeypointEvalFunc()
    # gucci_bag_keypoint_eval_func.compute_acc_using_gt_txt_pred_json(
    #     root + 'test_shelf.txt', 
    #     root + 'test_image_shape.json',
    #     '/yuanzifu_data/projects/gucci/bag_keypoint/PIPNet/images/test_pred_keypoint.json'
    #     )
    # # gucci_bag_keypoint_eval_func.badcase_utils.draw_bag_keypoint_using_txt(root + 'keypoints_gallery_583ids.txt')


    '''
    头肩检测+臀部关键点指标评估
    '''
    # hs_det_eval_func = DetEvalFunc(root)
    # hs_det_eval_func.calcu_map_coco(
    #         '/yuanzifu_data/dataset/gucci/headshoulder/with_hip_mid/train_data/instances_test_labeled_gt.json', 
    #         '/yuanzifu_data/dataset/gucci/headshoulder/with_hip_mid/train_data/instances_test_pred_ezi_only_box.json'
    #         )
    # gucci_hip_keypoint_eval_func = GucciHipKeypointEvalFunc(root, os.path.join(root, 'badcase'))
    # gucci_hip_keypoint_eval_func.compute_acc_using_gt_xml_pred_json(
    #             os.path.join(root, 'instances_test_pred_ezi_box_with_kpt.json'),
    #             os.path.join(root, 'test_labeled.txt'),
    #             0.3,
    #             np.arange(0.0, 0.5, 0.05),
    #             False
    #             )


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    FileUtils
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # download_url(file_url, save_file_path)

    # from rich.progress import track
    # files_paths = glob.glob('/Users/fuyuanzi/Personal/Data/Physical/JerseyNum/STR/marathon_20220421/images/*')
    # for file_path in track(files_paths, description="Find Empty Files..."):
    #     if is_file_empty(file_path):
    #         print('file is empty', file_path)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    FormatDataset
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    基础数据集
    '''
    # basic_dataset = BasicDataset()
    # videos_path = glob.glob(os.path.join(root, 'videos', '*mp4'))
    # basic_dataset.extract_image_every_interval(
    #     videos_path,
    #     5,
    #     os.path.join(root, 'images'),
    #     25
    #     )
    # basic_dataset.filter_similar_image(
    #     '/Users/fuyuanzi/Personal/Data/Physical/JerseyPlateDet/train_data/20220415/images',
    #     '/Users/fuyuanzi/Personal/Data/Physical/JerseyPlateDet/train_data/20220415/filter',
    #     1
    #     )
    # basic_dataset.filter_incomplete_image('/yuanzifu_data/dataset/gucci/bag_detection/train_data/train_with_new_shelf_20210318/')
    # basic_dataset.filter_gray_error_image('/yuanzifu_data/dataset/gucci/bag_detection/train_data/train_with_new_shelf_20210318/')


    '''
    分类数据集
    '''
    # cls_dataset = ClsDataset(root)
    # cls_dataset.convert_json_2_traindata(
    #                     os.path.join(root, 'src_data/comp_20220117/comp_1_20220124_081607.json'),
    #                     os.path.join(root, 'train_data/comp_20220117/'),
    #                     0.1
    #                     )

    '''
    检测数据集
    '''
    # subdirs = ['YQ_81_miss_test', ]
    # det_dataset = DetDataset()
    # # det_dataset.filter_very_small_boxes_in_xml(subdirs, 20)
    # for subdir in subdirs:
    #     # det_dataset.label_json_2_traindata(
    #     #                 os.path.join(root, subdir),
    #     #                 os.path.join(root, subdir, 'label_20220412_021153.json'),
    #     #                 'poly',
    #     #                 )
    #     # det_dataset.yolo_voc_convert.voc2yolo(
    #     #     os.path.join(root, subdir),
    #     #     CLASSES, 'std'
    #     #     )
    #     # det_dataset.yolo_voc_convert.yolo2voc(
    #     #     os.path.join(root, subdir),
    #     #     CLASSES, 1920, 1080
    #     #     )
    #     det_dataset.voc_coco_convert.voc2coco(
    #         CLASSES,
    #         os.path.join(root, 'testset_YQ_81_miss.txt'),
    #         os.path.join(root, 'instances_testset_YQ_81_miss_gt.json'),
    #         )
    #     # det_dataset.traindata2prelabel_json(
    #     #     os.path.join(root, subdir),
    #     #     os.path.join(root, '20220415_prelabel.json')
    #     #     )
        
    #     # det_dataset.vis.show_voc_xml(os.path.join(root, subdir), 0.1, mode='write')
    #     # det_dataset.vis.show_yolo_txt(os.path.join(root, subdir), 0.1, CLASSES, mode='write')
    #     # det_dataset.vis.show_prelabel(
    #     #     os.path.join(root, subdir, '20220415_prelabel.json'),
    #     #     os.path.join(root, subdir, 'JPEGImages'),
    #     #     os.path.join(root, subdir, 'show_prelabel'),
    #     #     0.1, mode='write'
    #     #     )


    '''
    女包检测数据集
    '''
    # subdirs = ['CD_side_1536', 'train_CDC_20210914']
    # gucci_bag_det_dataset = GucciBagDetDataset(root, CLASSES)
    # gucci_bag_det_dataset.gen_perspective_image_of_shelf(
    #                         os.path.join(root, 'Images'), 
    #                         os.path.join(root, 'PerspectiveImages'), 
    #                         1920, 1080)
    # shelf_cols = gucci_bag_det_dataset.analyse_perspective_shelf_cols_from_json(
    #                         os.path.join(root, 'det_result.json'), 
    #                         1920, 1080, False)
    # gucci_bag_det_dataset.stick_specified_box_images_on_src_dataset(
    #                         '/yuanzifu_data/dataset/gucci/bag_detection/train_data/train.txt',
    #                         '/yuanzifu_data/dataset/gucci/bag_detection/badcase/model_0006_badcase/selected_false_box.txt',
    #                         [0, 0, 1920, 1080],
    #                         0.1, 
    #                         '/yuanzifu_data/dataset/gucci/bag_detection/train_data/train_artificial_20210903/')

    """
    检测+关键点数据集
    """
    # subdirs = ['train_CDC_20210914', ]
    # for subdir in subdirs:
    #     det_keypoint_dataset = DetKeypointDataset(root + subdir)
    #     det_keypoint_dataset.crop_image_using_headshoulder_xml_for_keypoint_label(
    #         'src_images', 
    #         'src_xmls', 
    #         'crop_images', 
    #         'crop_xmls'
    #         )
    #     det_keypoint_dataset.convert_json_2_xml(
    #         os.path.join(root, subdir, 'crop_images_20210914_20211023_185239.json'),
    #         os.path.join(root, subdir, 'src_images'),
    #         os.path.join(root, subdir, 'crop_xmls'),
    #         os.path.join(root, subdir),
    #         )
    #     det_keypoint_dataset.vis.show_voc_xml(mode='write')

    """
    关键点数据集
    """
    # keypoint_dataset = KeypointDataset(root)
    # keypoint_dataset.gen_train_test_using_json(
    #     root,
    #     root + 'shelf0419secoopart1_20210420_20210511_132242.json',
    #     0.1, 
    #     False
    #     )

    '''
    ReID数据集
    '''

    """
    球服号牌关键点数据集
    """
    # jersey_card_keypoint_dataset = JerseyCardKeypointDataset()
    # jersey_card_keypoint_dataset.label_json_2_traindata(
    #     os.path.join(root, 'jersey_plate/train_data/20220406/label_20220412_021153.json'),
    #     os.path.join(root, 'jersey_plate/train_data/20220406/JPEGImages/'),
    #     os.path.join(root, 'jersey_number/STR/train_data/20220406/images/'),
    #     os.path.join(root, 'jersey_number/STR/train_data/20220406/affine_images/')
    #     )


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ImageVideoUtils
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    基础数据处理
    '''
    # cut_video_clip(root + '/fps_align/蛇形跑侧面3-起跑线.mp4',
    #                 75,17425,
    #                 root + '/person_align/蛇形跑侧面3-起跑线.mp4', 'mp4v')

    # images_path = glob.glob(root + '*jpg')
    # images = [cv2.imread(image_path) for image_path in images_path]
    # merged_image = merge_images(images, 64, 100, 3, 0, 'white', None, 'keep_aspect_ratio')
    # cv2.imwrite(root + 'merged.jpg', merged_image)
    
    # videos_path_list = glob.glob(root + '/result/*mp4')
    # merge_videos(videos_path_list, 1080, 1920, 2, 0, root+'/result/merged.mp4', None)
    
    '''
    生成mask图像，并可视化mask图像到场景图上
    '''
    # sites_pts = {
    #     'YQ-81': [[0,1080], [0,687], [449,548], [1636,692], [1687,1080]],
    #     'YQ-82': [[0,1080], [0,582], [917,582], [1815,1080]],
    #     'YQ-84': [[0,1080], [0,754], [1920,754], [1920,1080]],
    #     'YQ-85': [[0,1080], [0,758], [1920,758], [1920,1080]],
    # }
    # for site in sites_pts:
    #     mask_image = gen_mask_image(sites_pts[site], 1920, 1080)
    #     cv2.imwrite('./%s.jpg' % (site), mask_image)

    # src_image = cv2.imread('/yuanzifu_data/projects/DatasetUtils/YQ-81-0001.png')
    # mask_image = cv2.imread('/yuanzifu_data/projects/physical/snake_routing/physical_track/masks/YQ-81.jpg')
    # masked_image = image_with_translucent_mask(src_image, 'img', mask_image, None, 0.5, 0.5, 0)
    # cv2.imwrite('/yuanzifu_data/projects/DatasetUtils/YQ-81-0001_mask.png', masked_image)

    '''
    相机标定
    '''
    # # 输出不采用科学计数法
    # np.set_printoptions(suppress=True)
    # # 内参标定
    # image_paths = glob.glob('/home/ubuntu/HDD/Projects/gucci/bag/camCalication/SHSCam/intern/SHS3/*.jpg')
    # A_matrix, d_vector, error = calibration_internal_params(image_paths, 8, 11, True)
    # print("A_matrix:", A_matrix)
    # print("d_vector:", d_vector)
    # print("total error: ", error)
    # # 外参标定
    # image_path = '/home/ubuntu/HDD/Projects/gucci/bag/camCalication/SHSCam/extern/SHS3/3row_2_3col.jpg'
    # A_matrix = np.array([1635.5135666, 0.0, 968.36206072,
    #                     0.0, 1635.97812831, 511.81358557, 
    #                     0.0, 0.0, 1.0],dtype=np.float32)
    # d_vector = np.array([-0.41809446,  0.25266543, -0.00004686, -0.00021952, -0.10131539],dtype=np.float32)
    # id = 'SHS3'
    # calibration_external_params(image_path, id, A_matrix, d_vector, 8, 11, 90, "./calib_%s.json"%(id), True)
    # # 利用内外参获取距离
    # distance = get_point_distance_using_RT(
    #     '/home/ubuntu/HDD/Projects/gucci/bag/camCalication/SHSCam/extern/SHS3/3row_2_3col.jpg',
    #     'config/calibration/calib_SHS3.json', 1, 8, 8, 11, 90, True)
    # undistort_image = get_undistort_image_using_A(
    #     '/home/ubuntu/HDD/Projects/gucci/bag/camCalication/SHSCam/extern/SHS1/3_4row_2col.jpg',
    #     'config/calibration/calib_SHS1.json')
    # undistort_box = get_undistort_box_using_A([804, 20, 980, 254], 'config/calibration/calib_SHS1.json', 1920, 1080)
    # cv2.rectangle(undistort_image, (int(undistort_box[0]), int(undistort_box[1])), (int(undistort_box[2]),int(undistort_box[3])), (255, 0, 0), 2)

    # cv2.namedWindow('all_image', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("all_image", 1920*2, 1080)
    # cv2.imshow('all_image',undistort_image)
    # cv2.waitKey(0)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Math
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # distance = Distance()
    # print(distance.calcu_iou([1328,841,1585,1076], [1401,1015,1499,1079]))
    # npy_diff, npy_similarity = calcu_diff_npy(
    #     '/yuanzifu_data/projects/physical/jersey_plate_det/yolov5_official/pytorch2caffe/physical/caffe_last_conv_output.npy', 
    #     '/yuanzifu_data/projects/physical/jersey_plate_det/yolov5_official/pytorch2caffe/physical/pytorch_last_conv_output.npy'
    #     )
    # print('npy_similarity:', npy_similarity[0][0])


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ModelRelease
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    ModelRelease
    '''
    # model_release = ModelRelease(root)
    # # model_release.downgrade_pth(
    # #     '/yuanzifu_data/projects/physical/jersey_number/deep-text-recognition-benchmark/saved_models/None-ResNet50-None-CTC-Seed1111_release_r50_basicblock_rgb_conv/best_accuracy.pth', 
    # #     '/yuanzifu_data/projects/physical/jersey_number/deep-text-recognition-benchmark/saved_models/None-ResNet50-None-CTC-Seed1111_release_r50_basicblock_rgb_conv/best_accuracy_torch13.pth'
    # #     )
    # model_release.gen_calibset(
    #     '/yuanzifu_data/dataset/physical/jersey_plate/train_data/calibset.txt',
    #     '',
    #     '/yuanzifu_data/projects/ezm/JerseyPlateDet/calibset/0001/',
    #     (640,384)
    #     )

    '''
    ModelReleaseCls
    '''
    # model_release_cls = ModelReleaseCls(root)
    # model_release_cls.gen_testset(
    #     root + 'testset_w_greater45.txt',
    #     root,
    #     '/yuanzifu_data/projects/ezm/StickDownCls/testset/0001/'
    #     )

    '''
    ModelReleaseSTR
    '''
    # model_release_str = ModelReleaseSTR(root)
    # model_release_str.gen_testset(
    #     '/yuanzifu_data/dataset/physical/jersey_number/STR/train_data/testset.txt',
    #     '/yuanzifu_data/dataset/physical/jersey_number/STR/train_data/',
    #     '/yuanzifu_data/projects/ezm/JerseyNumRec/testset/0002/',
    #     1804001007
    #     )

    '''
    ModelReleaseDet
    '''
    # model_release_det = ModelReleaseDet()
    # model_release_det.gen_testset(
    #     '/yuanzifu_data/dataset/physical/jersey_plate/train_data/testset.txt',
    #     '/yuanzifu_data/projects/ezm/JerseyPlateDet/testset/0001/',
    #     1805001004
    #     )
    # model_release_det.convert_result_json_2_coco_json(
    #     '/yuanzifu_data/projects/ezm/GucciBag/testset/0006/testlist/test.json',
    #     '/yuanzifu_data/projects/ezm/GucciBag/0.0.0.8/results.GucciBag.test_0006_0006.json_trt_60_p4_148_ezi_384',
    #     '/yuanzifu_data/dataset/gucci/bag_detection/train_data/instances_test_pred_official_ezi_conf03_round_bgr_384.json',
    #     0.3
    #     )

    '''
    ModelReleaseDetWithKpt
    '''
    # model_release_det_with_kpt = ModelReleaseDetWithKpt()
    # model_release_det_with_kpt.gen_testset(
    #     '/yuanzifu_data/dataset/gucci/headshoulder/with_hip_mid/train_data/test_labeled.txt', 
    #     '/yuanzifu_data/projects/ezm/GucciHeadShoulderHipDet/testset/0001/',
    #     (551006001, 551006002)
    #     )
    # model_release_det_with_kpt.convert_result_json_2_coco_json(
    #     '/yuanzifu_data/projects/ezm/GucciHeadShoulderHipDet/testset/0001/testlist/test_0001.json',
    #     '/yuanzifu_data/projects/ezm/GucciHeadShoulderHipDet/0.0.1.0/GucciHeadShoulderHipDet_0_0_1_0/test_0001_0001.json_vega_result.json',
    #     '/yuanzifu_data/dataset/gucci/headshoulder/with_hip_mid/train_data/instances_test_pred_ezi_only_box.json',
    #     '/yuanzifu_data/dataset/gucci/headshoulder/with_hip_mid/train_data/instances_test_pred_ezi_box_with_kpt.json',
    #     0.3
    #     )

    '''
    ModelReleaseReID
    '''
    # model_release_cls = ModelReleaseReID(root)
    # model_release_cls.gen_testset(
    #     root + 'query_shelf20210419_with_labor_filter.txt', 
    #     root + 'bounding_box_test_626ids_affine_keypoints.txt', 
    #     '/yuanzifu_data/projects/ezm/GucciBagReID/testset/0002/'
    #     )

    '''
    ModelReleaseKeypoint
    '''
    # model_release_cls = ModelReleaseKeypoint(root)
    # model_release_cls.gen_testset(
    #     '/home/ubuntu/HDD/Projects/ezm/GucciBagKeypoint/testset/test_shelf.txt', 
    #     '/home/ubuntu/HDD/Projects/ezm/GucciBagKeypoint/testset/0001/',
    #     203001001)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    StreamlitUtils
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # image_paths, image_captions = read_result_pkl(root + 'merged_all_out_2021-04-14_10_11_7390.pkl')
    # list_image_captions = list(set(image_captions.tolist()))

    # # for index, cam_tracking_id in enumerate(list_image_captions):
    # view_specify_person(image_paths, image_captions, list_image_captions)


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TimeUtils
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # dates = date_range('20210924', '20211101', step=1, format="%Y%m%d")