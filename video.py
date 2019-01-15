import cv2

video = cv2.VideoCapture(-1)
ok, frame = video.read()
cv2.imshow("123", frame)
