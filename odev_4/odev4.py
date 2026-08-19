import cv2
import time
from collections import deque
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
pts = deque(maxlen=60)
face_start_time = None
while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)
    if len(faces) > 0:
        if face_start_time is None:
            face_start_time = time.time()

        elapsed_time = int (time.time()-face_start_time)
        (x,y,w,h) = faces[0]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cx = x + (w//2)
        cy = y + (h//2)
        text_center = f"Merkez: X={cx}, Y={cy}"
        cv2.putText(frame,text_center,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        text_timer = f"Sure: {elapsed_time} sn"
        cv2.putText(frame,text_timer,(width - 250,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        pts.appendleft((cx,cy))
    else:
        face_start_time = None

    for i in range(1,len(pts)):
        cv2.line(frame,pts[i-1],pts[i],(0,0,255),2)

    cv2.imshow('Yuz Tespiti', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()