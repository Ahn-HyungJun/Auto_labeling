import sys
import os
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt



script_path = os.path.dirname(__file__)
os.chdir(script_path)

# 4번
def rotate(origin, point, radian):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(radian) * (px - ox) - math.sin(radian) * (py - oy)
    qy = oy + math.sin(radian) * (px - ox) + math.cos(radian) * (py - oy)
    return round(qx), round(qy)

# 1번
def rotate_box_dot(x_cen, y_cen, width, height, theta):

    # 2번 최솟값 연산
    x_min = x_cen - (width / 2)
    y_min = y_cen - (height / 2)

    # 5번 rotated_x1 --x_4 & y_1 -- y_4 연산
    # 3번 rotate함수 호출
    rotated_x1, rotated_y1 = rotate(
        origin=(x_cen, y_cen), point=(x_min, y_min), radian=theta)
    rotated_x2, rotated_y2 = rotate(
        origin=(x_cen, y_cen), point=(x_min, y_min+height), radian=theta)
    rotated_x3, rotated_y3 = rotate(origin=(x_cen, y_cen), point=(
        x_min+width, y_min+height), radian=theta)
    rotated_x4, rotated_y4 = rotate(
        origin=(x_cen, y_cen), point=(x_min+width, y_min), radian=theta)
    # 6번 최종 출력
    return [rotated_x1, rotated_y1, rotated_x2, rotated_y2, rotated_x3, rotated_y3, rotated_x4, rotated_y4]
