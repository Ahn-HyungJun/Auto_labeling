import cv2
import numpy as np
import glob
import os

img_array = []

for filename in sorted(glob.glob(r'.\001\*.jpg'), key=os.path.getctime):
    print(filename)
    img = cv2.imread(filename)
    # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # cv2.imshow('img', img)
    # k = cv2.waitKey(0)
    # if k == 27: #esc
    #     cv2.destroyAllWindows()
    file_path = 'project_11_trk.avi'
    height, width, layers = img.shape
    size = (int(width), int(height))
    fps = 15
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    img_array.append(img)


out = cv2.VideoWriter(file_path, fourcc, fps, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()