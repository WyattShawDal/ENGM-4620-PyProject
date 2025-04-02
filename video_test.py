'''File name: video_test.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: Used to test video capture
Note: NOT used to run the application
'''
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class VideoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenCV Video in PyQt5")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # QLabel for video
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Start button
        self.start_button = QPushButton("Start Video", self)
        self.start_button.clicked.connect(self.start_video)
        self.layout.addWidget(self.start_button)

        self.central_widget.setLayout(self.layout)

        # OpenCV Video Capture
        self.cap = cv2.VideoCapture(0)  # 0 for webcam

        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_video(self):
        self.timer.start(30)  # Update every 30ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoApp()
    window.show()
    sys.exit(app.exec_())
