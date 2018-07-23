import cv2

def Detect_Faces(videoPath):
	capture = cv2.VideoCapture(videoPath)
	cascades = cv2.CascadeClassifier("haarcascade.xml")

	while(capture.isOpened()):
	    ret, frame = capture.read()

	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    faces = cascades.detectMultiScale(gray,scaleFactor = 1.1,
	        minNeighbors = 5,minSize = (30,30))

	    for (x,y,w,h) in faces:
	        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0))

	    cv2.imshow('Press "q" to exit',frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	capture.release()
	cv2.destroyAllWindows()
	return