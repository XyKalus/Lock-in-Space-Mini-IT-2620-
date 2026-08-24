import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QSpinBox,QVBoxLayout
from PyQt5.QtCore import QTimer, Qt

class Timer(QWidget):
    def __init__(self):
        super().__init__()

        self.remaining_seconds = 0

        self.time_label = QLabel("00:00:00", self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)

        self.minutesLabel = QLabel("Minutes:", self)
        self.minutesSpinBox = QSpinBox(self)

        self.timer = QTimer(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("CountDown Timer")

        self.minutesSpinBox.setRange(1, 999)

        vbox = QVBoxLayout()

        vbox.addWidget(self.minutesLabel)
        vbox.addWidget(self.minutesSpinBox)
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.reset_button)
        vbox.addWidget(self.stop_button)

        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)

        # Button signals
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)

        # Timer signal
        self.timer.timeout.connect(self.countdown)

        # SpinBox signal
        self.minutesSpinBox.valueChanged.connect(self.set_minutes)

        # Set initial time
        self.set_minutes(self.minutesSpinBox.value())

    def set_minutes(self, minutes):
        # Convert minutes to seconds
        self.remaining_seconds = minutes * 60

        # Only update the display.
        # Do NOT subtract a second here.
        self.update_display()

    def start(self):
        if self.remaining_seconds > 0:
            self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def reset(self):
        self.timer.stop()

        minutes = self.minutesSpinBox.value()
        self.remaining_seconds = minutes * 60

        self.update_display()

    def countdown(self):
        # Subtract one second every time the QTimer fires
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1

        self.update_display()

        # Stop when countdown reaches zero
        if self.remaining_seconds == 0:
            self.timer.stop()

    def update_display(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60

        self.time_label.setText(
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    timer = Timer()
    timer.show()

    sys.exit(app.exec_())