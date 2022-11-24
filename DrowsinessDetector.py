print("[INFO] Importing libraries")
import pygame
import time
import dlib
import numpy as np
from scipy.spatial import distance
import cv2
print("[INFO]Imported Libraries............")


# Developed by: Sreekar
#Mail: sreekar.cango@gmail.com


# This code is built on Eye Aspect Ratio formula by Tereza Soukupova and Jan Cech
# https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf
# Referrences:http://emaraic.com/blog/realtime-sleep-detection
#            :https://github.com/lincolnhard/head-pose-estimation


#################Function to calculate Eye Aspect Ratio##############
def compute_EAR(vec):

	a = distance.euclidean(vec[1], vec[5])
	b = distance.euclidean(vec[2], vec[4])
	c = distance.euclidean(vec[0], vec[3])
	# compute EAR
	ear = (a + b) / (2.0 * c)

	return ear



#######################Loading pre trained model#######################
print("[INFO] Loading pre trained model")
predictor_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
print("[INFO] Loaded...................")
##############initial adjustments and setting flag variables############
drow=0
color=(0,0,0)
height=int(1920/3)
width=int(1080/3)
pygame.init()
pygame.mixer.init()
blink=0
blink_count=0
blink_time=0
flag1=1
status="Not Sleeping"
blink_flag=100
blink_sec=0
alarm_flag=0
alarm_time=0
alarm_start=0
alarm_end=0

pygame.mixer.music.load('alarm.wav')
effect = pygame.mixer.Sound('blink.wav')

