import cv2
import numpy as np
import math
import os
from .FileUtils import *
from .Convertion import (
    xyxy2points,
    quadrilateral_points2rectangle_xyxy,
)

"""
相机标定
"""


def get_chessboard_corners(image_path, row, col):
    """寻找图像中棋盘格的角点，并使用亚像素角点检测进行修正

    Args:
        image_path: str, 图像路径
        row: int, 棋盘格角点行数
        col: int, 棋盘格角点列数

    Returns:
        ret: bool, 是否找到棋盘格角点
        image: np.array, 图像
        corners: np.array, 像素级别的棋盘格角点
        corners_subpixel: np.array, 亚像素级别的棋盘格角点
    """
    corners_subpixel = None
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.001)

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (row, col), None)

    if ret == True:
        corners_subpixel = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)

    return ret, image, corners, corners_subpixel


def calibration_internal_params(intern_image_paths_list, row, col, show_flag=False):
    """多张棋盘格图像标定内参

    Args:
        intern_image_paths_list: list, 多张内参图像绝对路径列表
        row: int, 棋盘格角点行数
        col: int, 棋盘格角点列数
        show_flag: bool, 是否绘制棋盘格

    Returns:
        A_matrix: np.array, 内参矩阵
        d_vector: np.array, 畸变系数向量
        mean_error/len(objpoints): np.array, 误差
    """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((col * row, 3), np.float32)
    objp[:, :2] = np.mgrid[0:row, 0:col].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    image_points = []  # 2d points in image plane.

    for intern_image_path in intern_image_paths_list:
        ret, image, _, corners_subpixel = get_chessboard_corners(
            intern_image_path, row, col
        )

        if ret == True:
            objpoints.append(objp)
            image_points.append(corners_subpixel)

            if show_flag:
                # 绘制棋盘格角点，红色线头为起始点
                image = cv2.drawChessboardCorners(
                    image, (row, col), corners_subpixel, ret
                )

                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("image", image.shape[1], image.shape[0])
                cv2.imshow("image", image)
                cv2.waitKey(10)

    if show_flag:
        cv2.destroyAllWindows()

    # A_matrix内参矩阵, d_vector畸变系数; r_vector旋转向量, t_vector平移向量(每张图像有一个rt)
    ret, A_matrix, d_vector, r_vector, t_vector = cv2.calibrateCamera(
        objpoints, image_points, image.shape[::-1][1:], None, None
    )

    mean_error = 0
    for i in range(len(objpoints)):
        # 通过给定的内参数和外参数计算三维点投影到二维图像平面上的坐标
        calcu_image_points, _ = cv2.projectPoints(
            objpoints[i], r_vector[i], t_vector[i], A_matrix, d_vector
        )
        error = cv2.norm(image_points[i], calcu_image_points, cv2.NORM_L2) / len(
            calcu_image_points
        )
        mean_error += error

    return A_matrix, d_vector, mean_error / len(objpoints)


def calibration_external_params(
    extern_image_path, id, A_matrix, d_vector, row, col, side, save_json_path, show_flag
):
    """单张棋盘格图像标定外参。利用几组世界坐标系3D点和对应图像坐标系2D点坐标，以及内参反推出外参

    Args:
        extern_image_path: str, 外参图像绝对路径
        id: str, 相机id号
        A_matrix: np.array, 内参矩阵
        d_vector: np.array, 畸变系数向量
        row: int, 棋盘格角点行数
        col: int, 棋盘格角点列数
        side: int, 棋盘格方格边长，单位mm
        save_json_path: str, 内外参json文件保存路径
        show_flag: bool, 是否绘制棋盘格

    Returns:
        mean_error/len(objpoints): np.array, 误差
    """
    carmera, carmeraMatrix = {}, {}
    carmera["id"] = id
    carmera["calib_extern_image"] = os.path.basename(extern_image_path)

    objp = np.zeros((col * row, 3), np.float32)
    objp[:, :2] = np.mgrid[0:row, 0:col].T.reshape(-1, 2)
    objp = objp * side

    A_matrix = A_matrix.reshape(3, 3)
    d_vector = d_vector.reshape(1, 5)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    image_points = []  # 2d points in image plane.

    ret, image, _, corners_subpixel = get_chessboard_corners(
        extern_image_path, row, col
    )

    if ret == True:
        objpoints.append(objp)
        image_points.append(corners_subpixel)

        if show_flag:
            # 绘制棋盘格角点，红色线头为起始点
            image = cv2.drawChessboardCorners(image, (row, col), corners_subpixel, ret)

            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("image", image.shape[1], image.shape[0])
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # 利用几组世界坐标系3D点和对应图像坐标系2D点坐标，以及内参反推出外参
    ret, rotation, translation = cv2.solvePnP(
        objpoints[0], image_points[0], A_matrix, d_vector
    )

    # 利用罗德里格斯公式将旋转向量转换为旋转矩阵
    R_matrix = cv2.Rodrigues(rotation)[0]
    RT = np.hstack((R_matrix, translation))
    print("RT: ", RT)

    # 重投影计算误差
    calcu_image_points, _ = cv2.projectPoints(
        objpoints[0], rotation, translation, A_matrix, d_vector
    )
    error0 = cv2.norm(image_points[0], calcu_image_points, cv2.NORM_L2) / len(
        calcu_image_points
    )
    print(id, "error: ", error0)

    carmera["kmat"] = A_matrix.reshape(1, 9).tolist()[0]
    carmera["dvec"] = d_vector.reshape(1, 5).tolist()[0]
    carmera["pmat"] = RT.reshape(1, 12).tolist()[0]
    carmeraMatrix["cameras"] = [carmera]

    save_json(save_json_path, carmeraMatrix)


