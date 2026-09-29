"""Music Player notes
forget"""

from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout,
)


class MusicController:
    """Owns the player. Create ONCE and keep a reference (e.g. self.music)."""

    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.player.setAudioOutput(self.audio_out)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)  # loop background music
        self.audio_out.setVolume(0.5)
        self.track = None

    def play(self, path):
        self.player.setSource(QUrl.fromLocalFile(str(path)))
        self.player.play()
        self.track = Path(path)

    def toggle(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        elif self.track:
            self.player.play()

    def set_volume(self, percent):          # 0-100
        self.audio_out.setVolume(percent / 100)


class MusicDialog(QDialog):
    """The popup. Reads its starting state from the controller."""

    def __init__(self, music, parent=None):
        super().__init__(parent)
        self.music = music
        self.setWindowTitle("Music settings")

        self.track_label = QLabel()
        self.browse_btn = QPushButton("Choose music...")
        self.toggle_btn = QPushButton("Play / Pause")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(int(music.audio_out.volume() * 100))
        self.volume_label = QLabel(f"{self.slider.value()}%")

        vol_row = QHBoxLayout()
        vol_row.addWidget(QLabel("Volume"))
        vol_row.addWidget(self.slider)
        vol_row.addWidget(self.volume_label)

        layout = QVBoxLayout(self)
        layout.addWidget(self.track_label)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.toggle_btn)
        layout.addLayout(vol_row)

        self.browse_btn.clicked.connect(self.browse)
        self.toggle_btn.clicked.connect(music.toggle)
        self.slider.valueChanged.connect(self.on_volume)

        self.update_track_label()

    def browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose audio", "", "Audio files (*.mp3 *.wav *.ogg)"
        )
        if path:                            # empty string if cancelled
            self.music.play(path)
            self.update_track_label()

    def on_volume(self, value):
        self.music.set_volume(value)
        self.volume_label.setText(f"{value}%")

    def update_track_label(self):
        name = self.music.track.name if self.music.track else "None"
        self.track_label.setText(f"Now playing: {name}")


# ---------- how to use it in ANY window ----------
# In your main window's __init__ (once):
#     self.music = MusicController()
#
# Then connect any QPushButton:
#     self.settings_btn.clicked.connect(self.open_music_settings)
#
# And add this method:
#     def open_music_settings(self):
#         MusicDialog(self.music, parent=self).exec()
#
# Every page's button can call that same method.