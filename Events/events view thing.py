"""
Standalone event viewer: a QComboBox to pick which category file to look at,
and a QListWidget that displays that file's events.

Meant to be dropped into another file/window -- e.g.:

    from event_viewer import EventViewerWidget
    self.viewer = EventViewerWidget()
    some_layout.addWidget(self.viewer)

If the folder isn't at the default location relative to where the program
is launched from, pass it explicitly:

    self.viewer = EventViewerWidget(events_folder=eventsfolder)

(reusing the same `eventsfolder` variable your other file already builds,
so both windows are guaranteed to be pointed at the same folder).
"""

import json
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QListWidget


class EventViewerWidget(QWidget):
    def __init__(self, events_folder: Path = None, parent=None):
        super().__init__(parent)

        # Falls back to the same Path.cwd()/"Events" convention used elsewhere,
        # but accepts an explicit folder so both windows can share ONE source
        # of truth instead of each independently guessing where it is.
        self.eventsfolder = events_folder if events_folder is not None else Path.cwd() / "Events"

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.viewer_dropdown = QComboBox()
        self.viewer_dropdown.currentIndexChanged.connect(self.load_events_into_list)

        self.event_list_widget = QListWidget()

        layout.addWidget(self.viewer_dropdown)
        layout.addWidget(self.event_list_widget)

        self.setLayout(layout)

        self.refresh_dropdown()

    def refresh_dropdown(self):
        """
        Re-scans the folder for .json files and repopulates the dropdown.
        Call this any time files might have been added/renamed/deleted
        elsewhere -- e.g. when this widget/page becomes visible again,
        since it won't know about changes made in a different window
        on its own.
        """
        names = [f.stem for f in self.eventsfolder.glob("*.json")]

        self.viewer_dropdown.blockSignals(True)
        self.viewer_dropdown.clear()
        self.viewer_dropdown.addItems(names)
        self.viewer_dropdown.blockSignals(False)

        self.load_events_into_list()   # populate for whatever ended up selected

    def load_events_into_list(self):
        self.event_list_widget.clear()

        selected_name = self.viewer_dropdown.currentText()
        if not selected_name:
            return

        file_path = self.eventsfolder / f"{selected_name}.json"
        if not file_path.exists():
            return

        with open(file_path, 'r', encoding="utf-8") as f:
            events = json.load(f)   # bare list format: [ {...}, {...} ]

        for event in events:
            name = event.get("event_name", "(untitled)")
            date_str = event.get("event_date", "?")
            time_str = event.get("event_time", "?")
            display_text = f"{name} — {date_str} {time_str}"

            recurrence = event.get("recurrence", "none")
            if recurrence != "none":
                end = event.get("recurrence_end")
                if end:
                    display_text += f" (repeats {recurrence}, until {end})"
                else:
                    display_text += f" (repeats {recurrence})"

            self.event_list_widget.addItem(display_text)