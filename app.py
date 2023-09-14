from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QFileDialog
import sys

class MainApp(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Drag and Drop")
        self.resize(720, 480)
        self.setAcceptDrops(True)

        # create a QPushButton instance and set the text
        self.button = QPushButton("Select File", app)

        # set the size and position of the button
        self.button.setGeometry(10, 10, 100, 30)

        # set the callback function for the button click event
        self.button.clicked.connect(self.select_file)
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)

    # define the callback function
    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(None, "Select File", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            print("Selected file:", file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainApp(app)
    ui.show()
    sys.exit(app.exec_())