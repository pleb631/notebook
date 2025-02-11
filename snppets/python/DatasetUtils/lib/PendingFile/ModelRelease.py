import caffe


def convert_rgb_to_bgr(src_prototxt_file_path, src_caffemodel_file_path, dst_caffemodel_file_path):
    '''模型第一层由rgb转为bgr
    Args:
        src_prototxt_file_path: str, 原始模型prototxt文件路径
        src_caffemodel_file_path: str, 原始模型caffemodel文件路径
        dst_caffemodel_file_path: str, 转换后模型caffemodel文件路径
    '''
    
    net = caffe.Net(src_prototxt_file_path, src_caffemodel_file_path, caffe.TEST)
    name = 'ConvNd_1'
    weight = net.params[name][0].data
    weight = weight[:,::-1]
    net.params[name][0].data[...] = weight
    net.save(dst_caffemodel_file_path)