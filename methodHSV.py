import cv2
import numpy as np
from time import sleep
import os
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
rawCapture = PiRGBArray(camera)
#video = cv2.VideoCapture(0)


def timeToTest(camera, rawCapture):
	camera.capture(rawCapture, format="bgr")
	frame = rawCapture.array
	#_,frame = video.read()
	h, w, ch = frame.shape
	sideH = h//10
	sideW = h//10
	threshold = 40
	UpDownRightLeft = np.array([0, 0, 0, 0, 0])
	print(frame.shape)
	handLocation = np.array([frame.shape[0]//4, frame.shape[1]*3//4]).astype(int)
	handLocationUp = np.array([handLocation[0]-sideH, handLocation[1] ]).astype(int)
	handLocationDown = np.array([handLocation[0]+sideH, handLocation[1] ]).astype(int)
	handLocationRight = np.array([handLocation[0], handLocation[1]+sideW ]).astype(int)
	handLocationLeft = np.array([handLocation[0], handLocation[1]-sideW ]).astype(int)

	while(not((UpDownRightLeft>20).any())):
		camera.capture(rawCapture, format="bgr")
		frame = rawCapture.array
		#_,frame = video.read()
		frame = (np.fliplr(frame)).copy()

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		lower_blue = np.array([0,40,80])
		upper_blue = np.array([20,255,255])

		mask = cv2.inRange(hsv,lower_blue,upper_blue)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
		mask = cv2.erode(mask, kernel, iterations = 2)
		mask = cv2.dilate(mask, kernel, iterations = 2)
		mask = cv2.GaussianBlur(mask,(3,3),0)

		valueUp = np.mean(mask[handLocationUp[0]:handLocationUp[0]+sideH, handLocationUp[1]:handLocationUp[1]+sideW])
		valueDown = np.mean(mask[handLocationDown[0]:handLocationDown[0]+sideH, handLocationDown[1]:handLocationDown[1]+sideW])
		valueRight = np.mean(mask[handLocationRight[0]:handLocationRight[0]+sideH, handLocationRight[1]:handLocationRight[1]+sideW])
		valueLeft = np.mean(mask[handLocationLeft[0]:handLocationLeft[0]+sideH, handLocationLeft[1]:handLocationLeft[1]+sideW])
		
		cv2.rectangle(mask, (handLocation[1], handLocation[0]), 
									(handLocation[1] + sideW , 
									handLocation[0] + sideH), (255, 255, 255), 2)

		cv2.imshow('res',mask)
		k = cv2.waitKey(5) & 0xFF
		
		valueArray = np.array([valueUp, valueDown, valueRight, valueLeft])
		dirTemp = np.argmax(valueArray)
		if valueArray[dirTemp] > threshold:
			UpDownRightLeft[dirTemp] +=1
		else:
			UpDownRightLeft[4]+=1
		sleep(0.5)
		print(UpDownRightLeft)
	print("I finish it !")
	direction = np.argmax(UpDownRightLeft)
	return direction

#ans = timeToTest(video)
#print(ans)
	


