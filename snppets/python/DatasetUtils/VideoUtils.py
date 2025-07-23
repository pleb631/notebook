import cv2
import os
from .FileUtils import *
from .ImageUtils import merge_images


def get_video_features(capture):
    """获取cv2格式视频的属性

    Args:
        capture: cv2.VideoCapture, cv2读取的视频

    Returns:
        fps: int, 帧率
        width: int, 分辨率-宽度
        height: int, 分辨率-高度
        whole_frame_num: int, 总帧数
        current_frame_num: int, 视频文件的当前位置（以毫秒为单位）或帧数（cv2.CAP_PROP_POS_FRAMES）
        duration: int, 时长（单位s）
        fourcc: int, four character code, 视频编码格式，fourcc.org/fourcc.php
                               写视频常用
                               fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                                "MP4V", MPEG-4编码类型，文件名后缀为.mp4
                                "I420",    YUV编码类型，文件名后缀为.avi
                                "PIMI",   MPEG-1编码类型，文件名后缀为.avi
                                "XVID",   MPEG-4编码类型，文件名后缀为.avi
                                "THEO", Ogg Vorbis,  文件名后缀为.ogv
                                "FLV1",    Flash视频，文件名后缀为.flv
    """
    fps = int(round(capture.get(cv2.CAP_PROP_FPS)))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    whole_frame_num = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame_num = int(capture.get(cv2.CAP_PROP_POS_MSEC))
    duration = whole_frame_num / 1000 / fps
    fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))

    return fps, width, height, whole_frame_num, current_frame_num, duration, fourcc



def get_specify_frame(capture, frame_num):
    """获取视频指定帧。如果视频格式有错误，该命令无效，只能从第0帧开始读取，需要重新修改视频格式

    Args:
        capture: cv2.VideoCapture, 视频
        frame_num: int, 指定帧
    """
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = capture.read()

    return frame



def draw_framenum_on_video(src_video_path, save_video_path, fourcc):
    """绘制帧号在视频左上角

    Args:
        src_video_path: str, 原始视频路径
        save_video_path: str, 保存视频路径
        fourcc: str, 视频编码格式
    """
    capture = cv2.VideoCapture(src_video_path)
    assert capture.isOpened()
    fps, width, height, _, _, _, _ = get_video_features(capture)

    os.makedirs(os.path.dirname(save_video_path), exist_ok=True)
    writer = cv2.VideoWriter(
        save_video_path, cv2.VideoWriter_fourcc(*fourcc), fps, (width, height), True
    )

    ret, frame = capture.read()
    frame_count = 0
    while ret:
        print("frame_count: ", frame_count)
        cv2.putText(
            frame,
            str(frame_count),
            (50, 100),
            cv2.FONT_HERSHEY_COMPLEX,
            2,
            (0, 255, 0),
            2,
        )
        writer.write(frame)
        ret, frame = capture.read()
        frame_count += 1

    capture.release()
    writer.release()



def cut_video_clip(src_video_path, start_frame_num, end_frame_num, clip_path, fourcc):
    """截取指定帧段的视频并保存。
    从指定帧开始读取，如果视频格式有错误，该命令无效，只能从第0帧开始读取，需要重新修改视频格式
    cv2.VideoCapture有设置当前帧的功能，cv2.VideoWriter没有。https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga41c5cfa7859ae542b71b1d33bbd4d2b4

    Args:
        src_video_path: str, 原始视频路径
        start_frame_num: int, 开始截取帧号
        end_frame_num: int, 结束截取帧号
        clip_path: str, 视频片段名保存路径
        fourcc: str, 视频编码格式
    """
    capture = cv2.VideoCapture(src_video_path)
    assert capture.isOpened()

    fps, width, height, _, _, _, _ = get_video_features(capture)

    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame_num)
    ret, frame = capture.read()

    os.makedirs(os.path.split(clip_path)[0], exist_ok=True)
    writer = cv2.VideoWriter(
        clip_path, cv2.VideoWriter_fourcc(*fourcc), fps, (width, height), True
    )

    while ret:
        if start_frame_num <= end_frame_num:
            print("frame_count: ", start_frame_num)
            writer.write(frame)
            ret, frame = capture.read()
            start_frame_num += 1
        else:
            break

    capture.release()
    writer.release()
    cv2.destroyAllWindows()


