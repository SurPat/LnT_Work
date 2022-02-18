import cv2
from scipy.spatial import distance as dist
import imutils
from imutils import perspective, contours
import numpy as np
import time


def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5

global prod_dim

prods = [('Connector',42,38),('cap',36,18),('Washer',18,18),('Sharpner',28,18),('clip',34,18)]

def ProdLabel(l, w):
    for i in prods:
        prodname = i[0]
        ProdLen = i[1]
        ProdWid = i[2]
        print(i, ProdLen, ProdWid)
        if ((((ProdLen + 3) >= l >= (ProdLen - 3)) & (ProdWid + 3 >= l >= (ProdWid - 3))) or (
                                            ((ProdLen + 3) >= w >= (ProdLen - 3)) & (ProdWid + 3 >= w >= (ProdWid - 3)))):
            return prodname
        else:
            continue        
# initialize camera

def ProdSort(frame):
    start_time = time.time()
    orig = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    try:
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

            #compute the size of object
            if pixles_to_size is None:
                pixles_to_size = 4  # change value as per camera calibration

            dimA = dA / pixles_to_size
            dimB = dB / pixles_to_size

            label = ProdLabel(dimA, dimB)

            #print("width value is",dimA)
            #print("lenth is",dimB)


            cv2.putText(orig, "{:.2f}mm".format(dimB), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (255, 255, 255), 2)
            cv2.putText(orig, "{:.2f}mm".format(dimA), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                        (255, 255, 255), 2)
            cv2.putText(orig, label, (int(trbrX + 10), int(trbrY+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                        (255, 255, 255), 2)
            frame_time = (time.time()-start_time)
            print("-----{0} seconds---".format(frame_time))
            FPS = 1/frame_time
            print("FPS: ", FPS)
            FPS_str = "FPS = {0}".format(str(FPS))
            cv2.putText(orig, FPS_str, (1000, 1000), cv2.FONT_HERSHEY_SIMPLEX, 0.65,(255, 255, 255), 2)
        cv2.imshow('frame', frame)
        cv2.imshow("Test_Frame", orig)
    except:
        print("Searching for contours..")
        cv2.imshow("Test_Frame", orig)
