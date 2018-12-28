import time
import cv2
import numpy as np
from utils import detector_utils as detector_utils
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

# detection_graph, sess = detector_utils.load_inference_graph()

# video = cv2.VideoCapture(0)

print("hi!")


def timeToTest():
	firstFramePosition = [0,0]
	sideHeight = 0
	sideWidth = 0
	timeOut = time.time()+10
	num_hands_detect = 1;
	UpDownRightLeft = np.array([0, 0, 0, 0, 0])


	while(True):
		ok, firstFrame = video.read()
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

	while(True):
		if time.time() >timeOut:
			print("Time is Up")
			break
		ok, originalFrame = video.read()
		if originalFrame is None:
			break;
		originalFrame = (np.fliplr(originalFrame)).copy()
		cv2.rectangle(originalFrame, (firstFramePosition[1], firstFramePosition[0]), (firstFramePosition[1]+sideWidth,firstFramePosition[0]+sideHeight), (0, 0, 255), 2)
		originalFrame = cv2.cvtColor(originalFrame, cv2.COLOR_BGR2RGB)
		boxes, scores = detector_utils.detect_objects(originalFrame, detection_graph, sess)
		currentFramePosition, currentHeight, currentWidth = detector_utils.draw_box_on_image(num_hands_detect, 0.2, scores, boxes, w, h, originalFrame)		
		if(currentHeight==0 or currentHeight==0):
			cv2.putText(originalFrame, "Not Found Hand", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.imshow("Security Feed", originalFrame)
			key = cv2.waitKey(1) & 0xFF
			continue
		'''
		ok, bbox = tracker.update(originalFrame)
		if ok:
			p1 = (int(bbox[0]),int(bbox[1]))
			p2 = (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3]))
			currentFramePosition[0] = bbox[1]
			currentFramePosition[1] = bbox[0]
			cv2.rectangle(originalFrame, p1, p2, (255,0,0),2)
		'''


		if firstFramePosition[0]-currentFramePosition[0]>sideHeight//2:
			cv2.putText(originalFrame, "Up", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.imshow("Security Feed", originalFrame)
			key = cv2.waitKey(1) & 0xFF
			UpDownRightLeft[0] = UpDownRightLeft[0]+1
			continue
		if currentFramePosition[0]-firstFramePosition[0]>sideHeight//2:
			cv2.putText(originalFrame, "Down", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.imshow("Security Feed", originalFrame)
			key = cv2.waitKey(1) & 0xFF
			UpDownRightLeft[1] = UpDownRightLeft[1]+1
			continue
		if firstFramePosition[1]-currentFramePosition[1]>sideWidth//2:
			cv2.putText(originalFrame, "Left", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.imshow("Security Feed", originalFrame)
			key = cv2.waitKey(1) & 0xFF
			UpDownRightLeft[2] = UpDownRightLeft[2]+1
			continue
		if currentFramePosition[1]-firstFramePosition[1]>sideWidth//2:
			cv2.putText(originalFrame, "Right", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.imshow("Security Feed", originalFrame)
			key = cv2.waitKey(1) & 0xFF
			UpDownRightLeft[3] = UpDownRightLeft[3]+1
			continue
		else:
			cv2.putText(originalFrame, "Not Move", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.imshow("Security Feed", originalFrame)
			key = cv2.waitKey(1) & 0xFF
			UpDownRightLeft[4] = UpDownRightLeft[4]+1
			continue
		

	video.release()
	cv2.destroyAllWindows()
	direction = np.argmax(UpDownRightLeft)
	return direction

ans = timeToTest()
print(ans)
#print(time.time())
#time.sleep(3)
#print(time.time())





