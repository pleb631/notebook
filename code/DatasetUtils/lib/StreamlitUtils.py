import streamlit as st
import pandas as pd
import numpy as np

from .FileUtils import read_pkl

@st.cache
def read_result_pkl(result_pkl_path):
    pkl_data = read_pkl(result_pkl_path)
    # pkl_data = read_pkl(root + 'data_div_2021-04-14_10-00_2_tracking_id.pkl')
    image_paths = pkl_data['img_url'].values
    image_captions = pkl_data['cam_tracking_id'].values

    return image_paths, image_captions

def view_specify_person(image_paths, image_captions, list_image_captions):
    number = st.sidebar.number_input('number:%d-%d'%(1, len(list_image_captions)), value=1, min_value=0, max_value=len(list_image_captions))
    cam_tracking_id = list_image_captions[number]
    a = []
    for line in list_image_captions:
        if 'CDC' not in line:
            a.append(line)

    st.write(cam_tracking_id)
    image_indexes = np.where(image_captions == cam_tracking_id)
    paths = image_paths[image_indexes]
    captions = image_captions[image_indexes].tolist()
    # /HDD/ /data2/fyz/
    paths = paths.tolist()
    for index in range(len(paths)):
        paths[index] = paths[index].replace('/HDD/', '/data2/fyz/')
    # st.image(paths, caption=image_captions, width=100, use_column_width=False)
    st.image(paths, caption=captions, width=100)

def tracking_seq_vis_streamlit(trackingid_data):
    '''可视化行人框

    Args:
        trackingid_data: list, 按tracking id排序的内容
    '''
    import streamlit as st
    import pandas as pd
    st.set_page_config(layout="wide")

    select_key_frame_rotated_box = SelectKeyFrameRotatedBox()

    # trackingid = st.sidebar.number_input('trackingid:%d-%d'%(1, len(trackingid_data)), value=1, min_value=0, max_value=len(trackingid_data))
    trackingid = st.sidebar.number_input('trackingid:%d-%d'%(1, 18), value=1, min_value=0, max_value=18)
    tracking_seq = trackingid_data[str(trackingid)]
    tracking_quality_seq = []
    image_paths, captions = [], []
    quality_line_x, quality_line_y = [], []

    st.sidebar.write('---')
    bigger_flag = st.sidebar.checkbox('显示大于阈值的图像', value=False)
    quality_threshold = st.sidebar.slider('质量分数阈值', 0.0, 1.0, 1.0)

    for index, data in enumerate(tracking_seq):
        QualityScore = data['QualityScore']
        if bigger_flag:
            if QualityScore >= quality_threshold:
                tracking_quality_seq.append(data)
        else:
            if QualityScore <= quality_threshold:
                tracking_quality_seq.append(data)

    if len(tracking_quality_seq) == 0:
        st.write('不存在满足条件的图像！')
    else:
        st.sidebar.write('---')
        seq_interval = st.sidebar.slider('', 0, max(1, len(tracking_quality_seq)-1), (0, max(1, len(tracking_quality_seq)-1)), format='')
        st.sidebar.write('当前帧范围:', tracking_quality_seq[seq_interval[0]]['FrameNum'], '-', tracking_quality_seq[seq_interval[1]-1]['FrameNum'])
        st.sidebar.write('当前时间范围:', tracking_quality_seq[seq_interval[0]]['Time'].split('_')[1], '-', tracking_quality_seq[seq_interval[1]-1]['Time'].split('_')[1])
        tracking_quality_seq = tracking_quality_seq[seq_interval[0]:seq_interval[1]]

        st.sidebar.write('---')
        show_keyframe_flag = st.sidebar.checkbox('显示关键帧', value=True)
        if show_keyframe_flag:
            keyframe_num = st.sidebar.number_input('关键帧数量:%d-%d'%(1, 10), value=5, min_value=1, max_value=10)
            tracking_quality_keyframe_seq = select_key_frame_rotated_box.select_key_frame(tracking_quality_seq, keyframe_num)
            if len(tracking_quality_keyframe_seq) < keyframe_num:
                st.write('满足条件的图像只有', len(tracking_quality_keyframe_seq), '个，少于关键帧的数量', keyframe_num, '，请减少关键帧数量')
                return
        else:
            tracking_quality_keyframe_seq = tracking_quality_seq

        for index, data in enumerate(tracking_quality_keyframe_seq):
            CamSNID = data['CamSNID']
            FrameNum = data['FrameNum']
            Time = data['Time']
            ImagePath = data['ImagePath']
            Identity = data['Identity']
            HeadShoulderBox = data['HeadShoulderBox']
            QualityScore = data['QualityScore']
            # HipMidKeypoint = data['HipMidKeypoint']
            
            image_paths.append(ImagePath)
            quality_line_x.append(FrameNum)
            quality_line_y.append(QualityScore)
            # captions.append('%s,\nframe:%d,\n%s,\n%s,\n%.4f' % (CamSNID, FrameNum, Time, Identity, QualityScore))
            captions.append('%s,\nframe:%d,\n%.4f' % (CamSNID, FrameNum, QualityScore))

        with st.beta_expander('质量分数曲线', expanded=True):
            quality_line = pd.DataFrame({
                                        'frame': quality_line_x,
                                        'quality score': quality_line_y
                                        })
            st.line_chart(quality_line.rename(columns={'frame':'index'}).set_index('index'))

        with st.beta_expander('查看对应图像', expanded=True):
            st.image(image_paths, caption=captions, width=100, use_column_width=False)
