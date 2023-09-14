import cv2
import numpy as np
# define the callback function for the button click event
def button_click(state, userdata):
    print("Button clicked")

# create the window and image
cv2.namedWindow("Button")
image = 255 * np.ones((100, 200, 3), dtype=np.uint8)

# create the button
cv2.createButton("Click me", button_click, None, cv2.QT_PUSH_BUTTON)

# display the image
cv2.imshow("Button", image)
cv2.waitKey(0)
cv2.destroyAllWindows()