i=0
cap=cv2.VideoCapture(0) #Get Video feed from webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
while(True):            #infinite Loop
    i+=1
    ret,frame=cap.read()
    ##############skipping two frames and processing only every third frame#####################
    if(i%3==0):
         print("******************************************************************************")
         print("image",i+1)
         frame=cv2.resize(frame,(height,width))        #resizing to a lower resolution and converting to greyscale for faster processing
         gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         matrix=gray.shape
         st=time.time()                                #time variable to calculate FPS of each frame
         dets = detector(gray, 0)
         vec = np.empty([68, 2], dtype = int)
         black=np.ones((width,height,3),dtype=np.uint8)#declaring a black window to show the overlays

         #####################code to warn the driver if he blinks more than 7 times in 20 seconds#######################################
         if(flag1==1):
                 blink_rate_start=time.time()
         blink_rate_end=time.time()
         blink_rate_time=blink_rate_end-blink_rate_start
         flag1=0
    
         if(blink_flag==blink_count-1):
                 blink_sec+=1
                 print('####################################################################')
         if(blink_sec>=7):
                 cv2.putText(black,'be alert',(15,80),cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)
                 alarm_flag=1
         if(blink_rate_time>20):
                 flag1=1
                 blink_sec=0
         blink_flag=blink_count
         #################################################################################################################################



         print("Number of faces detected: {}".format(len(dets)))
         for k, d in enumerate(dets):
                 status="Not Sleeping"
                 print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                 k, d.left(), d.top(), d.right(), d.bottom()))
                 # Get the landmarks/parts for the face in box d.
                 shape = predictor(gray, d)

                 print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))
                 # Draw the face landmarks on the screen.
                 for b in range(68):

                     vec[b][0] = shape.part(b).x
                     vec[b][1] = shape.part(b).y

                 right_ear=compute_EAR(vec[42:48])#compute eye aspect ratio for right eye
                 left_ear=compute_EAR(vec[36:42])#compute eye aspect ratio for left eye
                 xyz=0

                 ##############Code for Head Pose Estimation################################
                 image_points = np.array([
                            vec[30],     # Nose tip
                            vec[8],      # Chin
                            vec[36],     # Left eye left corner
                            vec[45],     # Right eye right corne
                            vec[48],     # Left Mouth corner
                            vec[54]      # Right mouth corner
                        ], dtype="double")
                 model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                         
                        ])

                 focal_length = matrix[1]
                 center = (matrix[1]/2,matrix[0]/2)
                 camera_matrix = np.array(
                         [[focal_length, 0, center[0]],
                         [0, focal_length, center[1]],
                         [0, 0, 1]], dtype = "double"
                         )
 
                 print ("Camera Matrix :\n {0}".format(camera_matrix))
 
                 dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
                 start1=time.time()
                 (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
                 end1=time.time()
                 print('solvepnp=',end1-start1)
 
                 print ("Rotation Vector:\n {0}".format(rotation_vector))
                 print ("Translation Vector:\n {0}".format(translation_vector))
                 (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
 
                  
                 p1 = ( int(image_points[0][0]), int(image_points[0][1]))
                 p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
 
                 cv2.line(black, p1, p2, (255,0,0), 2)
                 ###############################################################################################################################


                 
                 if (((right_ear+left_ear)/2) <0.25): #if the avarage eye aspect ratio of lef and right eye less than 0.2, the status is sleeping.
                       status="sleeping"
                 if (status=="Not Sleeping"): 
                       if(blink!=0):
                               blink_end=time.time()
                               blink_time=blink_end-blink_start
                               blink_count+=1
                               #pygame.mixer.music.load('blink.mp3')
                               #pygame.mixer.music.play()
                               effect.play()
                       blink=0
                       color=(0,255,0)
                       cv2.putText(black,'drive',(15,150),cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)
                 if(status=='sleeping'):
                         
                         if(blink==0):
                                 blink_start=time.time()
                                 blink=1
                                 alarm_start=time.time()
                               
                         alarm_end=time.time()
                         alarm_time=alarm_end-alarm_start

                         
                         if (alarm_time>2.0):#warns the driver if eyes closed for more than 2 seconds
                                 cv2.putText(black,'wakeup!',(15,150),cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)
                                 alarm_flag=1        
                       
                         else:
                                 cv2.putText(black,'drive',(15,150),cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)

                         color=(255,0,0)

                 print(status)
                 print((right_ear+left_ear)/2)

                 
                 #Overlay the points on the screen
                 pts1=np.array([vec[42],vec[43],vec[44],vec[45],vec[46],vec[47]],np.int32)
                 pts2=np.array([vec[36],vec[37],vec[38],vec[39],vec[40],vec[41]],np.int32)
                 pts3=np.array(vec[1:17],np.int32)
                 pts4=np.array(vec[18:22],np.int32)
                 pts5=np.array(vec[23:27],np.int32)
                 pts6=np.array(vec[28:31],np.int32)
                 pts7=np.array(vec[32:36],np.int32)
                 pts8=np.array(vec[61:68],np.int32)
                 pts9=np.array(vec[49:60],np.int32)
                 pts10=np.array([vec[31],vec[30],vec[35]],np.int32)
                 cv2.polylines(black,[pts1],True,color,1)
                 cv2.polylines(black,[pts2],True,color,1)
                 cv2.polylines(black,[pts3],False,(0,215,255),1)
                 cv2.polylines(black,[pts4],False,(255,0,255),1)
                 cv2.polylines(black,[pts5],False,(255,0,255),1)
                 cv2.polylines(black,[pts6],False,(255,0,255),1)
                 cv2.polylines(black,[pts7],False,(255,0,255),1)
                 cv2.polylines(black,[pts8],True,(0,0,255),1)
                 cv2.polylines(black,[pts9],True,(0,0,255),1)
                 cv2.polylines(black,[pts10],True,(255,0,255),1)
         cv2.putText(black,'blink:'+str(blink_count),(15,25),cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)
         cv2.putText(black,'bt:'+str(blink_time),(15,50),cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)
         #black=cv2.resize(black,(640,480))
         en=time.time()
         print('For_Frame',i,"FPS=",1/(en-st))
         #cv2.imshow('drowsiness',black)
         #cv2.imshow('frame',frame)
         finalFrame= np.hstack((frame,black))
         cv2.imshow("Drowsiness Detector",finalFrame)
         k=cv2.waitKey(1)
         if(alarm_flag==1):
                 pygame.mixer.music.play(-1)
         alarm_flag=0        
         if(k==ord('q')):
            break
         if(k==ord('r')):
             pygame.mixer.music.stop()
         
            

cv2.destroyAllWindows()
cap.release()