def get_undistort_image_using_A(image_path, calib_json_path, crop_flag=False):
    """利用内参矩阵得到去除图像畸变后的图像

    Args:
        image_path: str, 外参图像路径
        calib_json_path: str, 内外参标定文件路径
        crop_flag: bool, 是否剪裁掉去除畸变产生的外侧黑边区域

    Returns:
        undistort_image: np.array, 去畸变后的图像
    """
    json_data = read_json(calib_json_path, mode="all")
    A_matrix = np.array(json_data["cameras"][0]["kmat"]).reshape(3, 3)
    d_vector = np.array(json_data["cameras"][0]["dvec"]).reshape(1, 5)

    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    new_A_matrix, roi = cv2.getOptimalNewCameraMatrix(
        A_matrix, d_vector, (w, h), 1, (w, h)
    )
    undistort_image = cv2.undistort(image, A_matrix, d_vector, None, new_A_matrix)

    # 裁剪黑边
    if crop_flag:
        x, y, w, h = roi
        undistort_image = undistort_image[y : y + h, x : x + w]

    return undistort_image


def get_undistort_points_using_A(points, calib_json_path, width, height):
    """利用内参矩阵得到去除图像畸变后的点

    Args:
        points: list, 点列表
        width: int, 原始图像宽
        height: int, 原始图像高
        calib_json_path: str, 内外参标定文件路径

    Returns:
        undistort_points: np.array, 去畸变后的点
    """
    json_data = read_json(calib_json_path, mode="all")
    A_matrix = np.array(json_data["cameras"][0]["kmat"]).reshape(3, 3)
    d_vector = np.array(json_data["cameras"][0]["dvec"]).reshape(1, 5)

    new_A_matrix, roi = cv2.getOptimalNewCameraMatrix(
        A_matrix, d_vector, (width, height), 1, (width, height)
    )
    points = points.reshape(-1, 1, 2).astype(np.float32)
    return cv2.undistortPoints(points, A_matrix, d_vector, None, new_A_matrix).reshape(
        -1, 2
    )


def get_undistort_box_using_A(box, calib_json_path, width, height):
    """利用内参矩阵得到去除图像畸变后的矩形框

    Args:
        box: list, 矩形框
        width: int, 原始图像宽
        height: int, 原始图像高
        calib_json_path: str, 内外参标定文件路径

    Returns:
        undistort_box: np.array, 去畸变后的矩形框
    """
    json_data = read_json(calib_json_path, mode="all")
    A_matrix = np.array(json_data["cameras"][0]["kmat"]).reshape(3, 3)
    d_vector = np.array(json_data["cameras"][0]["dvec"]).reshape(1, 5)

    new_A_matrix, roi = cv2.getOptimalNewCameraMatrix(
        A_matrix, d_vector, (width, height), 1, (width, height)
    )
    points = np.array(xyxy2points(box), dtype=np.float32).reshape(-1, 1, 2)
    undistort_points = (
        cv2.undistortPoints(points, A_matrix, d_vector, None, new_A_matrix)
        .reshape(-1, 2)
        .tolist()
    )
    return quadrilateral_points2rectangle_xyxy(undistort_points)


