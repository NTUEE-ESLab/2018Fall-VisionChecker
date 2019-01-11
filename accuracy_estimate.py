import cv2
import numpy as np
from utils import detector_utils as detector_utils
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

detection_graph, sess = detector_utils.load_inference_graph()

print("Camera Init Start")
#video = cv2.VideoCapture(0)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
print("Camera Init Finish")



def timeToTest(camera, rawCapture):
	print("Start rawCapture.truncate")
	print("Finish rawCapture.truncate")
	print("Start In time Totest")
	camera.capture(rawCapture, format="bgr")
	firstFrame = rawCapture.array
	rawCapture.truncate(0)
	#ok, firstFrame = video.read()
	h, w, ch = firstFrame.shape
	firstFramePosition = [h//2,w//2]
	sideHeight = 200
	sideWidth = 200
	num_hands_detect = 1;
	UpDownRightLeft = np.array([0, 0, 0, 0, 0])
	rawCapture.truncate(0)
	print("First frame Finsih")
    
	

	'''
	while(True):
		ok, firstFrame = video.read()
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

	#bbox = (firstFramePosition[1], firstFramePosition[0], sideWidth, sideHeight)
	#tracker = cv2.TrackerTLD_create()
	#ok = tracker.init(firstFrame, bbox)
	print("GO Inside While loop")
	while(not((UpDownRightLeft>20).any())):
		#ok, originalFrame = video.read()
		originalFrame = rawCapture.array
		cv2.circle(originalFrame,(firstFramePosition[1],firstFramePosition[0]), 20, (255,0,255), -1)
		txtScreen = "None"
		if originalFrame is None:
			break;
		originalFrame = (np.fliplr(originalFrame)).copy()
		#cv2.rectangle(originalFrame, (firstFramePosition[1], firstFramePosition[0]), (firstFramePosition[1]+sideWidth,firstFramePosition[0]+sideHeight), (0, 0, 255), 2)
		originalFrame = cv2.cvtColor(originalFrame, cv2.COLOR_BGR2RGB)
		print("Using Deep Learning")
		boxes, scores = detector_utils.detect_objects(originalFrame, detection_graph, sess)
		currentFramePosition, currentHeight, currentWidth = detector_utils.draw_box_on_image(num_hands_detect, 0.2, scores, boxes, w, h, originalFrame)		
		print("Finish Deep")
		print("Classify Stary")
		if(currentHeight==0 or currentHeight==0):
			txtScreen = "Not Found Hand"
		elif firstFramePosition[0]-currentFramePosition[0]>sideHeight//2:
			txtScreen = "Up"
			UpDownRightLeft[0] = UpDownRightLeft[0]+1
		elif currentFramePosition[0]-firstFramePosition[0]>sideHeight//2:
			txtScreen = "Down"
			UpDownRightLeft[1] = UpDownRightLeft[1]+1
		elif firstFramePosition[1]-currentFramePosition[1]>sideWidth//2:
			txtScreen = "Left"
			UpDownRightLeft[2] = UpDownRightLeft[2]+1
		elif currentFramePosition[1]-firstFramePosition[1]>sideWidth//2:
			txtScreen = "Right"
			UpDownRightLeft[3] = UpDownRightLeft[3]+1
		else:
			txtScreen = "Not Move"
			UpDownRightLeft[4] = UpDownRightLeft[4]+1
		cv2.putText(originalFrame, txtScreen, (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
		cv2.imshow("Security Feed", originalFrame)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		sleep(0.05)

		#print(UpDownRightLeft)
		#print(np.where( UpDownRightLeft > 30 ))
	
	#video.release()
	#cv2.destroyAllWindows()
	direction = np.argmax(UpDownRightLeft)
	print("Finish Function")
	return direction

ans = timeToTest(video)
print(ans)
# ans = timeToTest()
# print(ans)
#print(time.time())
#time.sleep(3)
#print(time.time())





