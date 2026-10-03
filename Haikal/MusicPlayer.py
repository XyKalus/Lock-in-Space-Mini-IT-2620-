# """Music Player notes
# forget"""

# from pathlib import Path

# from PyQt6.QtCore import Qt, QUrl
# from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
# from PyQt6.QtWidgets import (
#     QDialog, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout,
# )


# class MusicController:
#     """Owns the player. Create ONCE and keep a reference (e.g. self.music).""" # < for reference

#     def __init__(self):
#         self.player = QMediaPlayer()
#         self.audio_out = QAudioOutput()
#         self.player.setAudioOutput(self.audio_out)
#         self.player.setLoops(QMediaPlayer.Loops.Infinite)  # loop background music
#         self.audio_out.setVolume(0.5)
#         self.track = None

#     def play(self, path):
#         self.player.setSource(QUrl.fromLocalFile(str(path)))
#         self.player.play()
#         self.track = Path(path)

#     def toggle(self):
#         if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
#             self.player.pause()
#         elif self.track:
#             self.player.play()

#     def set_volume(self, percent):          # 0-100
#         self.audio_out.setVolume(percent / 100)


# class MusicDialog(QDialog):
#     """The popup. Reads its starting state from the controller."""

#     def __init__(self, music, parent=None):
#         super().__init__(parent)
#         self.music = music
#         self.setWindowTitle("Music settings")

#         self.track_label = QLabel()
#         self.browse_btn = QPushButton("Choose music...")
#         self.toggle_btn = QPushButton("Play / Pause")

#         self.slider = QSlider(Qt.Orientation.Horizontal)
#         self.slider.setRange(0, 100)
#         self.slider.setValue(int(music.audio_out.volume() * 100))
#         self.volume_label = QLabel(f"{self.slider.value()}%")

#         vol_row = QHBoxLayout()
#         vol_row.addWidget(QLabel("Volume"))
#         vol_row.addWidget(self.slider)
#         vol_row.addWidget(self.volume_label)

#         layout = QVBoxLayout(self)
#         layout.addWidget(self.track_label)
#         layout.addWidget(self.browse_btn)
#         layout.addWidget(self.toggle_btn)
#         layout.addLayout(vol_row)

#         self.browse_btn.clicked.connect(self.browse)
#         self.toggle_btn.clicked.connect(music.toggle)
#         self.slider.valueChanged.connect(self.on_volume)

#         self.update_track_label()

#     def browse(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Choose audio", "", "Audio files (*.mp3 *.wav *.ogg)"
#         )
#         if path:                            # empty string if cancelled
#             self.music.play(path)
#             self.update_track_label()

#     def on_volume(self, value):
#         self.music.set_volume(value)
#         self.volume_label.setText(f"{value}%")

#     def update_track_label(self):
#         name = self.music.track.name if self.music.track else "None"
#         self.track_label.setText(f"Now playing: {name}")


# # ---------- how to use it in ANY window ----------
# # In your main window's __init__ (once):
# #     self.music = MusicController()
# #
# # Then connect any QPushButton:
# #     self.settings_btn.clicked.connect(self.open_music_settings)
# #
# # And add this method:
# #     def open_music_settings(self):
# #         MusicDialog(self.music, parent=self).exec()
# #
# # Every page's button can call that same method.


from pathlib import Path

from PyQt6.QtCore import Qt, QUrl, QSettings
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout,
)


class MusicController:
    """Owns the player and the per-page track map. Create ONCE (e.g. self.music)."""

    def __init__(self):
        self.settings = QSettings("YourOrgName", "YourAppName")

        self.player = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.player.setAudioOutput(self.audio_out)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)

        volume = self.settings.value("volume", 50, type=int)
        self.audio_out.setVolume(volume / 100)

        self.track = None            # Path currently playing
        self.page_tracks = {}        # {page_index: path_str}
        self.current_page = 0

    # --- called by MainWindow when QStackedWidget changes page ---
    def on_page_changed(self, index):
        self.current_page = index
        track = self.page_tracks.get(index)
        if track is None or track == str(self.track):
            return                   # nothing assigned to this page, or same song: keep playing
        self.play(track)

    # --- assign a track to whichever page is currently showing ---
    def assign_to_current_page(self, path):
        self.page_tracks[self.current_page] = str(path)
        self.play(path)

    def play(self, path):
        self.player.setSource(QUrl.fromLocalFile(str(path)))
        self.player.play()
        self.track = Path(path)
        self.settings.setValue(f"track_page_{self.current_page}", str(path))

    def toggle(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        elif self.track:
            self.player.play()

    def set_volume(self, percent):
        self.audio_out.setVolume(percent / 100)
        self.settings.setValue("volume", percent)

    def load_saved_tracks(self, page_count):
        """Call once at startup to restore page_tracks from QSettings."""
        for i in range(page_count):
            saved = self.settings.value(f"track_page_{i}", "", type=str)
            if saved:
                self.page_tracks[i] = saved


class MusicDialog(QDialog):
    """Popup. Whatever is chosen here applies to the CURRENTLY ACTIVE page."""

    def __init__(self, music, parent=None):
        super().__init__(parent)
        self.music = music
        self.setWindowTitle("Music settings")

        self.track_label = QLabel()
        self.browse_btn = QPushButton("Choose music for this page...")
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
        if path:
            self.music.assign_to_current_page(path)
            self.update_track_label()

    def on_volume(self, value):
        self.music.set_volume(value)
        self.volume_label.setText(f"{value}%")

    def update_track_label(self):
        name = self.music.track.name if self.music.track else "None"
        self.track_label.setText(f"Page {self.music.current_page} now playing: {name}")


# ---------- how to use it in your MainWindow ----------
# In __init__, AFTER your QStackedWidget (self.stack) is built with all pages added:
#
#     self.music = MusicController()
#     self.music.load_saved_tracks(self.stack.count())
#     self.stack.currentChanged.connect(self.music.on_page_changed)
#     self.music.on_page_changed(self.stack.currentIndex())   # play the startup page, if saved
#
# Any QPushButton, on any page, opens the SAME dialog:
#     def open_music_settings(self):
#         MusicDialog(self.music, parent=self).exec()
#
# Picking a file in the dialog now assigns it to whatever page is on screen
# at that moment, not globally.