import json
import math
import ahrs
import copy
import time
import cv2
import requests
import threading
import pyquaternion
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from queue import Queue
from datetime import datetime
from ahrs.common.orientation import q_prod, q_conj, acc2q, am2q, q2R, q_rot


matplotlib.use('agg')


global imu_data, samplePeriod
imu_data = Queue(maxsize=10000)


def update_imu_6axis_madgwick(q, gyr, acc, beta):
    '''Madgwick AHRS算法，利用六轴解算姿态

    Args:
        q: np.array, 上一时刻的朝向四元数
        gry: np.array, 当前时刻陀螺仪的xyz角速度
        acc: np.array, 当前时刻加速度计的xyz加速度
        beta: float, Madgwick算法增益系数

    Returns:
        q: np.array, 更新后的朝向四元数
    '''
    if acc is None or not np.linalg.norm(acc)>0:
        return q
    acc = acc / np.linalg.norm(acc)

    F = np.array([2*(q[1]*q[3] - q[0]*q[2]) - acc[0],
                2*(q[0]*q[1] + q[2]*q[3]) - acc[1],
                2*(0.5 - q[1]*q[1] - q[2]*q[2]) - acc[2]])
    J = np.array([[-2*q[2], 2*q[3], -2*q[0], 2*q[1]],
                [2*q[1], 2*q[0], 2*q[3], 2*q[2]],
                [0, -4*q[1], -4*q[2], 0]])

    step = J.transpose()@F
    step /= np.linalg.norm(step)

    # Compute rate of change of quaternion
    qDot = 0.5*q_prod(q, [0, *gyr]) - beta*step

    # Integrate to yield quaternion
    q += qDot*samplePeriod
    q /= np.linalg.norm(q)

    return q


def update_imu_9axis_madgwick(q, gyr, acc, mag, beta):
    '''Madgwick AHRS算法，利用九轴解算姿态
    
    Args:
        q: np.array, 上一时刻的朝向四元数
        gyr: np.array, 当前时刻陀螺仪的xyz角速度
        acc: np.array, 当前时刻加速度计的xyz加速度
        mag: np.array, 当前时刻磁力计的xyz磁力
        beta: float, Madgwick算法增益系数

    Returns:
        q: np.array, 更新后的朝向四元数
    '''
    # Normalise accelerometer measurement
    if acc is None or not np.linalg.norm(acc)>0:
        return q
    acc = acc/np.linalg.norm(acc)

    # Normalise magnetometer measurement
    if mag is None or not np.linalg.norm(mag)>0:
        return q
    mag = mag/np.linalg.norm(mag)

    # Reference direction of Earth's magnetic feild
    h = q_prod(q, q_prod([0, *mag], q_conj(q)))
    b = [0, np.linalg.norm([h[1], h[2]]), 0, h[3]]

    # Gradient decent algorithm corrective step
    F = np.array([2*(q[1]*q[3] - q[0]*q[2]) - acc[0],
                2*(q[0]*q[1] + q[2]*q[3]) - acc[1],
                2*(0.5 - q[1]*q[1] - q[2]*q[2]) - acc[2],
                2*b[1]*(0.5 - q[2]**2 - q[3]**2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]) - mag[0],
                2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]) - mag[1],
                2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]**2 - q[2]**2) - mag[2]])
    J = np.array([[-2*q[2], 2*q[3], -2*q[0], 2*q[1]],
                [2*q[1], 2*q[0], 2*q[3], 2*q[2]],
                [0, -4*q[1], -4*q[2], 0],
                [-2*b[3]*q[2], 2*b[3]*q[3], -4*b[1]*q[2]-2*b[3]*q[0], -4*b[1]*q[3]+2*b[3]*q[1]],
                [-2*b[1]*q[3]+2*b[3]*q[1], 2*b[1]*q[2]+2*b[3]*q[0], 2*b[1]*q[1]+2*b[3]*q[3], -2*b[1]*q[0]+2*b[3]*q[2]],
                [2*b[1]*q[2], 2*b[1]*q[3]-4*b[3]*q[1], 2*b[1]*q[0]-4*b[3]*q[2], 2*b[1]*q[1]]])

    # normalise step magnitude
    step = J.transpose()@F
    step /= np.linalg.norm(step)

    # Compute rate of change of quaternion
    qDot = 0.5*q_prod(q, [0, *gyr]) - beta*step

    # Integrate to yield quaternion
    q += qDot*samplePeriod
    q /= np.linalg.norm(q)

    return q


