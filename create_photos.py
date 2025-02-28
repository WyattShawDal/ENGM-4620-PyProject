import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit, QProgressBar, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtCore import QTimer, Qt

class VideoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign Language Image Capture")
        self.setGeometry(100, 100, 800, 700)
        
        # Apply dark mode theme
        self.apply_dark_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # QLabel for video
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Input for label character
        self.char_layout = QHBoxLayout()
        self.char_label = QLabel("Label Character:")
        self.char_input = QLineEdit()
        self.char_input.setMaxLength(1)
        self.char_layout.addWidget(self.char_label)
        self.char_layout.addWidget(self.char_input)
        self.layout.addLayout(self.char_layout)
        
        # Counter for images and reset button
        self.counter_layout = QHBoxLayout()
        self.counter_label = QLabel("Current Count: 0")
        self.reset_count_button = QPushButton("Reset Count", self)
        self.reset_count_button.clicked.connect(self.reset_count)
        self.counter_layout.addWidget(self.counter_label)
        self.counter_layout.addWidget(self.reset_count_button)
        self.layout.addLayout(self.counter_layout)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        
        # Start button
        self.start_button = QPushButton("Start Video", self)
        self.start_button.clicked.connect(self.start_video)
        self.buttons_layout.addWidget(self.start_button)
        
        # Take photo button
        self.photo_button = QPushButton("Take Photo", self)
        self.photo_button.clicked.connect(self.take_photo)
        self.photo_button.setEnabled(False)
        self.buttons_layout.addWidget(self.photo_button)
        
        # Auto photo button
        self.auto_button = QPushButton("Start Auto Photos", self)
        self.auto_button.clicked.connect(self.toggle_auto_photo)
        self.auto_button.setEnabled(False)
        self.buttons_layout.addWidget(self.auto_button)
        
        self.layout.addLayout(self.buttons_layout)
        
        # Progress bar for auto photo timing
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)
        
        self.central_widget.setLayout(self.layout)

        # OpenCV Video Capture
        self.cap = cv2.VideoCapture(0)  # 0 for webcam

        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        # Timer for auto photos
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.update_progress)
        
        # Timer for taking photos automatically
        self.photo_timer = QTimer()
        self.photo_timer.timeout.connect(self.take_photo)
        
        # Auto photo state
        self.auto_active = False
        self.progress_value = 0
        self.image_count = 0
        
        # Original frame storage (without border)
        self.original_frame = None

    def apply_dark_theme(self):
        # Create dark palette
        dark_palette = QPalette()
        
        # Set color roles
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Apply palette
        self.setPalette(dark_palette)
        
        # Set stylesheet for more consistent styling
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #353535;
                color: white;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #808080;
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #555555;
                padding: 3px;
                border-radius: 2px;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 3px;
                background-color: #2a2a2a;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
            }
        """)

    def start_video(self):
        self.timer.start(30)  # Update every 30ms
        self.start_button.setText("Stop Video")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.stop_video)
        self.photo_button.setEnabled(True)
        self.auto_button.setEnabled(True)

    def stop_video(self):
        self.timer.stop()
        self.stop_auto_photo()
        self.start_button.setText("Start Video")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start_video)
        self.photo_button.setEnabled(False)
        self.auto_button.setEnabled(False)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Flip the image horizontally for a mirror effect
            frame = cv2.flip(frame, 1)
            
            # Store the original frame for photo capture (without border)
            self.original_frame = frame.copy()
            
            # Draw indicator for auto photo on the display frame only
            if self.auto_active:
                # Calculate the thickness based on progress_value (thicker as it gets closer to taking a photo)
                thickness = max(1, int(self.progress_value / 20))
                color = (0, 255, 0)  # Green
                
                # Draw a rectangle around the frame (for display only)
                cv2.rectangle(frame, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), color, thickness)
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to QImage and display
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def take_photo(self):
        if self.original_frame is None:
            QMessageBox.warning(self, "Warning", "No frame to capture. Start video first.")
            return
            
        char = self.char_input.text()
        if not char or not char.isalpha():
            QMessageBox.warning(self, "Warning", "Please enter a valid letter in the Label Character field.")
            return
            
        # Create directory if it doesn't exist
        char_dir = os.path.join(os.getcwd(), char.lower())
        if not os.path.exists(char_dir):
            os.makedirs(char_dir)
            
        # Increment count and save image
        self.image_count += 1
        filename = f"{char.lower()}{self.image_count}.jpg"
        filepath = os.path.join(char_dir, filename)
        
        # Save the image (using original_frame without green border)
        cv2.imwrite(filepath, self.original_frame)
        
        # Update counter display
        self.counter_label.setText(f"Current Count: {self.image_count}")
        
        # Show notification
        self.statusBar().showMessage(f"Photo saved: {filepath}", 2000)

    def reset_count(self):
        # Confirm reset with the user
        reply = QMessageBox.question(
            self, 
            "Reset Count Confirmation",
            "Are you sure you want to reset the count? This is useful when changing to a new letter.",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.image_count = 0
            self.counter_label.setText("Current Count: 0")
            self.statusBar().showMessage("Counter has been reset", 2000)

    def toggle_auto_photo(self):
        if not self.auto_active:
            self.start_auto_photo()
        else:
            self.stop_auto_photo()

    def start_auto_photo(self):
        char = self.char_input.text()
        if not char or not char.isalpha():
            QMessageBox.warning(self, "Warning", "Please enter a valid letter in the Label Character field.")
            return
            
        self.auto_active = True
        self.auto_button.setText("Stop Auto Photos")
        
        # Start progress timer (updates every 10ms)
        self.auto_timer.start(10)
        
        # Start photo timer (takes photo every 1000ms = 1s)
        self.photo_timer.start(1000)
        
        self.progress_value = 0
        self.progress_bar.setValue(0)

    def stop_auto_photo(self):
        self.auto_active = False
        self.auto_button.setText("Start Auto Photos")
        self.auto_timer.stop()
        self.photo_timer.stop()
        self.progress_bar.setValue(0)

    def update_progress(self):
        if self.auto_active:
            self.progress_value = (self.progress_value + 1) % 101
            self.progress_bar.setValue(self.progress_value)

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoApp()
    window.show()
    sys.exit(app.exec_())