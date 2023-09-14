import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap

# define the callback function
def mouse_callback(event):
    print("Mouse clicked at ({}, {})".format(event.x(), event.y()))

# create the PyQt application
app = QApplication(sys.argv)

# create a QWidget instance
root = QWidget()

# create a QLabel instance and set the image
label = QLabel(root)
pixmap = QPixmap("Sample.PNG")
label.setPixmap(pixmap)

# set the size of the label to match the image size
label.resize(pixmap.width(), pixmap.height())

# set the mouse event handler
label.mousePressEvent = mouse_callback

# show the window
root.show()

# start the PyQt event loop
sys.exit(app.exec_())