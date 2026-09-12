import sys
import json
import os
from datetime import date

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QRectF,QUrl
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput


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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 20
        rect = QRectF((width - size) / 2, (height - size) / 2, size, size)

        if self.progress >= 0.5:
            t = ((1.0 -self.progress)/0.5)
            r = int(255 * t)
            g = 255
            b = 0

        else:
            t = self.progress / 0.5
            r = 255
            g = int(255 * t)
            b = 0

        dynamic_color = QColor(r,g,b)

        pen_bg = QPen(QColor(230, 230, 230), 12)
        painter.setPen(pen_bg)
        painter.drawEllipse(rect)

        pen_progress = QPen(dynamic_color, 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_progress)
        angle = int(360 * self.progress * 16)
        painter.drawArc(rect, 90 * 16, -angle)

        painter.setPen(QColor(50, 50, 50))
        painter.setFont(QFont("Comic Sans MS", 26, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.display_time)

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

        
        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)

        self.player.setAudioOutput(self.audio_output)   
        audio_file = "alarm.mp3"
        
        self.player.setSource( QUrl.fromLocalFile(audio_file))
        

        self.alarm_playing = False
        self.timer = QTimer(self)

        self.initUI()

    def load_total_time(self):
        if not os.path.exists("study_progress.json"):
            return{}

        try:
            with open("study_progress.json","r") as file:
                return json.load(file)

        except (json.JSONDecodeError,IOError):
            return {}

    def save_total_time(self,seconds):
        if seconds <= 0:
            return

        today = str(date.today())

        total_time = self.load_total_time()

        if today not in total_time:
            total_time[today] = 0

        total_time[today] += seconds

        try:
            with open("study_progress.json","w") as file:
                json.dump(total_time,file,indent=4)

        except IOError as error:
            print( "Could not save usage:",error)


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
        vbox.addWidget(self.circle_timer, Qt.AlignmentFlag.AlignVCenter)
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
        if self.alarm_playing:
            self.player.stop()
            self.alarm_playing = False
            self.start_button.setText("Start")

            return

        if self.timer.isActive():
            self.timer.stop()
            self.used_seconds = 0
            self.start_button.setText("Start")

            return
        
        if self.remaining_seconds > 0:
            self.timer.start(1000)
            self.start_button.setText("Stop")

    def set_minutes(self, minutes):
        if not self.timer.isActive():
            self.remaining_seconds = minutes * 60
            self.total_seconds = self.remaining_seconds
            self.used_seconds = 0
            self.player.stop()
            self.alarm_playing = False
            self.start_button.setText("Start")
            self.update_display()

    def reset(self):
        self.timer.stop()
        self.start_button.setText("Start")
        minutes = self.minutesSpinBox.value()
        self.remaining_seconds = minutes * 60
        self.total_seconds = self.remaining_seconds
        self.used_seconds = 0
        self.update_display()

    def countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.used_seconds += 1
            self.save_total_time(1)

        self.update_display()
        if self.remaining_seconds == 0:
            self.timer.stop()
            self.play_audio()
            self.start_button.setText("Stop")

    def play_audio(self):
        if not self.alarm_playing:
            self.alarm_playing = True
            self.player.play()

    def update_display(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        text = f"{hours:02}:{minutes:02}:{seconds:02}"

        if self.total_seconds > 0:
            progress = (self.remaining_seconds/ self.total_seconds)

        else:
            progress = 0

        progress = max(0.0,min(1.0, progress))
        self.circle_timer.set_data(progress, text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer = Timer()
    timer.show()
    sys.exit(app.exec())