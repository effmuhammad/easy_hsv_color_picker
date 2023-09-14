import cv2
import numpy as np

# define the callback function for the button click event
def button_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Button clicked")

# create the window and image
cv2.namedWindow("Button")
image = 255 * np.ones((100, 200, 3), dtype=np.uint8)

# draw the button
cv2.rectangle(image, (10, 10), (190, 90), (0, 0, 255), -1)
cv2.putText(image, "Click me", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# set the mouse event handler for the button
cv2.setMouseCallback("Button", button_click)

def on_trackbar(val):
    pass

# create the trackbars
cv2.createTrackbar('Hmin', 'Button', 0, 179, on_trackbar)
cv2.createTrackbar('Smin', 'Button', 0, 255, on_trackbar)
cv2.createTrackbar('Vmin', 'Button', 0, 255, on_trackbar)
cv2.createTrackbar('Hmax', 'Button', 179, 179, on_trackbar)
cv2.createTrackbar('Smax', 'Button', 255, 255, on_trackbar)
cv2.createTrackbar('Vmax', 'Button', 255, 255, on_trackbar)

# display the image
cv2.imshow("Button", image)
cv2.waitKey(0)
cv2.destroyAllWindows()