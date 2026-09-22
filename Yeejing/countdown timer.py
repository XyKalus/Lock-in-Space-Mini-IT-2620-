import sys
import os

from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QSpinBox,QVBoxLayout,QHBoxLayout,QLineEdit
from PyQt6.QtCore import QTimer,Qt,QRectF,QUrl,QSize
from PyQt6.QtGui import QPainter,QColor,QPen,QFont,QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALARM_FILE = os.path.join(BASE_DIR,"alarm.mp3")

class CircularTimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.progress = 1.0
        self.display_time = "00:00:00"
        self.setMinimumSize(250,250)

    def set_data(self,progress,text):
        self.progress = max(0.0,min(1.0, progress))
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
            t = ((1.0 - self.progress) / 0.5)
            r = int(255 * t)
            g = 255
            b = 0

        else:
            t = self.progress / 0.5
            r = 255
            g = int(255 * t)
            b = 0

        dynamic_color = QColor(r, g, b)

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

class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(1100,800))
        self.setGeometry(250,25,1100,800)

        self.total_seconds = 0
        self.remaining_seconds = 0

        self.timer_running = False
        self.alarm_playing = False
        self.timer_finished = False

        self.timer = QTimer(self)

        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.countdown)
        self.setup_audio()
        self.setup_ui()
        self.set_time()

    def setup_audio(self):
        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(1.0)
        self.player = QMediaPlayer(self)
          
        self.player.setAudioOutput(self.audio_output)
            
        if os.path.exists(ALARM_FILE):
            self.player.setSource(QUrl.fromLocalFile(ALARM_FILE))

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

       
        
        name_label = QLabel("Timer Name : ")
        

        name_label.setObjectName("fieldLabel")
        main_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.name_input)
        time_label = QLabel("Enter Time : ")
        time_label.setObjectName("fieldLabel")

        main_layout.addWidget(time_label)

        time_layout = QHBoxLayout()
        time_layout.setSpacing(15)

        # HOURS
        hours_layout = QVBoxLayout()
        hours_label = QLabel("Hours")
        hours_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0,23)
        self.hours_spin.setValue(0)
        self.hours_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hours_layout.addWidget(hours_label)
        hours_layout.addWidget(self.hours_spin)

        #MINUTES
        minutes_layout = QVBoxLayout()
        minutes_label = QLabel("Minutes")
        minutes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0,59)
        self.minutes_spin.setValue(0)
        self.minutes_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        minutes_layout.addWidget(minutes_label)
        minutes_layout.addWidget(self.minutes_spin)
         
        #SECONDS
        seconds_layout = QVBoxLayout()
        seconds_label = QLabel( "Seconds")
        seconds_label.setAlignment( Qt.AlignmentFlag.AlignCenter)
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0,59)
        self.seconds_spin.setValue(0)
        self.seconds_spin.setAlignment( Qt.AlignmentFlag.AlignCenter)
        seconds_layout.addWidget(seconds_label)
        seconds_layout.addWidget(self.seconds_spin)

        time_layout.addLayout(hours_layout)
        time_layout.addLayout(minutes_layout)
        time_layout.addLayout(seconds_layout)
        main_layout.addLayout(time_layout)
        

        self.timer_name_label = QLabel("")
        self.timer_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_name_label.setObjectName("timerName")
        main_layout.addWidget( self.timer_name_label)

        # Circular timer
        self.circle_timer = CircularTimerWidget( self)
        main_layout.addWidget(self.circle_timer,1)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
          
        self.start_button = QPushButton("Start")
        self.reset_button = QPushButton("Reset")

        self.start_button.setObjectName("startButton")
        self.reset_button.setObjectName("resetButton")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)

        # Connections
        self.start_button.clicked.connect(self.start_stop)
        self.reset_button.clicked.connect(self.reset)
        self.hours_spin.valueChanged.connect(self.set_time)
        self.minutes_spin.valueChanged.connect( self.set_time)
        self.seconds_spin.valueChanged.connect(self.set_time)
        self.name_input.textChanged.connect(self.update_name)

        # Style
        self.setStyleSheet(
            """
            QWidget {
                background: #181818;
                color: #F5F5F5;
                
        
            }

            #title {
                
                font-weight: bold;
                margin-bottom: 5px;
            }

            #fieldLabel {
                font-size: 30px;
                font-weight: bold;
            }

            #timerName {
                font-size: 30px;
                font-weight: bold;
                margin-top: 5px;
            }

            QLineEdit {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 10px;
                font-size: 30px;
                font-weight: bold;
            }

            QLineEdit:focus {
                border: 1px solid #777777;
            }

            QSpinBox {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
                font-size: 20px;
                font-weight: bold;
                min-width: 110px;
            }

            QSpinBox:focus {
                border: 1px solid #777777;
            }

            QPushButton {
                min-width: 150px;
                padding: 14px;
                border-radius: 8px;
                font-size: 17px;
                font-weight: bold;
            }

            #startButton {
                background: #3A3A3A;
            }

            #resetButton {
                background: #292929;
            }

            #startButton:hover,
            #resetButton:hover {
                background: #4A4A4A;
            }
            """
        )

    def update_name(self):
        name = self.name_input.text().strip()
        if not name:
            self.timer_name_label.setText("")
        else:
            self.timer_name_label.setText(name)
            
    def set_time(self):
        if self.timer_running:
            return
        
        if self.alarm_playing:
            return

        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        seconds = self.seconds_spin.value()
        self.total_seconds = ( hours * 3600+ minutes * 60+ seconds)
        self.remaining_seconds = ( self.total_seconds)
        self.update_display()

    def format_time(self):
        hours = ( self.remaining_seconds// 3600)
        minutes = (self.remaining_seconds% 3600) // 60
        seconds = (self.remaining_seconds% 60)
        
        return (f"{hours:02d}: "f"{minutes:02d}: "f"{seconds:02d}")
        
    def update_display(self):
        text = self.format_time()
        if self.total_seconds > 0:
            progress = (self.remaining_seconds  / self.total_seconds)

        else:
            progress = 0
        self.circle_timer.set_data( progress, text)

    def start_stop(self):
        if self.alarm_playing:
            self.stop_alarm()
            return

        if self.timer_finished:
            return

        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.start_button.setText("Start")
            return

        if self.remaining_seconds <= 0:
            self.set_time()
            if self.remaining_seconds <= 0:
                return

        self.timer.start()
        self.timer_running = True
        self.start_button.setText("Pause")

    def countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.timer_running = False
            self.timer_finished = True
            self.start_alarm()

    def start_alarm(self):
        self.alarm_playing = True
        self.start_button.setText("Stop Alarm")
        self.reset_button.setEnabled(False)
      
        if os.path.exists(ALARM_FILE):
            self.player.setPosition(0)
            self.player.play()

    def stop_alarm(self):
        self.player.stop()
        self.alarm_playing = False
        self.reset_button.setEnabled(True)
        self.start_button.setText("Start")
          
    def reset(self):
        if self.alarm_playing:
            return

        self.timer.stop()
        self.timer_running = False
        self.timer_finished = False
        self.remaining_seconds = (self.total_seconds)
        self.start_button.setText("Start")
        self.reset_button.setEnabled(True)
     
        # Clear timer name only when Reset is pressed
        self.name_input.clear()
        self.timer_name_label.setText("")
        self.update_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "Cave-Story.ttf"))

    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family,50))

    window = CountdownTimer()
    window.show()
    sys.exit(app.exec())