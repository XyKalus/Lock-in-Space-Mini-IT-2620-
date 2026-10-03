import PyQt6
from PyQt6 import *
from PyQt6.QtMultimedia import *
from PyQt6.QtWidgets import *

class MusicWidget(QWidget):
    def __init__(self):
        super().__init__
        
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
