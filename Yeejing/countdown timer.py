import sys
import os
import json
from datetime import datetime

from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QSpinBox,QVBoxLayout,QHBoxLayout,QLineEdit,QFrame
from PyQt6.QtCore import QTimer,Qt,QRectF,QUrl,QSize
from PyQt6.QtGui import QPainter,QColor,QPen,QFont,QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
<<<<<<< HEAD
ALARM_FILE = os.path.join(BASE_DIR, "alarm.mp3")
=======
ALARM_FILE = os.path.join(BASE_DIR,"alarm.mp3")
>>>>>>> lock-in-space/main


class CircularTimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 1.0
        self.display_time = "00:00:00"


    def set_data(self, progress, text):
        self.progress = max( 0.0, min(1.0, progress))
        self.display_time = text
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        size = min(width,height) - 20

        rect = QRectF((width - size) / 2,(height - size) / 2,size,size)

        if self.progress >= 0.5:
            t = ((1.0 - self.progress) / 0.5)

            r = int(255 * t)
            g = 255
            b = 0

        else:
            t = (self.progress/ 0.5)

            r = 255
            g = int(255 * t)
            b = 0

        dynamic_color = QColor(r,g,b)

        pen_bg = QPen(QColor(230, 230, 230),12)

        painter.setPen(pen_bg)
        painter.drawEllipse(rect)
        pen_progress = QPen( dynamic_color,12,  Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_progress)
         
        angle = int(360* self.progress* 16)
        painter.drawArc(rect, 90 * 16,-angle)
        painter.setPen(QColor(50, 50, 50))
        painter.setFont( QFont("Comic Sans MS", 26, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter,self.display_time)
         

class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()

<<<<<<< HEAD
        self.setFixedSize(QSize(1100, 800))
    
        self.setGeometry(250,25,1100,800)
         
=======
>>>>>>> lock-in-space/main
        self.total_seconds = 0
        self.remaining_seconds = 0

        self.timer_running = False
        self.alarm_playing = False
        self.timer_finished = False
        self.timer_started = False

        self.session_start_time = None
        self.session_saved = False

        self.popup_type = None
        self.popup_was_running = False

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.countdown)
   
        self.setup_audio()
        self.setup_ui()
        self.setup_popup()
        self.set_time()

    def format_duration(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        return (f"{hours:02d}:" f"{minutes:02d}:"f"{secs:02d}")
       

    def coin_value_for(self, seconds):
        return seconds // 60


    def save_session(self,description,start_time,end_time,duration,status,coin_earned):
        record = {
            "description":
                description
                if description
                else "(no description)",

            "start_time":
                start_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if start_time
                else "",

            "end_time":
                end_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if end_time
                else "",

            "duration":
                self.format_duration(
                    duration
                ),

            "status":
                status,

            "coin_earned":
                coin_earned
        }

        progress_path = os.path.join( BASE_DIR,"study_progress.json")

        try:
            if os.path.exists(progress_path):
                with open(progress_path,"r") as f:
                    data = json.load(f)

            else:
                data = []

        except (json.JSONDecodeError,OSError) as e:

            print(f"[study_progress] "f"could not read "f"{progress_path}: {e}")
            data = []

        data.append(record)

        try:
            with open(progress_path,"w") as f:
                json.dump(data,f,indent=2)

            print(f"[study_progress] " f"session saved to " f"{progress_path}")
               
        except OSError as e:

            print(f"[study_progress] "f"FAILED to write "f"{progress_path}: {e}")


    def setup_audio(self):
        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(1.0)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.errorOccurred.connect(self.on_player_error)
            
        if os.path.exists(ALARM_FILE):
            self.player.setSource(QUrl.fromLocalFile(ALARM_FILE))

            print(f"[alarm] using sound file: " f"{ALARM_FILE}")

        else:
            print(f"[alarm] WARNING: alarm file not found "f"at {ALARM_FILE}")


    def on_player_error(self,error,error_string):
        print(f"[alarm] QMediaPlayer error: " f"{error_string}")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.quit_button = QPushButton("X")
        self.quit_button.setFixedSize(45,45)
        self.quit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quit_button.setObjectName("quitButton")
        self.quit_button.clicked.connect(self.quit_clicked)
        self.quit_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #4285F4;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #F0F6FF;
            }
            """
        )
        
        top_bar.addWidget(self.quit_button)
         
        main_layout.addLayout(top_bar)

        # DESCRIPTION
        name_label = QLabel("Enter Your Description/Purpose for using timer : ")
        name_label.setObjectName("fieldLabel")
        main_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setAlignment( Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.name_input)

        # TIME 
        time_label = QLabel("Enter Time : ")
        time_label.setObjectName("fieldLabel")
        main_layout.addWidget( time_label)
     
        time_layout = QHBoxLayout()
        time_layout.setSpacing(15)
          
        hours_layout = QVBoxLayout()
        hours_label = QLabel("Hours")
        hours_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0,24)
        self.hours_spin.setValue(0)
        self.hours_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hours_layout.addWidget(hours_label)
        hours_layout.addWidget(self.hours_spin)
         
        minutes_layout = QVBoxLayout()
        minutes_label = QLabel("Minutes")
        minutes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0,59)
        self.minutes_spin.setValue(0)
        self.minutes_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        minutes_layout.addWidget( minutes_label)
        minutes_layout.addWidget(self.minutes_spin)
       
        seconds_layout = QVBoxLayout()
        seconds_label = QLabel("Seconds")
        seconds_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
       
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0,59)
        self.seconds_spin.setValue(0)
        self.seconds_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        seconds_layout.addWidget(seconds_label)
        seconds_layout.addWidget(self.seconds_spin)

        time_layout.addLayout(hours_layout)
        time_layout.addLayout(minutes_layout)
        time_layout.addLayout(seconds_layout)
         
        main_layout.addLayout(time_layout)
     
        self.timer_name_label = QLabel("")
        self.timer_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_name_label.setObjectName("timerName")
         
        self.timer_name_label.setToolTip("")
        
        main_layout.addWidget(self.timer_name_label)

        self.circle_timer = CircularTimerWidget(self)
        self.circle_timer.setFixedSize(300,300)

        main_layout.addWidget(self.circle_timer,0,Qt.AlignmentFlag.AlignCenter)

        # START RESET BTN   
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
         
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
          
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
           
        main_layout.addLayout(button_layout)

        self.start_button.clicked.connect(self.start_stop)
        self.reset_button.clicked.connect(self.reset)

        self.hours_spin.valueChanged.connect(self.set_time)
        self.minutes_spin.valueChanged.connect(self.set_time)
        self.seconds_spin.valueChanged.connect(self.set_time)
       
        self.name_input.textChanged.connect(self.update_name)
   
        self.setStyleSheet(
            """
            #fieldLabel {
                font-size: 40px;
                font-weight: bold;
            }

            QLineEdit {
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
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 20px;
                font-size: 20px;
            }

            #timerName {
                background: transparent;
                font-size: 30px;
                font-weight: bold;
                padding: 5px;
            }

            QToolTip {
                border: 1px solid #555555;
                padding: 8px;
                font-size: 18px;
            }

            #startButton {
                font-size: 30px;
                padding: 15px;
            }

            #resetButton {
                font-size: 30px;
                padding: 15px;
            }

            #quitButton {
                font-size: 20px;
                font-weight: bold;
                border: 1px solid #555555;
                border-radius: 8px;
            }            
            """
        )

    def setup_popup(self):
        self.popup_overlay = QWidget(self)
          
        overlay_layout = QVBoxLayout(self.popup_overlay)
        overlay_layout.setContentsMargins(0,0,0,0)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.popup_card = QFrame(self.popup_overlay)
        self.popup_card.setFixedSize(560,280)
        self.popup_card.setStyleSheet(
            """
            QFrame {
                background:white;
                color :black;
                border: 2px solid #555555;
                border-radius: 18px;
            }
            """
        )

        card_layout = QVBoxLayout(self.popup_card)
        card_layout.setContentsMargins(30,25,30,25)
        card_layout.setSpacing(18)
     

        # POP UP CORFIMATION
        self.popup_title = QLabel()
        self.popup_title.setAlignment( Qt.AlignmentFlag.AlignCenter)
        
        self.popup_title.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
                font-size: 30px;
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(self.popup_title)
            
        self.popup_message = QLabel("")
        self.popup_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.popup_message.setWordWrap(True)
        self.popup_message.setStyleSheet(
            """
            QLabel {
                border: none;
                font-size: 20px;
                color :black;
            }
            """
        )

        card_layout.addWidget(self.popup_message)

        # YES/ NO
        popup_button_layout = QHBoxLayout()
        popup_button_layout.setSpacing(15)

        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        self.yes_button.setFixedHeight(55)
        self.no_button.setFixedHeight(55)

        self.yes_button.setStyleSheet(
            """
            QPushButton {
                color :black;
                border: 1px solid #555555;
                border-radius: 8px;
                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #4A4A4A;
            }
            """
        )
        self.no_button.setStyleSheet(
            """
            QPushButton {
                color :black;
                border: 1px solid #555555;
                border-radius: 8px;
                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #4A4A4A;
            }
            """
        )

        popup_button_layout.addWidget(self.yes_button)
        popup_button_layout.addWidget(self.no_button)

        card_layout.addLayout(popup_button_layout)
        overlay_layout.addWidget(self.popup_card)

        self.yes_button.clicked.connect(self.popup_yes)
        self.no_button.clicked.connect(self.popup_no)

        self.popup_overlay.hide()


    def resizeEvent(self, event):
        if hasattr(self, "popup_overlay"):
            self.popup_overlay.setGeometry(self.rect())

        super().resizeEvent(event)

    # BACK TO MAIN CODE BTN ,NOW PUT FOR QUIT APP TEMPORARILY    

    def quit_clicked(self):
        if self.alarm_playing:
            self.stop_alarm()
            self.close()
            return

        if self.timer_finished:
            self.close()
            return

        if not self.timer_started:
            self.close()
            return

        self.show_confirmation("quit")


    # RESET / QUIT POP UP
    def show_confirmation(self,popup_type):
        self.popup_type = popup_type

        self.popup_was_running = (self.timer_running)

        # STOP TIMER WHEN POP UP CORFIMATION VISIBLE
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.start_button.setText("Start")

        if popup_type == "reset":
            giveup_coins = (self.coin_value_for(self.total_seconds))

            self.popup_title.setText("Reset Timer?")
            self.popup_message.setText(
                "If you reset this timer,you will give up "f"{giveup_coins} coin(s) from this timer.\n\nDo you want to reset?"
            )

        elif popup_type == "quit":
            self.popup_title.setText("Leave Timer?")
            self.popup_message.setText(
                "Your current timer session is not completed.\n\nIf you leave now, this session will be saved as incomplete.\n\nDo you want to quit?"
            )
            
        # SHOW POPUP CORFIMATION
        self.popup_overlay.setGeometry(self.rect())
        self.popup_overlay.raise_()
        self.popup_overlay.show()

    # YES BTN ON RESET / QUIT BTN
    def popup_yes(self):
        popup_type = self.popup_type
        self.popup_overlay.hide()
        self.popup_type = None

        if popup_type == "reset":
            self.perform_reset()

        elif popup_type == "quit":
            self.perform_quit()


    # NO BTN ON RESET / QUIT BTN
    def popup_no(self):
        self.popup_overlay.hide()
        popup_type = self.popup_type
        self.popup_type = None

        if ((popup_type == "reset" or popup_type == "quit")
            and self.popup_was_running and not self.timer_finished and not self.alarm_playing):

            self.timer.start()
            self.timer_running = True
            self.start_button.setText("Pause")

        self.popup_was_running = False

    def update_name(self):
        name = (self.name_input.text().strip())
          
        if not name:
            self.timer_name_label.setText("")
            self.timer_name_label.setToolTip("")

            return

        max_length = 50
        if len(name) > max_length:
            display_name = (name[:max_length]+ "...")

        else:
            display_name = name

        self.timer_name_label.setText(display_name)
        self.timer_name_label.setToolTip(name)
 
    def set_time(self):
        if self.timer_running:
            return

        if self.alarm_playing:
            return

        if self.timer_finished:
            return

        hours = (self.hours_spin.value())
        minutes = (self.minutes_spin.value())
        seconds = (self.seconds_spin.value())
      
        self.total_seconds = (hours * 3600 + minutes * 60 + seconds)
        self.remaining_seconds = (self.total_seconds)
        self.update_display()

    def format_time(self):
        hours = (self.remaining_seconds // 3600)
        minutes = (self.remaining_seconds % 3600 ) // 60
        seconds = (self.remaining_seconds % 60)
        
        return (f"{hours:02d}:" f"{minutes:02d}:" f"{seconds:02d}")

    def update_display(self):
        text = (self.format_time())
        
        if self.total_seconds > 0:
            progress = (self.remaining_seconds / self.total_seconds)
              
        else:
            progress = 0

        self.circle_timer.set_data(progress,text)
    
    #START /STOP/ RESET FUNC
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

        self.name_input.setReadOnly(True)

        if not self.timer_started:
            self.session_start_time = (datetime.now())
            self.session_saved = False
        self.timer_started = True

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

        #AFTER TIMES UP START BTN FUNC
    def start_alarm(self):
        self.alarm_playing = True
        self.start_button.setText("Stop Alarm")
        self.reset_button.setEnabled(False)

        coin = (self.coin_value_for( self.total_seconds))
           
        # SAVE WHEN STATUS COMPLETED
        end_time = datetime.now()
        self.save_session(
            description=
                self.name_input.text().strip(),

            start_time=
                self.session_start_time,

            end_time=
                end_time,

            duration=
                self.total_seconds,

            status=
                "Completed",

            coin_earned=
                coin
        )

        self.session_saved = True

     

        if os.path.exists(ALARM_FILE):
            self.player.setPosition(0)
            self.player.play()

        else:
            print(
                f"[alarm] skipped playback — "
                f"file missing at {ALARM_FILE}"
            )

    def stop_alarm(self):
        self.player.stop()
        self.alarm_playing = False
        self.start_button.setText("Completed")
        self.start_button.setEnabled(False)

        self.reset_button.setEnabled(True)

    def reset(self):
        if self.alarm_playing:
            return

        if self.timer_finished:
            self.perform_reset()
            return


        if not self.timer_started:
            self.perform_reset()

            return

        self.show_confirmation("reset")

    #FOR IMCOMPLETE STATUS,WHEN RESET BEFORE TIMESUP
    def perform_reset(self):

        # SAVE IMCOMPLETE STATUS
        if (self.timer_started and not self.timer_finished and not self.session_saved):
            end_time = datetime.now()

            self.save_session(
                description=
                    self.name_input.text().strip(),

                start_time=
                    self.session_start_time,

                end_time=
                    end_time,

                duration=
                    self.total_seconds,

                status=
                    "Incomplete",

                coin_earned=
                    0
            )

            self.session_saved = True

        # STOP TIMER
        self.timer.stop()
        self.timer_running = False
        self.timer_finished = False
        self.timer_started = False
        self.session_start_time = None
        self.session_saved = False

        # RESET TIMER
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.start_button.setText("Start")
        self.start_button.setEnabled(True)
        self.reset_button.setEnabled(True)
           
        # CLEAR NAME
        self.name_input.clear()
        self.name_input.setReadOnly(False)
        self.timer_name_label.setText("")
        self.timer_name_label.setToolTip("")
           
        # RESET SPINBOX

        self.hours_spin.setValue(0)
        self.minutes_spin.setValue(0)
        self.seconds_spin.setValue(0)

        # UPDATE CIRCLE TIMER
        self.update_display()


    def perform_quit(self):
        if (self.timer_started and not self.timer_finished and not self.session_saved):
            end_time = datetime.now()

            self.save_session(
                description=
                    self.name_input.text().strip(),

                start_time=
                    self.session_start_time,

                end_time=
                    end_time,

                duration=
                    self.total_seconds,

                status=
                    "Incomplete",

                coin_earned=
                    0
            )

            self.session_saved = True

        self.timer.stop()
        self.player.stop()
        self.timer_running = False
        self.alarm_playing = False
        self.close()


    def closeEvent(self, event):
        self.timer.stop()
        self.player.stop()
        event.accept() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font_path = os.path.join( BASE_DIR,"Cave-Story.ttf")
    font_id = ( QFontDatabase.addApplicationFont( font_path))

    if font_id != -1:
        font_family = ( QFontDatabase.applicationFontFamilies(font_id)[0])
        app.setFont( QFont(font_family,30))
        
    window = CountdownTimer()
    window.show()
    sys.exit(app.exec())