def update_imu_6axis_mahony(q, gyr, acc, k_I, k_P, eInt):
    '''Mahony AHRS算法，利用六轴解算姿态

    Args:
        q: np.array, 上一时刻的朝向四元数
        gry: np.array, 当前时刻陀螺仪的xyz角速度
        acc: np.array, 当前时刻加速度计的xyz加速度
        k_I: float, PI补偿器积分项系数
        k_P: float, PI补偿器比例项系数
        eInt: np.array, 积分误差

    Returns:
        q: np.array, 更新后的朝向四元数
        eInt: np.array, 积分误差
    '''
    if gyr is None or not np.linalg.norm(gyr)>0:
        return q, eInt
    if acc is None or not np.linalg.norm(acc)>0:
        return q, eInt
    Omega = np.copy(gyr)
    a_norm = np.linalg.norm(acc)
    if a_norm>0:
        # R = q2R(q)
        # v_a = R.T@np.array([0.0, 0.0, 1.0])     # Expected Earth's gravity
        v_a = np.array([2*(q[1]*q[3] - q[0]*q[2]),
                        2*(q[0]*q[1] + q[2]*q[3]),
                        q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3]])
        # ECF
        omega_mes = np.cross(acc/a_norm, v_a)   # Cost function (eqs. 32c and 48a)
        if k_I > 0:
            eInt = eInt + omega_mes * samplePeriod
        else:
            eInt = np.array([0, 0, 0])
        # b = -k_I*omega_mes                 # Estimated Gyro bias (eq. 48c)
        Omega = Omega + k_I*eInt + k_P*omega_mes  # Gyro correction
    p = np.array([0.0, *Omega])
    qDot = 0.5*q_prod(q, p)                     # Rate of change of quaternion (eqs. 45 and 48b)
    q += qDot*samplePeriod                           # Update orientation
    q /= np.linalg.norm(q)                      # Normalize Quaternion (Versor)    
    
    return q, eInt


def update_imu_9axis_mahony(q, gyr, acc, mag, k_I, k_P, eInt):
    '''Mahony AHRS算法，利用九轴解算姿态

    Args:
        q: np.array, 上一时刻的朝向四元数
        gry: np.array, 当前时刻陀螺仪的xyz角速度
        acc: np.array, 当前时刻加速度计的xyz加速度
        mag: np.array, 当前时刻磁力计的xyz磁力指数
        k_I: float, PI补偿器积分项系数
        k_P: float, PI补偿器比例项系数
        eInt: np.array, 积分误差

    Returns:
        q: np.array, 更新后的朝向四元数
        eInt: np.array, 积分误差
    '''
    # Normalise accelerometer measurement
    if acc is None or not np.linalg.norm(acc)>0:
        return q, eInt
    acc = acc/np.linalg.norm(acc)

    # Normalise magnetometer measurement
    if mag is None or not np.linalg.norm(mag)>0:
        return q, eInt
    mag = mag/np.linalg.norm(mag)

    # Reference direction of Earth's magnetic feild
    h = q_prod(q, q_prod([0, *mag], q_conj(q)))
    b = [0, np.linalg.norm([h[1], h[2]]), 0, h[3]]
    
    # Estimated direction of gravity and magnetic field
    v = [2*(q[1]*q[3] - q[0]*q[2]),
        2*(q[0]*q[1] + q[2]*q[3]),
        q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3]]
    w = [2*b[1]*(0.5 - q[2]*q[2] - q[3]*q[3]) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]),
        2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]),
        2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]*q[1] - q[2]*q[2])]

    # Error is sum of cross product between estimated direction and measured direction of fields
    e = np.cross(acc, v) + np.cross(mag, w)
    if (k_I > 0):
        eInt = eInt + e * samplePeriod
    else:
        eInt = np.array([0, 0, 0])

    # Apply feedback terms
    gyr = gyr + k_P*e + k_I*eInt
    
    # Compute rate of change of quaternion
    qDot = 0.5*q_prod(q, [0, *gyr])

    # Integrate to yield quaternion
    q += qDot*samplePeriod
    q /= np.linalg.norm(q)

    return q, eInt


def get_phyphox_data_9axis():
    '''实时获取手机phyphox的数据，包括加速度计、陀螺仪、磁力计、时间戳
    '''
    his_acc_time = None
    num = 1
    while 1:
        num += 1
        # r = requests.get("http://172.20.10.1/get?accX&acc_time&accY&accZ&gyroX&gyroY&gyroZ&gyro_time&magX&magY&magZ&mag_time")
        r = requests.get("http://192.168.1.108/get?accX&acc_time&accY&accZ&gyroX&gyroY&gyroZ&gyro_time&magX&magY&magZ&mag_time")
        data = json.loads(r.text)
        acc_time = data["buffer"]["acc_time"]["buffer"][-1]
        accX = data["buffer"]["accX"]["buffer"][-1]
        accY = data["buffer"]["accY"]["buffer"][-1]
        accZ = data["buffer"]["accZ"]["buffer"][-1]
        gyr_time = data["buffer"]["gyro_time"]["buffer"][-1]
        gyrX = data["buffer"]["gyroX"]["buffer"][-1]
        gyrY = data["buffer"]["gyroY"]["buffer"][-1]
        gyrZ = data["buffer"]["gyroZ"]["buffer"][-1]
        mag_time = data["buffer"]["mag_time"]["buffer"][-1]
        magX = data["buffer"]["magX"]["buffer"][-1]
        magY = data["buffer"]["magY"]["buffer"][-1]
        magZ = data["buffer"]["magZ"]["buffer"][-1]
        imu_data.put([num, gyrX, gyrY, gyrZ, accX, accY, accZ, magX, magY, magZ, datetime.now()])
        if his_acc_time is None:
            his_acc_time = acc_time
        elif his_acc_time == acc_time:
            break

        his_acc_time = acc_time


