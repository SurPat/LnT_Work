from __future__ import print_function
import sys
import cv2
import imutils
import numpy as np


def Seal_Check():
    print("Seal Check")
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (384, 512))

    def rescale_frame(frame, percent=80):  # make the video windows a bit smaller
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    while cap.isOpened():
        text = ""
        ret, frame = cap.read()
        frame = rescale_frame(frame)
        out_new = np.uint8(frame)
        out_Gray = cv2.cvtColor(out_new, cv2.COLOR_BGR2GRAY)
        ret, thresh_out = cv2.threshold(out_Gray, 37, 255, cv2.THRESH_BINARY_INV)
        kernel_ip = np.ones((2, 2), np.uint8)
        eroded_ip = cv2.erode(thresh_out, kernel_ip, iterations=1)
        dilated_ip = cv2.dilate(eroded_ip, kernel_ip, iterations=1)
        #cv2.imshow("dileted", dilated_ip)
        #             cv2.imshow("testing 222", dilated_ip)
        cnts = cv2.findContours(dilated_ip.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #     print(len(cnts))

        if len(cnts) == 0:
            flag_empty = 1

            flag_detected = 0
            #         text = "Empty Frame"
            #         cv2.putText(frame, text, (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2)
            # cv2.imshow("Decision", frame)
            cv2.waitKey(30)
            continue
        # read image and take first channel only
        # img = cv2.imread("half with cap.jpg")
        #     img = cv2.imread("stick.jpg")
        bottle_gray = cv2.cvtColor(out_new, cv2.COLOR_BGR2GRAY)
        # bottle_gray = cv2.split(bottle_3_channel)[0]
        #     cv2.imshow("Bottle Gray", bottle_gray)
        # cv2.waitKey(0)

        # blur image
        bottle_gray = cv2.GaussianBlur(bottle_gray, (7, 7), 0)
        #     cv2.imshow("Bottle Gray Smoothed 7 x 7", bottle_gray)
        # cv2.waitKey(0)
        # draw histogram
        # plt.hist(bottle_gray.ravel(), 256,[0, 256]); plt.show()

        # manual threshold
        bottle_gray = np.uint8(bottle_gray)
        bottle_threshold = cv2.threshold(bottle_gray, 20, 255, cv2.THRESH_BINARY_INV)[1]
        bottle_threshold = np.uint8(bottle_threshold)
        #     cv2.imshow("Bottle Gray Threshold 27.5", bottle_threshold)
        # cv2.waitKey(0)

        # apply opening operation
        kernel_O = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        bottle_open = cv2.morphologyEx(bottle_threshold, cv2.MORPH_OPEN, kernel_O, 3)
        kernel_C = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        bottle_close = cv2.morphologyEx(bottle_open, cv2.MORPH_CLOSE, kernel_C, 3)
        #cv2.imshow("Bottle Open 5 x 5", bottle_close)

        # cv2.waitKey(0)

        # find all contours
        contours = cv2.findContours(bottle_close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        bottle_clone = out_new.copy()
        cv2.drawContours(bottle_clone, contours, -1, (0, 255, 0), 2)

        # sort contours by area
        areas = [cv2.contourArea(contour) for contour in contours]
        if len(areas) == 0:
            cv2.imshow("Decision", frame)
            continue
        (contours, areas) = zip(*sorted(zip(contours, areas), key=lambda a: a[1]))
        # print contour with largest area
        bottle_clone = out_new.copy()
        cv2.drawContours(bottle_clone, [contours[-1]], -1, (0, 255, 0), 2)
        #cv2.imshow("Largest contour", bottle_clone)
        # cv2.waitKey(0)

        # draw bounding box, calculate aspect and display decision
        bottle_clone = out_new.copy()
        (x, y, w, h) = cv2.boundingRect(contours[-1])
        # print(x,y,w,h)
        aspectRatio = w / float(h)
        print(x)
        if (60 < x < 380):
            if (aspectRatio > 3):
                cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(bottle_clone, "Missing Cap", (25, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            elif (aspectRatio > 1.83 or aspectRatio < 1.3):
                cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(bottle_clone, "Open Cap", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            elif (1.5 < aspectRatio < 1.63):
                cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(bottle_clone, "good Cap", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                #cv2.imshow('NewFrame',bottle_clone)
            cv2.imshow("Decision", bottle_clone)
            print(bottle_clone.shape)
        else:
            cv2.imshow("Decision", frame)
        key = cv2.waitKey(30)
        if key == ord('q') or key == 27:
            break
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(app.exec_())

if __name__ == "__main__":
    Seal_Check()