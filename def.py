import cv2
import pandas as pd

video = r'mounting_001.mp4'
text = 'mounting_001_det.txt'
output_name = 'mounting_001.avi'

def overlay(video, text, output_name):


    cap = cv2.VideoCapture(video)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #*'H264를 넣어도 저장이 안됨,
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_name, fourcc, fps, (int(width), int(height)))

    cap = cv2.VideoCapture(video)

    df = pd.read_csv(text, sep=",", header=None)

    df = df.drop([0]).astype('float').astype('int')

    frame = 0

    if cap.isOpened():
        while True:
            ret, img = cap.read()

            if ret:
                df_frame = df.loc[df[0] == frame, 1:].values.tolist()

                for i in df_frame:
                    pi = 3.14

                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    cv2.ellipse(img, (i[0], i[1]), (i[2]//2, i[3]//2), float(i[4] * 360 / pi), 0, 360, (255, 255, 255), 3)

                    out.write(img)
                cv2.imshow(video, img)

                cv2.waitKey(5)

                frame += 1
            else:
                print("안됩니다.")
                break

    else:
        print("없습니다.")

    out.release()
    cap.release()
    cv2.destroyAllWindows()


#함수로 만들어보기.
overlay(video, text, output_name)