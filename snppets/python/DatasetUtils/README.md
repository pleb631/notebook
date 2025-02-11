# Repo组成

- lib/: 库目录
  - **DetectBadcaseAnalyseUtils: 各种数据集自动化分析及可视化Badcase工具**。目前支持ReID模型Badcase分析
  - **Convertion: 输出颜色、数据结构、文件格式转换**。目前支持控制台输出颜色转换；Yolo、Voc等格式转换
  - **DetectDataVisualization: 数据可视化**。如显示gt与pred框、置信度与类别并保存为视频
  - **FileUtils: 文件处理相关工具**。目前支持TXT、CSV、XML、JSON、COCO_JSON、NPY、H5常用文件类型的读写，及目录和文件批量移动、重命名、数量统计操作
  - **ImageUtils: 图像处理相关工具**。目前支持图像合法判断、多图拼接、蒙版图像生成、扩边裁剪、resize加黑边、；
  - **VideoUtils**:处理工具，视频属性获取、片段截取、视频拼接等
  - **calibration**：图像校正相关、仿射变换
  - **ImuUtils: IMU相关工具**。目前支持六轴九轴姿态解算
  - **Math: 数学计算相关工具**。目前支持math、numpy、pytorch数学计算
  - **StreamlitUtils: Streamlit可视化工具**。目前支持侧边栏选项、图片显示
  - **TimeUtils: 时间相关工具**。目前支持生成指定格式的日期时间段、利用起始时间与间隔帧数量计算下一时刻的时间等
  - **EvalUtils**。目前支持计算目标检测map，reid和分类topk，关键点检测pckh等
