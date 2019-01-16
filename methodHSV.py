import cv2
import numpy as np
from time import sleep
import os
from utils import detector_utils as detector_utils
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from picamera.array import PiRGBArray
from picamera import PiCamera

# camera = PiCamera()
# camera.resolution = (640,480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera)


# detection_graph, sess = detector_utils.load_inference_graph()
#video = cv2.VideoCapture(0)

def FindHandPosition(camera, rawCapture):

	firstFramePosition = [0,0]
	sideHeight = 0
	sideWidth = 0
	num_hands_detect = 1
	while(True):
		#ok, firstFrame = video.read()
		camera.capture(rawCapture, format="bgr")
		firstFrame = rawCapture.array
		rawCapture.truncate(0)
		if not ok:
			print("Did'nt Open Camera!")
			break
		h, w, ch = firstFrame.shape
		firstFrame = (np.fliplr(firstFrame)).copy()
		firstFrameRGB = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2RGB)
		boxes, scores = detector_utils.detect_objects(firstFrameRGB, detection_graph, sess)
		firstFramePosition, sideHeight, sideWidth = detector_utils.draw_box_on_image(num_hands_detect, 0.2, scores, boxes, w, h, firstFrameRGB)
		if(sideHeight==0 or sideWidth==0):
			print("Error: Not Found Hand")
		else:
			break
	'''
	while True:
		ok, frame = video.read()
		frame = (np.fliplr(frame)).copy()
		cv2.rectangle(frame, (firstFramePosition[1], firstFramePosition[0]), (firstFramePosition[1]+sideWidth, firstFramePosition[0]+sideHeight), (255,0,255), 2)
		cv2.imshow('mask',frame)
		k = cv2.waitKey(5) & 0xFF
	'''
	return firstFramePosition, sideHeight, sideWidth 



def timeToTest(camera, rawCapture):
	camera.capture(rawCapture, format="bgr")
	frame = rawCapture.array
	rawCapture.truncate(0)
	#_,frame = video.read()
	frame = (np.fliplr(frame)).copy()
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

	firstFrame = frame.copy()
	firstFrameGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)



	while(not((UpDownRightLeft>20).any())):
		camera.capture(rawCapture, format="bgr")
		frame = rawCapture.array
		rawCapture.truncate(0)
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
		mask = mask[:frame.shape[0]//2, frame.shape[1]//2:w]
		cv2.imshow('mask',mask)
		k = cv2.waitKey(5) & 0xFF
		
		valueArray = np.array([valueUp, valueDown, valueRight, valueLeft])
		dirTemp = np.argmax(valueArray)
		if valueArray[dirTemp] > threshold:
			UpDownRightLeft[dirTemp] +=1
		else:
			frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			frameDelta = cv2.absdiff(firstFrameGray, frameGray)
			thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
			valueArray[0] = np.mean(thresh[handLocationUp[0]:handLocationUp[0]+sideH, handLocationUp[1]:handLocationUp[1]+sideW])
			valueArray[1] = np.mean(frameDelta[handLocationDown[0]:handLocationDown[0]+sideH, handLocationDown[1]:handLocationDown[1]+sideW])
			valueArray[2] = np.mean(thresh[handLocationRight[0]:handLocationRight[0]+sideH, handLocationRight[1]:handLocationRight[1]+sideW])
			valueArray[3] = np.mean(thresh[handLocationLeft[0]:handLocationLeft[0]+sideH, handLocationLeft[1]:handLocationLeft[1]+sideW])
			dirTemp = np.argmax(valueArray)
			firstFrameGray = frameGray
			#cv2.imshow('frameDelta',thresh)
			#k = cv2.waitKey(5) & 0xFF
			if valueArray[dirTemp] > threshold:
				UpDownRightLeft[dirTemp] +=1
			else:
				UpDownRightLeft[4] +=1
		sleep(0.5)
		print(UpDownRightLeft)
	print("I finish it !")
	direction = np.argmax(UpDownRightLeft)
	return direction

def soEasyTest(camera, rawCapture):
	#_,frame = video.read()
	camera.capture(rawCapture, format="bgr")
	frame = rawCapture.array
	rawCapture.truncate(0)
	frame = (np.fliplr(frame)).copy()
	h, w, ch = frame.shape
	sideH = h//2
	sideW = w//2
	threshold = 0
	UpDownRightLeft = np.array([0, 0, 0, 0, 0])
	firstFrame = frame.copy()
	firstFrameGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)

	while(UpDownRightLeft.sum()<7):
		camera.capture(rawCapture, format="bgr")
		frame = rawCapture.array
		rawCapture.truncate(0)
		#_,frame = video.read()
		frame = (np.fliplr(frame)).copy()
		frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frameDelta = cv2.absdiff(firstFrameGray, frameGray)
		thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
		valueArray = np.array([0,0,0,0])
		valueArray[0] = np.mean(thresh[:sideH,:])
		valueArray[1] = np.mean(thresh[sideH:,:])
		valueArray[3] = np.mean(thresh[:,sideW:])
		valueArray[2] = np.mean(thresh[:,:sideW])
		dirTemp = np.argmax(valueArray)
		firstFrameGray = frameGray
		# cv2.imshow('frameDelta',thresh)
		# k = cv2.waitKey(1) & 0xFF
		if valueArray[dirTemp] > threshold:
			UpDownRightLeft[dirTemp] +=1
		else:
			UpDownRightLeft[4] +=1
		print(UpDownRightLeft)
		# sleep(0.005)
	print("I finish it !")
	direction = np.argmax(UpDownRightLeft)
	return direction







#ans = timeToTest(video)
# ans = soEasyTest(camera,rawCapture)
#L,H,W = FindHandPosition(video)
#print(L)
#print(H,W)
# print(ans)
	


