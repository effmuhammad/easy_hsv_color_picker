import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog

# define the callback function
def select_file():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(None, "Select File", "", "All Files (*);;Python Files (*.py)", options=options)
    if file_name:
        print("Selected file:", file_name)

# create the PyQt application
app = QApplication(sys.argv)

# create a QWidget instance
root = QWidget()

# create a QPushButton instance and set the text
button = QPushButton("Select File", root)

# set the size and position of the button
button.setGeometry(10, 10, 100, 30)

# set the callback function for the button click event
button.clicked.connect(select_file)

# show the window
root.show()

# start the PyQt event loop
sys.exit(app.exec_())