def show_attitude(axis_num=6,algrithm='mahony',k_P=2,k_I=0.2,beta=0.1):
    '''实时显示姿态

    Args:
        axis_num: int, 6代表使用6轴数据；9代表使用9轴数据
        k_P: float, PI补偿器比例系数
        k_I: float, PI补偿器积分系数
        algrithm: str, 姿态解算算法，默认为mahony；可选mahony,madgwick
    '''
    his_acc_time = None
    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection='3d')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    xs, ys, zs = np.zeros(2),np.zeros(2),np.zeros(2)
    line, = ax.plot(xs, ys, zs, animated=True)

    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)

    while 1:
        time_begin = time.time()
        k, GYROX, GYROY, GYROZ, ACCLX, ACCLY, ACCLZ, MAGX, MAGY, MAGZ, cur_acc_time= imu_data.get()
        print('processData: ', k, GYROX, GYROY, GYROZ, ACCLX, ACCLY, ACCLZ, MAGX, MAGY, MAGZ, cur_acc_time)
        if his_acc_time is None:
            his_acc_time = cur_acc_time
            q_last = np.array([1.0,0.0,0.0,0.0], dtype=np.float64)
            continue
        elif his_acc_time == cur_acc_time:
            break
        his_acc_time = cur_acc_time

        # 四元数，acc+gyr，计算角速度计的模长，越大则kp越小
        eInt = np.array([0, 0, 0])
        gyr = np.rad2deg(np.array([GYROX,GYROY,GYROZ]))
        # 判断是否静止状态
        if np.linalg.norm(gyr)<10:
            gyr = np.array([0, 0, 0])
        else:
            gyr = gyr*np.pi/180
        # gyr = np.array([GYROX,GYROY,GYROZ])*np.pi/180
        acc = np.array([ACCLX,ACCLY,ACCLZ])
        mag = np.array([MAGX,MAGY,MAGZ])

        if algrithm=='mahony' and axis_num == 6:
            cur_q, eInt=update_imu_6axis_mahony(q_last,gyr,acc, k_I, k_P, eInt)
        elif algrithm=='madgwick' and axis_num == 6:
            cur_q=update_imu_6axis_madgwick(q_last,gyr,acc,beta)
        elif algrithm=='mahony' and axis_num == 9:
            cur_q, eInt=update_imu_9axis_mahony(q_last,gyr,acc, mag, k_I, k_P, eInt)
        elif algrithm=='madgwick' and axis_num == 9:
            cur_q=update_imu_9axis_madgwick(q_last,gyr,acc,mag,beta)
        q_last=copy.deepcopy(cur_q)

        quatPlotMatrix = q2R(np.array(cur_q).reshape((1,4))).transpose(1,2,0)
        ux = quatPlotMatrix[0,0,0]
        vx = quatPlotMatrix[1,0,0]
        wx = quatPlotMatrix[2,0,0]
        uy = quatPlotMatrix[0,1,0]
        vy = quatPlotMatrix[1,1,0]
        wy = quatPlotMatrix[2,1,0]
        uz = quatPlotMatrix[0,2,0]
        vz = quatPlotMatrix[1,2,0]
        wz = quatPlotMatrix[2,2,0]
        # print(ux, vx, wx, uy, vy, wy, uz, vz, wz)

        fig.canvas.restore_region(background)
        line.set_data_3d(np.array([0, ux]), np.array([0, vx]), np.array([0, wx]))
        line.set_color('red')
        ax.draw_artist(line)

        line.set_data_3d(np.array([0, uy]), np.array([0, vy]), np.array([0, wy]))
        line.set_color('green')
        ax.draw_artist(line)

        line.set_data_3d(np.array([0, uz]), np.array([0, vz]), np.array([0, wz]))
        line.set_color('blue')
        ax.draw_artist(line)

        fig.canvas.blit(ax.bbox)
        
        image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3, ))[...,::-1]

        time_end = time.time()
        print('fps: ', 1/(time_end-time_begin))

        cv2.imshow("Image:", image)
        cv2.waitKey(1)


if __name__ == "__main__":
    samplePeriod=1/50

    get_data_9axis = threading.Thread(target=get_phyphox_data_9axis)
    get_data_9axis.start()

    # show_attitude(axis_num=6,algrithm='mahony',k_P=2,k_I=0.2,beta=0.1)
    # show_attitude(axis_num=9,algrithm='mahony',k_P=2,k_I=0.2,beta=0.1)
    # show_attitude(axis_num=6,algrithm='madgwick',k_P=2,k_I=0.2,beta=0.1)
    show_attitude(axis_num=9,algrithm='madgwick',k_P=2,k_I=0.2,beta=0.1)