def get_point_distance_using_RT(
    image_path, calib_json_path, point_row, point_col, row, col, side, show_flag=False
):
    """利用外参计算棋盘格某一点距离相机的距离

    Args:
        image_path: str, 外参图像路径
        calib_json_path: str, 内外参标定文件路径
        point_row: int, 该点所在棋盘格内的行数，从1开始算
        point_col: int, 该点所在棋盘格内的列数，从1开始算
        row: int, 棋盘格角点总行数
        col: int, 棋盘格角点总列数
        side: int, 棋盘格每个方格的边长，单位毫米
        show_flag: bool, 是否将距离和点绘制在图像上

    Returns:
        distance: float, 该点距离相机的距离
    """

    def RotateByZ(Cx, Cy, thetaZ):
        rz = thetaZ * math.pi / 180.0
        outX = math.cos(rz) * Cx - math.sin(rz) * Cy
        outY = math.sin(rz) * Cx + math.cos(rz) * Cy
        return outX, outY

    def RotateByY(Cx, Cz, thetaY):
        ry = thetaY * math.pi / 180.0
        outZ = math.cos(ry) * Cz - math.sin(ry) * Cx
        outX = math.sin(ry) * Cz + math.cos(ry) * Cx
        return outX, outZ

    def RotateByX(Cy, Cz, thetaX):
        rx = thetaX * math.pi / 180.0
        outY = math.cos(rx) * Cy - math.sin(rx) * Cz
        outZ = math.sin(rx) * Cy + math.cos(rx) * Cz
        return outY, outZ

    json_data = read_json(calib_json_path, mode="all")
    for cam_data in json_data["cameras"]:
        if cam_data["calib_extern_image"] == os.path.basename(image_path):
            Rt = np.array(cam_data["pmat"]).reshape(3, 4)
            R_matrix = Rt[:, :3]
            t_vector = Rt[:, 3]

            point_world_coordinate = [point_row * side, point_col * side, 0]
            point_vector = point_world_coordinate

            # 验证根据博客http://www.cnblogs.com/singlex/p/pose_estimation_1.html提供方法求解相机位姿
            # 先将相机坐标系与世界坐标系旋转为平行：计算相机坐标系的三轴旋转欧拉角，旋转后可以转出世界坐标系。旋转顺序z,y,x
            thetaZ = math.atan2(R_matrix[1, 0], R_matrix[0, 0]) * 180.0 / math.pi
            thetaY = (
                math.atan2(
                    -1.0 * R_matrix[2, 0],
                    math.sqrt(R_matrix[2, 1] ** 2 + R_matrix[2, 2] ** 2),
                )
                * 180.0
                / math.pi
            )
            thetaX = math.atan2(R_matrix[2, 1], R_matrix[2, 2]) * 180.0 / math.pi
            # 相机坐标系下的值
            x, y, z = t_vector[0], t_vector[1], t_vector[2]

            # 按顺序进行三次旋转
            (x, y) = RotateByZ(x, y, -1.0 * thetaZ)
            (x, z) = RotateByY(x, z, -1.0 * thetaY)
            (y, z) = RotateByX(y, z, -1.0 * thetaX)

            # 相机位置在世界坐标系的坐标
            Cx, Cy, Cz = x * -1, y * -1, z * -1
            t_vector = np.array([Cx, Cy, Cz])

            # 点到相机中心的向量，求模即为距离
            point_2_cam_center_vector = t_vector - point_vector
            distance = np.linalg.norm(point_2_cam_center_vector, ord=2)

            if show_flag:
                ret, image, _, corners_subpixel = get_chessboard_corners(
                    image_path, row, col
                )

                # 绘制棋盘格角点，红色线头为起始点
                image = cv2.drawChessboardCorners(
                    image, (row, col), corners_subpixel, ret
                )
                point_num = (point_col - 1) * row + (point_row - 1)
                position = (
                    int(corners_subpixel[point_num][0][0]),
                    int(corners_subpixel[point_num][0][1]),
                )
                cv2.circle(image, position, 1, (255, 255, 255), 18)
                cv2.putText(
                    image,
                    "%.04fm" % (distance / 1000),
                    position,
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("image", 1920, 1080)
                cv2.imshow("image", image)
                cv2.waitKey(0)

            return distance