def merge_videos(
    videos_path_list, height, width, rows, black_border, saved_video_path, show_info
):
    """将视频列表按指定行列数进行排布，生成大图视频

    Args:
        videos_path_list: list, 需要进行排布的视频列表
        height: int, 大图内每张图片的高
        width: int, 大图内每张图片的宽
        rows: int, 排布的行数；列数会自动计算
        black_border: int, 大图内每张图片之间的间隔
        saved_video_path: str, 保存视频的路径
        show_info: list, 每张图片要写的描述
    """
    frame_count = 0
    captures_list, rets, frames = [], [], []
    for video_name in videos_path_list:
        capture = cv2.VideoCapture(video_name)
        assert capture.isOpened()
        captures_list.append(capture)

    for captures in captures_list:
        tmp_ret, tmp_frame = captures.read()
        rets.append(tmp_ret)
        frames.append(tmp_frame)

    tmp_merged_image = merge_images(frames, height, width, rows, black_border)
    fps = int(round(captures_list[0].get(cv2.CAP_PROP_FPS)))
    video = cv2.VideoWriter(
        saved_video_path,
        cv2.VideoWriter_fourcc("D", "I", "V", "X"),
        fps,
        (tmp_merged_image.shape[1], tmp_merged_image.shape[0]),
        True,
    )

    while rets[0]:
        print("frame_count", frame_count)
        # if frame_count > 25*10:
        #     break
        if show_info is not None:
            for frame_index in range(len(frames)):
                cv2.putText(
                    frames[frame_index],
                    show_info[frame_index],
                    (10, 50),
                    cv2.FONT_HERSHEY_COMPLEX,
                    3,
                    (0, 255, 0),
                    2,
                )
                cv2.putText(
                    frames[frame_index],
                    str(frame_count),
                    (10, 200),
                    cv2.FONT_HERSHEY_COMPLEX,
                    3,
                    (0, 255, 0),
                    2,
                )

        merged_image = merge_images(frames, height, width, rows, black_border)
        video.write(merged_image)

        for capture_index in range(len(captures_list)):
            tmp_ret, tmp_frame = captures_list[capture_index].read()
            rets[capture_index] = tmp_ret
            frames[capture_index] = tmp_frame

        frame_count += 1

    for captures_ in captures_list:
        captures_.release()

    video.release()



def extract_image_every_interval(videos_path, interval, save_dir_path, fps=30):
    """读取视频，每隔interval秒存储一张图像

    Args:
        videos_path: str, 需要提取图像的视频路径列表
        interval: float, 帧间隔时长
        save_dir_path: str, 保存帧路径
        fps: int, 默认视频帧率
    """
    for video_path in videos_path:
        print(
            "Extracting images from video %s every %f second"
            % (os.path.basename(video_path), interval)
        )
        capture = cv2.VideoCapture(video_path)
        assert capture.isOpened()

        try:
            (
                fps,
                width,
                height,
                whole_frame_num,
                current_frame_num,
                duration,
                fourcc,
            ) = get_video_features(capture)
        except (IOError, OverflowError):
            whole_frame_num = -1
        frame_count = 0
        ret, frame = capture.read()
        os.makedirs(save_dir_path, exist_ok=True)

        while ret:
            print("frame_count:", frame_count, " | ", whole_frame_num)
            if frame_count % int(interval * fps) == 0:
                cv2.imwrite(
                    os.path.join(
                        save_dir_path,
                        "%s_%06d.jpg"
                        % (
                            os.path.basename(video_path).replace(".mp4", ""),
                            frame_count,
                        ),
                    ),
                    frame,
                )
            ret, frame = capture.read()
            frame_count += 1

        capture.release()



class VideoWriter:
    """
    Video writer.

    Args:
        path (str): The path to save a video.
        fps (int): The fps of the saved video.
        frame_size (tuple): The frame size (width, height) of the saved video.
        is_color (bool): Whethe to save the video in color format.
    """

    def __init__(self, path, fps, frame_size, is_color=True):
        self.is_color = is_color

        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.cap_out = cv2.VideoWriter(
            filename=path,
            fourcc=fourcc,
            fps=fps,
            frameSize=frame_size,
            isColor=is_color)

    def write(self, frames):

        frames = frames.astype('uint8')
        self.cap_out.write(frames)

    def release(self):
        self.cap_out.release()
        


class Cache:

    def __init__(self, capacity):
        self._cache = OrderedDict()
        self._capacity = int(capacity)
        if capacity <= 0:
            raise ValueError('capacity must be a positive integer')

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return len(self._cache)

    def put(self, key, val):
        if key in self._cache:
            return
        if len(self._cache) >= self.capacity:
            self._cache.popitem(last=False)
        self._cache[key] = val

    def get(self, key, default=None):
        val = self._cache[key] if key in self._cache else default
        return val
    





