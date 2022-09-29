from argparse import FileType
import cv2
import os
import shutil
from cvzone.HandTrackingModule import HandDetector
import numpy as np

detector = HandDetector(mode=False, # 靜態圖模式，若爲True，每一幀都會調用檢測方法，導致檢測很慢
                        maxHands=2, # 最多檢測幾隻手
                        detectionCon=0.8, # 最小檢測置信度
                        minTrackCon=0.5)  # 最小跟蹤置信度

def Get_images_from_video( video_name, time_F ):
    video_images = []
    vc = cv2.VideoCapture(0)
    count = 1
    
    rval, video_frame = vc.read()
        
    if not rval:
        print( "Dosen't found the video !" )
        print( "Please checking whether the video is in video folder !" )
        rval = False

    while rval:   #擷取影片至結束
        rval, video_frame = vc.read()
        

        if np.any(video_frame) :

            if ( count % time_F == 0 ): #每隔幾幀進行擷取
                hands = detector.findHands(video_frame, draw=False)
                if len(hands) > 0 :
                    
                    img_hight = video_frame.shape[0]
                    img_width = video_frame.shape[1]

                    x, y, w, h = hands[0]['bbox']
                    
                    x_offset = int(w/5) # x offset
                    y_offset = int(h/5) # y offset

                    x_start, x_end, y_start, y_end = x-x_offset, x+w+x_offset, y-y_offset, y+h+y_offset


                    if ( x_start ) < 0 :
                        x_start = 0
                    if ( y_start ) < 0 :
                        y_start = 0
                    if ( x_end ) > img_width :
                        x_end = img_width
                    if ( y_end ) > img_hight :
                        y_end = img_hight

                    print ( x_start, x_end, y_start, y_end, x_offset, y_offset )
                        
                    # det = [ (x-30), (y-30), (x+w+30), (y+h+30) ]
                    # img = video_frame[det[1]:det[3], det[0]:det[2]]
                    img = video_frame[y_start:y_end, x_start:x_end]
                    # print ( img_width, img_hight )
                    # print ( det[0], det[1], det[2], det[3] )
                    # print ( video_frame[det[1]:det[3], det[0]:det[2]] )
                    # cv2.imshow('img', img)
                    video_images.append(img)
            
        count = count + 1
        if count == 1000: 
            break
    vc.release()
    
    return video_images

def Write_image( video_images, video_name, rebuild = False ):
    print("\n")
    folderPath = "Output_Folder/" + video_name

    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)
        print( "Folder buiding successfully !" )
    else:
        print( "Found " + folderPath + " !" )
    
    if rebuild:
        shutil.rmtree(folderPath)
        os.mkdir(folderPath)

    print( "Writing Images...\n" )

    try:
        for i in range(len(video_images)):
            cv2.imwrite( os.path.join( folderPath, '{}_{}.jpg'.format(video_name, i) ), video_images[i] )

    except Exception as e:
        print( "Writing images Failure !" )
        # print( "Please to check whether the number of cuts( which is your second input) is too small or large !" )
        print(e)
    else:
        print( "Wirting images Successfully ! " )
        print( "There are " + str(len(video_images)) + " images in the folder !\n" )

def main():
    
    video_name = input( "Enter the video name :" )
    time_F = int(input( "Enter a number to cut video :" )) #time_F越小，取樣張數越多

    try:
        if ( time_F <= 0 ):
            raise ValueError("The number must bigger than zero ! ")

    except ValueError:
        print(ValueError)

    else:
        video_path = "video/" + video_name + ".mp4" # 影片名稱
        video_images = Get_images_from_video(video_path, time_F) # 讀取影片並轉成圖片

        if video_images:
            Write_image( video_images, video_name, rebuild=True )

        # for i in range(0, len(video_images)): #顯示出所有擷取之圖片
        #     cv2.imshow('windows', video_images[i])
        #     cv2.waitKey(100)

if __name__=="__main__":
    video_images = Get_images_from_video("t", 5) # 讀取影片並轉成圖片
    if video_images:
        Write_image( video_images, "video_name", rebuild=True )

