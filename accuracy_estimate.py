import cv2
import numpy as np
from utils import detector_utils as detector_utils
import os
from time import sleep
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

detection_graph, sess = detector_utils.load_inference_graph()

video = cv2.VideoCapture(0)







def timeToTest(video):
	firstFramePosition = [0,0]
	sideHeight = 0
	sideWidth = 0
	num_hands_detect = 1;
	UpDownRightLeft = np.array([0, 0, 0, 0, 0])



	while(True):
		ok, firstFrame = video.read()
		if not ok:
			print("Didnt Open Camera!")
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

	#bbox = (firstFramePosition[1], firstFramePosition[0], sideWidth, sideHeight)
	#tracker = cv2.TrackerTLD_create()
	#ok = tracker.init(firstFrame, bbox)

	while(not((UpDownRightLeft>30).any())):
		ok, originalFrame = video.read()
		txtScreen = "None"
		if originalFrame is None:
			break;
		originalFrame = (np.fliplr(originalFrame)).copy()
		cv2.rectangle(originalFrame, (firstFramePosition[1], firstFramePosition[0]), (firstFramePosition[1]+sideWidth,firstFramePosition[0]+sideHeight), (0, 0, 255), 2)
		originalFrame = cv2.cvtColor(originalFrame, cv2.COLOR_BGR2RGB)
		boxes, scores = detector_utils.detect_objects(originalFrame, detection_graph, sess)
		currentFramePosition, currentHeight, currentWidth = detector_utils.draw_box_on_image(num_hands_detect, 0.2, scores, boxes, w, h, originalFrame)		
		
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
		sleep(0.1)
		#print(UpDownRightLeft)
		#print(np.where( UpDownRightLeft > 30 ))
	
	video.release()
	cv2.destroyAllWindows()
	direction = np.argmax(UpDownRightLeft)
	return direction

#ans = timeToTest()
#print(ans)
#print(time.time())
#time.sleep(3)
#print(time.time())