class VideoReader:
    """Video class with similar usage to a list object.

    This video wrapper class provides convenient apis to access frames.
    There exists an issue of OpenCV's VideoCapture class that jumping to a
    certain frame may be inaccurate. It is fixed in this class by checking
    the position after jumping each time.
    Cache is used when decoding videos. So if the same frame is visited for
    the second time, there is no need to decode again if it is stored in the
    cache.

    Examples:
        >>> v = VideoReader('sample.mp4')
        >>> len(v)  # get the total frame number with `len()`
        120
        >>> for img in v:  # v is iterable
        >>>     cv2.imshow(img)
        >>> v[5]  # get the 6th frame
    """

    def __init__(self, filename, cache_capacity=10):
        # Check whether the video path is a url
        if not filename.startswith(('https://', 'http://')):
            if not os.path.isfile(filename):
                raise FileNotFoundError('Video file  {} not found: '.format(filename))

        self._vcap = cv2.VideoCapture(filename)
        assert cache_capacity > 0
        self._cache = Cache(cache_capacity)
        self._position = 0
        # get basic info
        self._width = int(self._vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = self._vcap.get(cv2.CAP_PROP_FPS)
        self._frame_cnt = int(self._vcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._fourcc = self._vcap.get(cv2.CAP_PROP_FOURCC)

    @property
    def vcap(self):
        """:obj:`cv2.VideoCapture`: The raw VideoCapture object."""
        return self._vcap

    @property
    def opened(self):
        """bool: Indicate whether the video is opened."""
        return self._vcap.isOpened()

    @property
    def width(self):
        """int: Width of video frames."""
        return self._width

    @property
    def height(self):
        """int: Height of video frames."""
        return self._height

    @property
    def resolution(self):
        """tuple: Video resolution (width, height)."""
        return (self._width, self._height)

    @property
    def fps(self):
        """float: FPS of the video."""
        return self._fps

    @property
    def frame_cnt(self):
        """int: Total frames of the video."""
        return self._frame_cnt

    @property
    def fourcc(self):
        """str: "Four character code" of the video."""
        return self._fourcc

    @property
    def position(self):
        """int: Current cursor position, indicating frame decoded."""
        return self._position

    def _get_real_position(self):
        return int(round(self._vcap.get(cv2.CAP_PROP_POS_FRAMES)))

    def _set_real_position(self, frame_id):
        self._vcap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        pos = self._get_real_position()
        for _ in range(frame_id - pos):
            self._vcap.read()
        self._position = frame_id

    def read(self):
        """Read the next frame.

        If the next frame have been decoded before and in the cache, then
        return it directly, otherwise decode, cache and return it.

        Returns:
            ndarray or None: Return the frame if successful, otherwise None.
        """
        # pos = self._position
        if self._cache:
            img = self._cache.get(self._position)
            if img is not None:
                ret = True
            else:
                if self._position != self._get_real_position():
                    self._set_real_position(self._position)
                ret, img = self._vcap.read()
                if ret:
                    self._cache.put(self._position, img)
        else:
            ret, img = self._vcap.read()
        if ret:
            self._position += 1
        return img

    def get_frame(self, frame_id):
        """Get frame by index.

        Args:
            frame_id (int): Index of the expected frame, 0-based.

        Returns:
            ndarray or None: Return the frame if successful, otherwise None.
        """
        if frame_id < 0 or frame_id >= self._frame_cnt:
            raise IndexError(
                f'"frame_id" must be between 0 and {self._frame_cnt - 1}')
        if frame_id == self._position:
            return self.read()
        if self._cache:
            img = self._cache.get(frame_id)
            if img is not None:
                self._position = frame_id + 1
                return img
        self._set_real_position(frame_id)
        ret, img = self._vcap.read()
        if ret:
            if self._cache:
                self._cache.put(self._position, img)
            self._position += 1
        return img

    def current_frame(self):
        """Get the current frame (frame that is just visited).

        Returns:
            ndarray or None: If the video is fresh, return None, otherwise
            return the frame.
        """
        if self._position == 0:
            return None
        return self._cache.get(self._position - 1)
    def __len__(self):
        return self.frame_cnt

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [
                self.get_frame(i)
                for i in range(*index.indices(self.frame_cnt))
            ]
        # support negative indexing
        if index < 0:
            index += self.frame_cnt
            if index < 0:
                raise IndexError('index out of range')
        return self.get_frame(index)

    def __iter__(self):
        self._set_real_position(0)
        return self

    def __next__(self):
        img = self.read()
        if img is not None:
            return img
        else:
            raise StopIteration

    next = __next__

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._vcap.release()
