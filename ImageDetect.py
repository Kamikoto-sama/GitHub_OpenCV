import cv2

def Detect_Faces(imagePath):
    faceCascade = cv2.CascadeClassifier('face.xml')
    smileCascade = cv2.CascadeClassifier('smile.xml')
    eyeCascade = cv2.CascadeClassifier('eye.xml')
 
    image = cv2.imread(imagePath)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),2)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,      
        minSize=(30, 30)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        
        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=15,
            minSize=(25, 25),
            )
        
        for (x, y, w, h) in smile:
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (0, 255, 0), 2)

        eye = eyeCascade.detectMultiScale(roi_gray,
            scaleFactor= 1.5,
            minNeighbors=10,
            minSize=(5, 5),
            )
               
        for (x,y,w,h) in eye:
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite("image.png",image)
    # image = cv2.imread(imagePath)
    # cascades = cv2.CascadeClassifier("faces.xml")

    # gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray,(5,5),5)

    # faces = cascades.detectMultiScale(
    # gray,
    # scaleFactor = 1.1,
    # minNeighbors = 5,
    # minSize = (30,30)
    #     )

    # for (x,y,w,h) in faces:
    #     cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)

    # 