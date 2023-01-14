# Repo组成
- lib/: 库目录
    - **DetectBadcaseAnalyseUtils: 各种数据集自动化分析及可视化Badcase工具**。目前支持ReID模型Badcase分析
    - **Convertion: 输出颜色、数据结构、文件格式转换**。目前支持控制台输出颜色转换；List、Dict、Set、Tuple常用数据结构格式转换；Yolo、Voc等格式转换
    - **Graph: 数据结构**。目前支持图-深度优先搜索DFS、广度优先搜索BFS
    - **DetectDataVisualization: 数据可视化**。如显示女包检测gt与pred框、置信度与类别并保存为视频
    - **EvalUtils: 模型评估**。目前支持分类准确率、检测mAP
    - **FileUtils: 文件处理相关工具**。目前支持TXT、CSV、XML、JSON、COCO_JSON、NPY、H5常用文件类型的读写，及目录和文件批量移动、重命名、数量统计操作
    - **FormatDataset: 数据集制作**。目前支持人工合成数据，隔帧存储视频图像，过滤灰图（离散傅里叶变换）、空图及相似图像（感知哈希算法），将标注结果JSON文件转换为训练数据等功能
    - **ImageVideoUtils: 图像视频处理相关工具**。目前支持图像合法判断、多图拼接、蒙版图像生成、扩边裁剪、resize加黑边、融合半透明蒙版；视频属性获取、片段截取、视频拼接等
    - **ImuUtils: IMU相关工具**。目前支持六轴九轴姿态解算
    - **Math: 数学计算相关工具**。目前支持math、numpy、pytorch数学计算
    - **ModelRelease: 模型发版相关工具**。目前支持分类及检测模型，生成线上测试集及JSON、线上校准集及JSON，一致性结果验证
    - **StreamlitUtils: Streamlit可视化工具**。目前支持侧边栏选项、图片显示
    - **TimeUtils: 时间相关工具**。目前支持生成指定格式的日期时间段、利用起始时间与间隔帧数量计算下一时刻的时间等

# Log
- 2023.1.8: 创建DatasetUtils项目
- 2023.1.14: 把暂时用不到或者看不懂的代码移动至PendingFile，加入paddle-segmentation的图像处理代码,加入以后可能会用到的class库