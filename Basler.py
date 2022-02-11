''' Anand Koirala email: anand.koirala@cqumail.com
code for the video explained in https://www.youtube.com/watch?v=A61Zn026Ruw&t=110s '''

from flask import Flask, Response
import cv2
import pypylon.pylon as py
from datetime import datetime
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
#video = cv2.VideoCapture(0)

icam = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
icam.Open()
#icam.PixelFormat = "RGB8"
icam.PixelFormat = "BayerRG 8"

@app.route('/')
def index():
    return "Default Message"
#def gen(video):
def gen():
    while True:
        #success, image = video.read()
        frame = icam.GrabOne(4000) ### 4ms time for grabbing image 
        frame = frame.Array
        frame = cv2.resize(frame, (0,0), fx=0.8366, fy=1, interpolation=cv2.INTER_LINEAR)### 2048x2048 resolution or INTER_AREA  inter_linear is fastest for and good for downsizing 
        #image = cv2.resize(image, (0,0), fx=0.44444, fy=0.53125, interpolation=cv2.INTER_AREA)##my code to resize image by a scale factor for display window........only.... scale is multiplier 0.3 is less less size than 0.5 which is half size
        # Put current DateTime on each frame
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(image,str(datetime.now()),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
        # ret, jpeg = cv2.imencode('.jpg', image)        
        # frame = jpeg.tobytes() 

        orig = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        (cnts, _) = contours.sort_contours(cnts)

        pixles_to_size = None

        for c in cnts:
            if cv2.contourArea(c) < 100:
                continue

            bbox = cv2.minAreaRect(c)
            bbox = cv2.cv.BoxPoints(bbox) if imutils.is_cv2() else cv2.boxPoints(bbox)
            box = np.array(bbox, dtype="int")

            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)

            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            if pixles_to_size is None:
                pixles_to_size = 4  # change value as per camera calibration

            dimA = dA / pixles_to_size
            dimB = dB / pixles_to_size
            print("width value is",dimA)
            print("lenth is",dimB)

            cv2.putText(orig, "{:.2f}mm".format(dimB), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (255, 255, 255), 2)
            cv2.putText(orig, "{:.2f}mm".format(dimA), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                        (255, 255, 255), 2)
        print("-----%s seconds---" % (time.time()-start_time))       
        #yield (b'--frame\r\n'
               #b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # yield (b'--frame\r\n'
        #        b'Content-Type:image/jpeg\r\n'
        #        b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
        #        b'\r\n' + frame + b'\r\n')
@app.route('/video_feed') #### this is new route which is needed for watching stream
def video_feed():
    #global video
    #return Response(gen(video),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, threaded=True) #### this is developer environment and process one request at a time..
##production###  below is the way to stream in production so multiple requests gets accepted. pip3 install gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

####to view the stream use http://localhost:5000/video_feed  or for opencv use cv2.VideoCapture(http://localhost:5000/video_feed)to read the stream.. #####
#### or u can replace localhost with 0.0.0.0 and if you wish to change port number or video_feed to other texts you can do it... ###