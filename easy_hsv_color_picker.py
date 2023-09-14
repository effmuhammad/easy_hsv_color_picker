import cv2
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog

image_src = None
image_hsv = None
image_mask = None
pixel = (0,0,0) #RANDOM DEFAULT VALUE
hue_tolerance = 5
saturation_tolerance = 5
value_tolerance = 5
lower_hsv = np.array([0, 0, 0])
upper_hsv = np.array([179, 255, 255])

ftypes = [
    ("All files", "*.*"),
    ("JPG", "*.jpg;*.JPG;*.JPEG"), 
    ("PNG", "*.png;*.PNG"),
    ("GIF", "*.gif;*.GIF"),
]

def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        # set the boundary for hue
        boundary = 180
    elif ranges == 1:
        # set the boundary for saturation and value
        boundary = 255

    if(value + tolerance > boundary):
        value = boundary
    elif (value - tolerance < 0):
        value = 0
    else:
        if upper_or_lower == 1:
            value = value + tolerance
        else:
            value = value - tolerance
    return value

def pick_color(event,x,y,flags,param):
    global lower_hsv, upper_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        list_pixels = []
        pixel = image_hsv[y,x]
        square_dim= 5
        # get pixel for the area around the mouse click
        for i in range(-square_dim,square_dim+1):
            for j in range(-square_dim,square_dim+1):
                list_pixels.append(image_hsv[y+i,x+j])
        # get the average of the pixels
        # pixel = np.mean(list_pixel, axis=0)
        # pixel = np.round(pixel).astype(int)
        
        # check boundaries for each pixel
        hue_upper = []
        hue_lower = []
        saturation_upper = []
        saturation_lower = []
        value_upper = []
        value_lower = []

        for pixel in list_pixels:
            hue_upper.append(check_boundaries(pixel[0], hue_tolerance, 0, 1))
            hue_lower.append(check_boundaries(pixel[0], hue_tolerance, 0, 0))
            saturation_upper.append(check_boundaries(pixel[1], saturation_tolerance, 1, 1))
            saturation_lower.append(check_boundaries(pixel[1], saturation_tolerance, 1, 0))
            value_upper.append(check_boundaries(pixel[2], value_tolerance, 1, 1))
            value_lower.append(check_boundaries(pixel[2], value_tolerance, 1, 0))

        hue_upper = int(np.mean(hue_upper))
        hue_lower = int(np.mean(hue_lower))
        saturation_upper = int(np.mean(saturation_upper))
        saturation_lower = int(np.mean(saturation_lower))
        value_upper = int(np.mean(value_upper))
        value_lower = int(np.mean(value_lower))

        upper_hsv =  np.array([hue_upper, saturation_upper, value_upper])
        lower_hsv =  np.array([hue_lower, saturation_lower, value_lower])

        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS 
        image_mask = cv2.inRange(image_hsv,lower_hsv,upper_hsv)
        cv2.imshow("Thresholding",image_mask)
        # Create trackbars for threshold values
        cv2.createTrackbar('Hmin', 'Thresholding', hue_lower, 179, on_trackbar)
        cv2.createTrackbar('Smin', 'Thresholding', saturation_lower, 255, on_trackbar)
        cv2.createTrackbar('Vmin', 'Thresholding', value_lower, 255, on_trackbar)
        cv2.createTrackbar('Hmax', 'Thresholding', hue_upper, 179, on_trackbar)
        cv2.createTrackbar('Smax', 'Thresholding', saturation_upper, 255, on_trackbar)
        cv2.createTrackbar('Vmax', 'Thresholding', value_upper, 255, on_trackbar)

        # create the window and image
        image = 255 * np.ones((100, 200, 3), dtype=np.uint8)
        image = cv2.rectangle(image, (10, 10), (190, 90), (0, 0, 255), -1)
        image = cv2.putText(image, "Get Value", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Button", image)

        # set the mouse event handler for the button
        cv2.setMouseCallback("Button", button_click)

def on_trackbar(val):
    global lower_hsv, upper_hsv, image_hsv, image_src, image_mask
    lower_hsv[0] = cv2.getTrackbarPos('Hmin', 'Thresholding')
    lower_hsv[1] = cv2.getTrackbarPos('Smin', 'Thresholding')
    lower_hsv[2] = cv2.getTrackbarPos('Vmin', 'Thresholding')
    upper_hsv[0] = cv2.getTrackbarPos('Hmax', 'Thresholding')
    upper_hsv[1] = cv2.getTrackbarPos('Smax', 'Thresholding')
    upper_hsv[2] = cv2.getTrackbarPos('Vmax', 'Thresholding')
    image_mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
    image_mask = cv2.bitwise_and(image_src, image_src, mask=image_mask)

    cv2.imshow('Thresholding', image_mask)

# define the callback function for the button click event
def button_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"[{lower_hsv.tolist()},{upper_hsv.tolist()}],")

def main():
    global image_hsv, pixel, image_mask, image_src, lower_hsv, upper_hsv

    #OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw() #HIDE THE TKINTER GUI
    file_path = filedialog.askopenfilename()
    root.update()
    image_src = cv2.imread(file_path)

    if image_src is not None:
        # resize image by percentage
        scale_percent = 50 # percent of original size
        width = int(image_src.shape[1] * scale_percent / 100)
        height = int(image_src.shape[0] * scale_percent / 100)
        dim = (width, height)
        image_src = cv2.resize(image_src, dim, interpolation = cv2.INTER_AREA)
        
        cv2.imshow("BGR",image_src)

        #CREATE THE HSV FROM THE BGR IMAGEs
        image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
        cv2.imshow("PickColor",image_src)
        
        #CALLBACK FUNCTION
        cv2.setMouseCallback("PickColor", pick_color)

        cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()