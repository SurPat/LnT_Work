import pypylon.pylon as py
import numpy as np
import cv2
import time

last_timestamp = 0
timestamp = 0

# Simply get the first available pylon device.
first_device = py.TlFactory.GetInstance().CreateFirstDevice()
instant_camera = py.InstantCamera(first_device)
instant_camera.Open()

# Optional if you set it in Pylon Viewer
instant_camera.PixelFormat = "RGB8"

instant_camera.StartGrabbing(py.GrabStrategy_LatestImages)


while True:
    # Update current image in video window.
    # Grab one image.
    img = np.zeros((1, 1))
    if instant_camera.NumReadyBuffers:
        res = instant_camera.RetrieveResult(1000)
        if res:
            try:
                if res.GrabSucceeded():
                    currImg = res.Array
                    img = cv2.cvtColor(currImg, cv2.COLOR_BAYER_RG2RGB)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

        # cv2.imshow('frame', frame)
        # cv2.imshow("Test_Frame", orig)
                    timestamp = time.time()
                    if 0 == last_timestamp:
                        last_timestamp = timestamp
                    else:
                        period = timestamp - last_timestamp
                        last_timestamp = timestamp

                        frame_rate = 1 / period
                        frametime = period

                        print(frame_rate)

                    # Display new image in video window.
                    cv2.imshow('Video', currImg)
                    # Wait    1 ms.
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
