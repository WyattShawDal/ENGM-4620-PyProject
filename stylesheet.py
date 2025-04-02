'''File name: sheetstyle.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: Where the theme style sheets are stored
'''
Light = """
QWidget#widget{
    background-color:qlineargradient(spread:pad, x1:0.426, y1:0.386364, x2:1, y2:1, stop:0.0371429 rgba(204, 77, 61, 200), stop:1 rgba(204, 77, 61, 255));
}

QPushButton {
    background-color: white;
    border: 1px solid #e6e6e6;
    color: #aa3e32;
    font-family: "Terminal";
    padding: 5px;
}

QPushButton:hover {
    background-color: #f0f0f0;
    border: 1px solid #d4d4d4;
}

QPushButton:pressed {
    background-color: #e6e6e6;
}

QLabel {
    font-family: "Terminal";
    color: white;
}

QComboBox {
    background-color: white;
    border: 1px solid #e6e6e6;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    color: #aa3e32;
    font-family: "Terminal";
}

QComboBox:hover {
    border: 1px solid #d4d4d4;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left: 1px solid #e6e6e6;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #e6e6e6;
    color: #aa3e32;
    selection-background-color: #f0f0f0;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: white;
    border: 1px solid #e6e6e6;
    border-radius: 3px;
    padding: 2px;
    color: #aa3e32;
    font-family: "Terminal";
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #aa3e32;
}

QProgressBar {
    border: 1px solid #e6e6e6;
    border-radius: 5px;
    text-align: center;
    background-color: white;
    height: 20px;
    color: #aa3e32;
    font-family: "Terminal";
}
QProgressBar::chunk {
    background-color: #cc4d3d;
    border-radius: 5px;
}
"""

Sunset = """
QWidget#widget{
background-color:qlineargradient(spread:pad, x1:0.426, y1:0.386364, x2:1, y2:1, stop:0.0371429 rgba(10, 0, 42, 255), stop:1 rgba(117, 58, 58, 255));}

QPushButton {
    background-color: transparent;
    border: 1px solid #fff6ab;
    color: #fff6ab;
    font-family: "Terminal";
    padding: 5px;
}

QPushButton:hover {
    background-color: rgba(255, 246, 171, 0.05);
}

QPushButton:pressed {
    background-color: rgba(255, 246, 171, 0.1);
}

/* Labels - terminal font and light yellow text */
QLabel {
    font-family: "Terminal";
    color: #fff6ab;
}

QComboBox {
    background-color: rgba(50, 50, 50, 0.2);
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    color: #fff6ab;
    font-family: "Terminal";
}

QComboBox:hover {
    border: 1px solid #fff6ab;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left: 1px solid #555555;
}

QComboBox QAbstractItemView {
    background-color: rgba(50, 50, 50, 0.3);
    border: 1px solid #555555;
    color: #fff6ab;
    selection-background-color: rgba(255, 246, 171, 0.15);
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: rgba(50, 50, 50, 0.2);
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 2px;
    color: #fff6ab;
    font-family: "Terminal";
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #fff6ab;
}

QProgressBar {
    border: 1px solid #555555;
    border-radius: 5px;
    text-align: center;
    background-color: rgba(50, 50, 50, 0.2);
    height: 20px;
    color: #fff6ab;
    font-family: "Terminal";
}
QProgressBar::chunk {
    background-color: rgba(255, 176, 89, 0.8);
    border-radius: 5px;
}
"""

Dark = """
QWidget#widget {
    background-color: qlineargradient(spread:pad, x1:0.426, y1:0.386364, x2:1, y2:1, 
        stop:0.037 rgba(15, 15, 15, 255), 
        stop:1 rgba(35, 35, 35, 255));
}

QPushButton {
    background-color: rgb(30, 30, 30); /* Even darker button */
    border: 1px solid rgb(90, 90, 90);
    color: rgb(255, 70, 50); /* Bright red text */
    font-family: "Terminal";
    padding: 5px;
}

QPushButton:hover {
    background-color: rgb(50, 50, 50);
    border: 1px solid rgb(120, 120, 120);
}

QPushButton:pressed {
    background-color: rgb(70, 70, 70);
}

QLabel {
    font-family: "Terminal";
    color: rgb(235, 235, 235); /* Slightly brighter white */
}

QLabel#label_7 {
    color: rgb(255, 90, 70); /* Brighter red to pop */
}

QComboBox {
    background-color: rgb(25, 25, 25); /* Darker dropdown */
    border: 1px solid rgb(90, 90, 90);
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    color: rgb(255, 70, 50); /* Bright red text */
    font-family: "Terminal";
}

QComboBox:hover {
    border: 1px solid rgb(120, 120, 120);
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left: 1px solid rgb(90, 90, 90);
}

QComboBox QAbstractItemView {
    background-color: rgb(20, 20, 20); /* Even darker dropdown */
    border: 1px solid rgb(90, 90, 90);
    color: rgb(255, 70, 50); /* Bright red text */
    selection-background-color: rgb(80, 80, 80);
    selection-color: rgb(255, 120, 100);
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: rgb(20, 20, 20); /* Deep dark input fields */
    border: 1px solid rgb(90, 90, 90);
    border-radius: 3px;
    padding: 2px;
    color: rgb(255, 70, 50); /* Bright red text */
    font-family: "Terminal";
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid rgb(255, 90, 70); /* More vibrant red when focused */
}

QProgressBar {
    border: 1px solid rgb(90, 90, 90);
    border-radius: 5px;
    text-align: center;
    background-color: rgb(20, 20, 20);
    height: 20px;
    color: rgb(235, 235, 235);
    font-family: "Terminal";
}
QProgressBar::chunk {
    background-color: rgb(255, 70, 50);
    border-radius: 5px;
}
"""