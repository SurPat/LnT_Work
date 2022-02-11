''' Anand Koirala email: anand.koirala@cqumail.com
code for the video explained in https://www.youtube.com/watch?v=A61Zn026Ruw&t=110s '''
import cv2
import pypylon.pylon as py
from datetime import datetime


icam = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
icam.Open()
#icam.PixelFormat = "RGB8"
icam.PixelFormat = "Bayerrg8"


def gen():
    while True:
        #success, image = video.read()
        image = icam.GrabOne(4000) ### 4ms time for grabbing image 
        image = image.Array
        image = cv2.resize(image, (0,0), fx=0.8366, fy=1, interpolation=cv2.INTER_LINEAR)### 2048x2048 resolution or INTER_AREA  inter_linear is fastest for and good for downsizing 
        #image = cv2.resize(image, (0,0), fx=0.44444, fy=0.53125, interpolation=cv2.INTER_AREA)##my code to resize image by a scale factor for display window........only.... scale is multiplier 0.3 is less less size than 0.5 which is half size
        # Put current DateTime on each frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image,str(datetime.now()),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("frame",image)
        ret, jpeg = cv2.imencode('.jpg', image)        
        frame = jpeg.tobytes()        
        #yield (b'--frame\r\n'
               #b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n'
               b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
               b'\r\n' + frame + b'\r\n')

if __name__ == "__main__"
    gen()