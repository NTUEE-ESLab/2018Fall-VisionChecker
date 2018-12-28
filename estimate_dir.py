from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from utils import detector_utils as detector_utils

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

detection_graph, sess = detector_utils.load_inference_graph()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
timeDuration = 0
num_hands_detect = 1;
boundForHandPosition = [0,0]
sideHeight = 0
sideWidth = 0


# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	originalFrame = vs.read()
	originalFrame = (np.fliplr(originalFrame)).copy()
	originalFrame = originalFrame if args.get("video", None) is None else originalFrame[1]
	originalFrameSize = originalFrame.shape
	frame = originalFrame

	text = "Not Moving"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	# resize the frame, convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=750)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	
	if firstFrame is None:
		firstFrame = originalFrame
		firstFrameRGB = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2RGB)
		boxes, scores = detector_utils.detect_objects(firstFrameRGB,
                                                      detection_graph, sess)

		boundForHandPosition, sideHeight, sideWidth = detector_utils.draw_box_on_image(num_hands_detect, 0.2, scores, boxes, originalFrameSize[1], originalFrameSize[0], firstFrameRGB)
		firstFrame = gray
		print(boundForHandPosition, sideHeight, sideWidth)
		adjustY = 100
		#sideHeight = sideHeight -100
		if(sideHeight==0 or sideWidth==0):
			print("Error: Not Found Hand")
			break
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 127, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Moving"


	# show the frame and record if the user presses a key

	
	#boundForHandPosition = [originalFrameSize[0]//4 - sideHeight//2 + adjustY , originalFrameSize[1]*3//4 - sideWidth//2]
	boundForHandUp = [boundForHandPosition[0] - sideHeight , boundForHandPosition[1]]
	boundForHandDown = [boundForHandPosition[0] + sideHeight, boundForHandPosition[1]]
	boundForHandRight = [boundForHandPosition[0] , boundForHandPosition[1] +sideWidth]
	boundForHandLeft = [boundForHandPosition[0] , boundForHandPosition[1] - sideWidth]

	#print(boundForHandUp, boundForHandDown, boundForHandRight, boundForHandLeft)



	# (x,y) is (col,row)
	cv2.rectangle(originalFrame, (boundForHandPosition[1], boundForHandPosition[0]), (boundForHandPosition[1] + sideWidth , boundForHandPosition[0] + sideHeight), (0, 255, 0), 2) 
	cv2.rectangle(originalFrame, (boundForHandUp[1], boundForHandUp[0]), (boundForHandUp[1] + sideWidth , boundForHandUp[0] + sideHeight), (0, 255, 0), 2)
	cv2.rectangle(originalFrame, (boundForHandDown[1], boundForHandDown[0]), (boundForHandDown[1] + sideWidth , boundForHandDown[0] + sideHeight), (0, 255, 0), 2)
	cv2.rectangle(originalFrame, (boundForHandRight[1], boundForHandRight[0]), (boundForHandRight[1] + sideWidth , boundForHandRight[0] + sideHeight), (0, 255, 0), 2)
	cv2.rectangle(originalFrame, (boundForHandLeft[1], boundForHandLeft[0]), (boundForHandLeft[1] + sideWidth , boundForHandLeft[0] + sideHeight), (0, 255, 0), 2)

	handInitial = frameDelta[ boundForHandPosition[0]:boundForHandPosition[0]+sideHeight , boundForHandPosition[1]:boundForHandPosition[1]+sideWidth ]
	handUp = frameDelta[ boundForHandUp[0]:boundForHandUp[0]+sideHeight , boundForHandUp[1]:boundForHandUp[1]+sideWidth ]
	handDown = frameDelta[ boundForHandDown[0]:boundForHandDown[0]+sideHeight , boundForHandDown[1]:boundForHandDown[1]+sideWidth  ]
	handRight = frameDelta[ boundForHandRight[0]:boundForHandRight[0]+sideHeight , boundForHandRight[1]:boundForHandRight[1]+sideWidth  ]
	handLeft = frameDelta[ boundForHandLeft[0]:boundForHandLeft[0]+sideHeight , boundForHandLeft[1]:boundForHandLeft[1]+sideWidth  ]

	middleValue = round(np.mean(handInitial),3)
	upValue = round(np.mean(handUp),3)
	downValue = round(np.mean(handDown),3)
	rightValue = round(np.mean(handRight),3)
	leftValue = round(np.mean(handLeft),3)

	print(middleValue, upValue, downValue, rightValue, leftValue)

	#cv2.imshow("Security Feed", originalFrame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)

	#key = cv2.waitKey(1) & 0xFF

	if upValue > 30:
		#print("Up")
		cv2.putText(originalFrame, "Up", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
		cv2.imshow("Security Feed", originalFrame)
		key = cv2.waitKey(1) & 0xFF
		continue
	if rightValue > 30:
		#print("Right")
		cv2.putText(originalFrame, "Right", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
		cv2.imshow("Security Feed", originalFrame)
		key = cv2.waitKey(1) & 0xFF
		continue
	if leftValue > 30:
		#print("Left")
		cv2.putText(originalFrame, "Left", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
		cv2.imshow("Security Feed", originalFrame)
		key = cv2.waitKey(1) & 0xFF
		continue
	if middleValue<30 :
		#print("Not Move")
		cv2.putText(originalFrame, "Not Move", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
		cv2.imshow("Security Feed", originalFrame)
		key = cv2.waitKey(1) & 0xFF
		continue
	else:
		#print("Down")
		cv2.putText(originalFrame, "Down", (80, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1, cv2.LINE_AA)
		cv2.imshow("Security Feed", originalFrame)
		key = cv2.waitKey(1) & 0xFF
		continue


	'''
	timeDuration = timeDuration+1
	print(timeDuration)

	if timeDuration==500 :
		break
	'''


# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()