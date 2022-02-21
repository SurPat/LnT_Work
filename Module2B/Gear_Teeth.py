
import cv2
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.fftpack

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()

    start_time = time.time()
    flter_img = cv2.bilateralFilter(img, 5, 175, 175)

    median_blurred = cv2.medianBlur(flter_img, 5)
    edge_detect = cv2.Canny(median_blurred, 75, 200)

    contours, _ = cv2.findContours(edge_detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 5) & (len(approx) < 25) & (area > 50) ):
            contour_list.append(contour)
    c = max(contours, key = cv2.contourArea)
    img = np.zeros_like(img)
    cv2.drawContours(img, contour_list, -1, (255, 255, 255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)

    # Get centroid
    Mid = cv2.moments(c)
    cX = int(Mid["m10"] / Mid["m00"])
    cY = int(Mid["m01"] / Mid["m00"])

    def distance(a,b): return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    angle = 0
    increment = 1/100
    distances = []
    display_image = img.copy() 

    while angle < 2*math.pi:

        img_size = max(img.shape)
        ray_end = int(math.sin(angle) * img_size + cX), int(math.cos(angle) * img_size + cY)
        center = cX, cY

        mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)

        cv2.line(mask, center, ray_end, 255, 2)

        gear_slice = cv2.bitwise_and(img, img, mask = mask)
        _, thresh = cv2.threshold(cv2.cvtColor(gear_slice, cv2.COLOR_BGR2GRAY), 0 , 255, 0)

        edge_slice_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        Mid = cv2.moments(max(edge_slice_contours, key = cv2.contourArea))

        edge_location = int(Mid["m10"] / Mid["m00"]), int(Mid["m01"] / Mid["m00"])
        cv2.circle(display_image, edge_location, 0, (0,255,0), 4) 

        center2edge_dist = distance(center, edge_location)
        
        distances.append(-center2edge_dist)
        temp = display_image.copy() 

        cv2.imshow('Master_Image', temp)
        k = cv2.waitKey(1)
        if k == 27: break
        angle += increment

    Fourier_transform = scipy.fftpack.fft(distances)
    num_teeth = list(Fourier_transform).index(max(Fourier_transform[2:200])) - 1
    print("--- %s seconds ---" % (time.time() - start_time))

    print('Number of teeth in this gear: ' + str(num_teeth ))
    cv2.putText(temp, 'Number of teeth in this gear: '+ str(num_teeth ), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

    cv2.imshow('raw_image', temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()