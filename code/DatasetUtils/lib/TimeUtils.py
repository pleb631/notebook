import os
import datetime


def get_time(format="S"):
    """
    :param format:
    :return:
    """
    if format in ["S", "s"]:
        # time = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
        time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    elif format in ["P", "p"]:
        # 20200508_143059_379116
        time = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S_%f")
        time = time[:-2]
    else:
        time = (str(datetime.now())[:-10]).replace(" ", "-").replace(":", "-")
    return time


def time_internal():
    """计算时间差"""
    t1 = datetime.datetime.now()
    t2 = datetime.datetime.now()
    print(t2 - t1)
    # 秒
    seconds = (t2 - t1).seconds
    # 毫秒
    millis = (t2 - t1).microseconds / 1000
    # 微秒
    micros = (t2 - t1).microseconds


def date_range(start, end, step=1, format="%Y_%m_%d"):
    """生成指定格式的日期时间段，返回该时间段内所有日期的列表；闭区间

    Args:
        start: str, 时间段开始，如"2020_09_27"
        end: str, 时间段结束，如"2020_11_03"
        step: str, 时间段日期间间隔
        format: str, 格式化日期

    Returns:
        date_range_list: list, 日期时间段列表
    """
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [
        strftime(strptime(start, format) + datetime.timedelta(i), format)
        for i in range(0, days, step)
    ]


def calcu_nexttime_using_frame(start_time, interval_frames, fps):
    """利用起始时间与间隔帧数量计算下一时刻的时间

    Args:
        start_time: str, 起始时间，格式为"2020-05-06_18-42-26"
        interval_frames: str, 下一时刻与起始时间间隔的帧数量
        fps: str, 视频帧率

    Returns:
        next_time: str, 下一时刻的时间，格式为"2020-05-06_18-42-26"
    """
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d_%H-%M-%S")
    interval_seconds = interval_frames / fps

    next_time = start_time + datetime.timedelta(seconds=interval_seconds)
    next_time = next_time.strftime("%Y-%m-%d_%H-%M-%S")

    return next_time


def find_timestamp_jpg(src_images, timestamp, interval):
    """寻找时间戳对应的货架图像，支持寻找特定时间戳前后n张的图像

    Args:
        src_images: list, 需要寻找的图像路径列表
        timestamp: str, 时间戳，格式"YY + MM + DD + hh + mm + ss: 20201207122043"
        interval: int, 该时间戳前后interval张图像
    """
    interval_images = []
    for index, image_path in enumerate(src_images):
        image_name = os.path.basename(image_path)
        gt_timestamp = image_name.split("_")[2][:14]
        if gt_timestamp == timestamp:
            for num in range(interval):
                interval_index = min(
                    max(index - int(interval / 2) + num, 0), len(src_images) - 1
                )
                interval_images.append(src_images[interval_index])
            return interval_images

    return None
