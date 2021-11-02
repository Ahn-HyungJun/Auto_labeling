import sys
import os
import re
import cv2
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

script_path = os.path.dirname(__file__)
os.chdir(script_path)


# txt file load
#data = pd.read_csv('파일경로', sep = "\t", engine='python', encoding = "인코딩방식")
data = pd.read_csv('mounting_001\mounting_001_det.txt',
                   sep=",", engine='python', encoding="cp949")

# data 전처리
input_data = data.drop(['no_x', 'no_y', 'ne_x', 'ne_y',
                       'ta_x', 'ta_y', 'theta'], axis=1)
cow_data = data.drop(['xc', 'yc', 'width', 'height', 'theta'], axis=1)

cow_data = np.array(cow_data, dtype=np.int64).tolist()
print('cow',type(cow_data))

frame_data = data['frame']
frame_data = np.array(frame_data, dtype=np.int64).tolist()
theta_data = data['theta']
theta_data = np.array(theta_data, dtype=np.float64).tolist()

input_data['xc'] = input_data['xc'].astype(int)
input_data['yc'] = input_data['yc'].astype(int)
input_data['width'] = (input_data['width']/2).astype(int)
input_data['height'] = (input_data['height']/2).astype(int)
input_data = np.array(input_data, dtype=np.int64).tolist()


degrees_theta = []

for i in theta_data:
    math_degree = math.degrees(i)
    degrees_theta.append(math_degree)


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

frameRate = 58

# ellipse(), circle() 적용 img 파일 저장
count = 0
for (data_frame, x_cen, y_cen, width, height), theta in zip(input_data, degrees_theta):

    count += 1

    images = cv2.imread((r"C:\Users\ond\vs_space\intflow\001\frame_{}.jpg").format(
        data_frame), cv2.IMREAD_UNCHANGED)
  
    #image_temp = cv2.cvtColor(images,cv2.COLOR_BGR2RGB)
    ellipse_img = cv2.ellipse(images, (x_cen, y_cen), (width, height),
                        theta, 0, 360, (0, 256, 0), 2)

    cv2.imwrite(r"C:\Users\ond\vs_space\intflow\001\frame_{}.jpg".format(data_frame), ellipse_img)          
    print(count)


count = 0
for (data_frame, no_x, no_y, ne_x, ne_y, ta_x, ta_y) in cow_data: 
    
    count += 1

    images = cv2.imread((r"C:\Users\ond\vs_space\intflow\001\frame_{}.jpg").format(
        data_frame), cv2.IMREAD_UNCHANGED)                   
    circle_img = cv2.circle(images,(no_x, no_y), radius=5, color=(0, 0, 255), thickness= 1)  
    circle_img = cv2.circle(images,(ne_x, ne_y), radius=5, color=(0, 0, 255), thickness= 1)
    circle_img = cv2.circle(images,(ta_x, ta_y), radius=5, color=(0, 0, 255), thickness= 1)         
    # cv2.imshow('images', circle_img)
    # cv2.waitKey(frameRate)
    # cv2.destroyAllWindows()
    cv2.imwrite(r"C:\Users\ond\vs_space\intflow\001\frame_{}.jpg".format(data_frame), circle_img)
    print(count)
