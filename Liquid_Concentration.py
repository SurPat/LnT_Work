from PIL import Image
import cv2 

cap = cv2.VideoCapture(0)

def AvgColVal(topleftcorn,bottomrightcorn):
	pixcolarray = []
	pixcol_B = 0
	pixcol_G = 0
	pixcol_R = 0
	for i in range(topleftcorn[1],bottomrightcorn[1]):
		print("##################################Row number:{0}###############################".format(i))
		for k in range(topleftcorn[0],bottomrightcorn[0]):
			pixcolor = frame[i,k]
			pixcolarray.append(pixcolor)
			pixcol_B = pixcol_B + pixcolor[0]
			pixcol_G = pixcol_G + pixcolor[1]
			pixcol_R = pixcol_R + pixcolor[2]
	print("pixel color:",pixcol_B,pixcol_G,pixcol_R)
	print("Length: ",len(pixcolarray))
	avgcol = int((pixcol_B)/len(pixcolarray)),int((pixcol_G)/len(pixcolarray)),int((pixcol_R)/len(pixcolarray))
	print("average color value:", avgcol)
	return str(avgcol)


while cap.isOpened():
	ret, frame = cap.read()
	width,length, __ = frame.shape
	print("width and length: ", width, length)
	(centlen, centwid) = (int(width/2),int(length/2))
	#print("Center pixel: ",centwid, centlen)
	#print("center pixel color:", frame[centwid,centlen])
	topleftcorn, bottomrightcorn = (centwid-5, centlen-5), (centwid+5, centlen+5)
	#print("topleftcorn, bottomrightcorn", topleftcorn, bottomrightcorn)
	pixcols = AvgColVal(topleftcorn,bottomrightcorn)
	cv2.rectangle(frame,topleftcorn, bottomrightcorn , (255,0,0), 2)
	cv2.putText(frame,pixcols,(bottomrightcorn[0]+10,bottomrightcorn[1]-10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 255, 255), 2)
	cv2.imshow("window",frame)
	#cv2.waitKey(1)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()


#print(PIL.__version__)

# red_image = Image.open("multi.png")
# #Create a PIL.Image object

# length,width = red_image.size

# print("center:", length/2,width/2)

# red_image_rgb = red_image.convert("RGB")
# #Convert to RGB colorspace


# rgb_pixel_value = red_image_rgb.getpixel((920,50))
# #Get color from (x, y) coordinates
# print("first: ",rgb_pixel_value)

# rgb_pixel_value = red_image_rgb.getpixel((1880,50))
# #Get color from (x, y) coordinates
# print("Second: ",rgb_pixel_value)

# rgb_pixel_value = red_image_rgb.getpixel((2840,50))
# #Get color from (x, y) coordinates
# print("third: ",rgb_pixel_value)

# rgb_pixel_value = red_image_rgb.getpixel((3800,50))
# #Get color from (x, y) coordinates
# print("fourth: ",rgb_pixel_value)