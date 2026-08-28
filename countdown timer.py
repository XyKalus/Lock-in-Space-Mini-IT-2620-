import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

class CircularTimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 1.0
        self.display_time = "00:00:00"
        self.setMinimumSize(250, 250)

    def set_data(self, progress, text):
        self.progress = max(0.0, min(1.0, progress))
        self.display_time = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 20
        rect = QRectF((width - size) / 2, (height - size) / 2, size, size)

        r = 255
        g = int(200 * self.progress)
        b = int(50 * self.progress)
        dynamic_color = QColor(r, g, b)

        pen_bg = QPen(QColor(230, 230, 230), 12)
        painter.setPen(pen_bg)
        painter.drawEllipse(rect)

        pen_progress = QPen(dynamic_color, 12, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen_progress)
        angle = int(360 * self.progress * 16)
        painter.drawArc(rect, 90 * 16, -angle)

        painter.setPen(QColor(50, 50, 50))
        painter.setFont(QFont("Comic Sans MS", 26, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, self.display_time)

class Timer(QWidget):
    def __init__(self):
        super().__init__()

        self.remaining_seconds = 0
        self.total_seconds = 0

        self.minutesLabel = QLabel("Minutes:", self)
        self.minutesSpinBox = QSpinBox(self)
        self.circle_timer = CircularTimerWidget(self)

        self.start_button = QPushButton("Start", self)
        self.reset_button = QPushButton("Reset", self)

        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CountDown Timer")
        self.move(700, 200)
        self.setFixedSize(500, 500)
        self.minutesSpinBox.setRange(1, 1440)

        hbox = QHBoxLayout()
        hbox.addWidget(self.minutesLabel)
        hbox.addWidget(self.minutesSpinBox)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.circle_timer, alignment=Qt.AlignCenter)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.reset_button)

        self.setLayout(vbox)

        self.setStyleSheet("""
            QSpinBox{
                font-weight: bold;
                font-family: Arial;
                font-size: 40px;
            }
            QLabel{
                font-weight: bold;
                font-size: 50px;
                font-family: Arial;
            }
            QPushButton{
                font-weight: bold;
                padding: 15px;
                font-size:25px;
                font-family: Times New Roman;
            }
        """)

        self.start_button.clicked.connect(self.start_timer)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.countdown)
        self.minutesSpinBox.valueChanged.connect(self.set_minutes)
        self.set_minutes(self.minutesSpinBox.value())

    def start_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Start")
        else:
            if self.remaining_seconds > 0:
                self.timer.start(1000)
                self.start_button.setText("Stop")

    def set_minutes(self, minutes):
        if not self.timer.isActive():
            self.remaining_seconds = minutes * 60
            self.total_seconds = self.remaining_seconds
            self.update_display()

    def reset(self):
        self.timer.stop()
        self.start_button.setText("Start")
        minutes = self.minutesSpinBox.value()
        self.remaining_seconds = minutes * 60
        self.total_seconds = self.remaining_seconds
        self.update_display()

    def countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1

        self.update_display()
        if self.remaining_seconds == 0:
            self.timer.stop()
            self.start_button.setText("Start")

    def update_display(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        text = f"{hours:02}:{minutes:02}:{seconds:02}"

        progress = (self.remaining_seconds / self.total_seconds) if self.total_seconds > 0 else 0
        self.circle_timer.set_data(progress, text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer = Timer()
    timer.show()
    sys.exit(app.exec_())