import cv2
import matplotlib.pyplot as plt
import pandas as pd
import math

def draw_circle(img, nose: tuple, neck: tuple, tail: tuple):
    frame=img

    nose_x, nose_y = nose
    neck_x, neck_y = neck
    tail_x, tail_y = tail

    nose_x, nose_y = int(nose_x), int(nose_y)
    neck_x, neck_y = int(neck_x), int(neck_y)
    tail_x, tail_y = int(tail_x), int(tail_y)

    cv2.circle(img= frame, center=(nose_x, nose_y), radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(img= frame, center=(neck_x, neck_y), radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(img= frame, center=(tail_x, tail_y), radius=5, color=(0, 0, 255), thickness=-1)

def draw_ellipse(img, center, axes, angle):
    image_temp=img
    xc_before, yc_before=center
    xc, yc=int(xc_before),int(yc_before)
    width,height=axes
    width_half=int(width/2)
    height_half=int(height/2)
    rad=angle
    theta=math.degrees(rad)
    cv2.ellipse(img= image_temp, center= (xc,yc), axes= (width_half,height_half), angle=theta, startAngle= 0, endAngle=360, color=(0, 255, 0), thickness=2)

def circle_data(frame_number):
    text_file = r'drive-download-20211024T024937Z-001\mounting_000\mounting_000_det.txt'
    df = pd.read_csv(text_file)
    df_circle = df[['frame','no_x','no_y','ne_x','ne_y','ta_x','ta_y']]
    df_circle_certain_frame = df_circle[df.frame==frame_number]
    df_circle_erase_frame = df_circle_certain_frame[['no_x','no_y','ne_x','ne_y','ta_x','ta_y']]
    
    return df_circle_erase_frame

def ellipse_data(frame_number):
    text_file = r'drive-download-20211024T024937Z-001\mounting_000\mounting_000_det.txt'
    df = pd.read_csv(text_file)
    df_ellipse = df[['frame','xc','yc','width','height','theta']]
    df_ellipse_certain_frame = df_ellipse[df.frame==frame_number]
    df_ellipse_erase_frame = df_ellipse_certain_frame[['xc','yc','width','height','theta']]
    
    return df_ellipse_erase_frame


def main():
    ##텍스트 열기
    text_file = r'drive-download-20211024T024937Z-001\mounting_001\mounting_001_det.txt'
    df = pd.read_csv(text_file)
    
    ##비디오 열기
    mp4_file = 'drive-download-20211024T024937Z-001/mounting_001/mounting_001.mp4'
    cap = cv2.VideoCapture(mp4_file)       #동영상 캡처 객체 생성
    if cap.isOpened():            #잘 열렸는지 확인
        file_path = 'trk_sungmin_1.avi'    #저장할 파일 경로 이름
        fps = cap.get(cv2.CAP_PROP_FPS)               #재생할 파일의 프레임 레이트 얻기
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)     #재생할 파일의 넓이 얻기
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)   #재생할 파일의 높이 얻기
        size = (int(width), int(height))              #프레임 크기
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')      #저장할 비디오 코덱 
        out = cv2.VideoWriter(file_path, fourcc, fps, size)   #파일 stream 생성
        count = 0
        while(True):
            ret, frame = cap.read()  #파일로 부터 이미지 얻기
            if ret:
                # draw_ellipse(img=frame, center=(1101.2773,681.70776), axes=(195.31213,469.94693), angle=0.063335426)
                # draw_ellipse(img=frame, center=(490.8695,715.7377), axes=(203.52441,387.11194), angle=-0.036949597)
                # draw_ellipse(img=frame, center=(333.08087,721.1758), axes=(165.5154,400.31036), angle=-0.032474793)
                # if count == 
                # draw_ellipse(img=frame, center=(), axes=(), angle=  )

                # draw_circle(img=frame, nose=(1123.7909,907.1449), neck=(1127.5334,862.4352), tail=(1139.5017,475.27542))
                # draw_circle(img=frame, nose=(423.91895,884.3331), neck=(516.713,872.82513), tail=(558.31165,549.50824))
                # draw_circle(img=frame, nose=(283.58325,908.7108), neck=(341.88434,869.08136), tail=(354.29572,543.04205))
                
                # draw_circle(img=frame, nose=(), neck=(), tail=())

                # draw point
                temp_df = df[['frame','no_x','no_y','ne_x','ne_y','ta_x','ta_y']]
                temp_df = temp_df[ temp_df['frame'] == count ]
                for i in range(len(temp_df)):
                    draw_circle(img=frame, nose=(temp_df['no_x'].iloc[i,], temp_df['no_y'].iloc[i,]),
                                           neck=(temp_df['ne_x'].iloc[i,], temp_df['ne_y'].iloc[i,]),
                                           tail=(temp_df['ta_x'].iloc[i,], temp_df['ta_y'].iloc[i,]))

                # draw ellipse 
                temp_df = df[['frame','xc','yc','width','height','theta']]
                temp_df = temp_df[ temp_df['frame'] == count ]
                for i in range(len(temp_df)):
                    draw_ellipse(img=frame, center=(temp_df['xc'].iloc[i,], temp_df['yc'].iloc[i,]),
                                            axes=(temp_df['width'].iloc[i,], temp_df['height'].iloc[i,]),
                                            angle=temp_df['theta'].iloc[i,])

                out.write(frame)
                cv2.imshow('cow_ellipse', frame)        # 다음  프레임 이미지 표시
                
                if cv2.waitKey(1) == 27:    # 1ms 동안 키 입력 대기 ---②
                    break                               # 아무 키라도 입력이 있으면 중지
            else:
                print("no frame!")
                break
            count += 1
        print("{} images are extracted in {}.". format(count, mp4_file))
        out.release()          #저장 파일 종료
    else:
        print("can't open video")
    cap.release()              #재생 파일 종료 /객체 자원 반납
    cv2.destroyAllWindows()    #윈도우 종료

# def main():
#     pathIn='./data/'
#     pathOut='video.avi'
#     fps=25.0
#     convert_frames_to_video(pathIn,pathOut,fps)

if __name__ == '__main__':
    # dataframe()
    main()
    # circle_data(1)
    # ellipse_data(1)