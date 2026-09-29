import os
import json

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView
)

from PyQt6.QtCore import (
    Qt,
    QTimer,
    QRect
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROGRESS_FILE = os.path.realpath(
    os.path.join(
        BASE_DIR,
        "study_progress.json"
    )
)


print("========================================")
print("[History] JSON FILE:")
print(PROGRESS_FILE)
print("========================================")


class HistoryPage(QWidget):

    MIN_ROW_HEIGHT = 45
    MAX_NAME_LINES = 3


    def __init__(self,controller):

        super().__init__()

        self.show_statistics = controller

        self.full_names = []

        self.setup_history_page()

        self.load_history()


    def setup_history_page(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            30,
            20,
            30,
            20
        )


        back_btn_layout = QHBoxLayout()


        self.back_btn = QPushButton(
            "Back"
        )

        self.back_btn.setFixedSize(
            100,
            35
        )

        self.back_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.back_btn.clicked.connect(
            self.show_statistics
        )


        self.back_btn.setStyleSheet(
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


        back_btn_layout.addWidget(
            self.back_btn
        )

        back_btn_layout.addStretch()

        main_layout.addLayout(
            back_btn_layout
        )


        self.title = QLabel(
            "Study History"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        self.title.setStyleSheet(
            """
            QLabel {
                font-size: 30px;
                font-weight: bold;
            }
            """
        )


        main_layout.addWidget(
            self.title
        )


        self.table = QTableWidget()

        self.table.setColumnCount(
            7
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Name",
                "Date",
                "Start Time",
                "End Time",
                "Duration",
                "Status",
                "Coin Earned"
            ]
        )


        self.table.setMinimumHeight(
            300
        )


        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )


        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setWordWrap(
            True
        )

        self.table.setTextElideMode(
            Qt.TextElideMode.ElideNone
        )


        self.table.verticalHeader().setDefaultSectionSize(
            self.MIN_ROW_HEIGHT
        )


        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch
        )


        for column in range(1,7):

            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.Stretch
            )


        header.setMinimumSectionSize(
            80
        )


        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )


        self.table.setStyleSheet(
            """
            QTableWidget {
                background: white;
                border: 1px solid #EEEEEE;
                border-radius: 10px;
                gridline-color: #EEEEEE;
                color: #333333;
            }

            QHeaderView::section {
                background: #F8F8F8;
                border: none;
                padding: 10px;
                font-weight: bold;
                color: #444444;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QTableWidget::item:selected {
                background: #EAF2FF;
                color: #333333;
            }
            """
        )


        main_layout.addWidget(
            self.table,
            1
        )


        self.setLayout(
            main_layout
        )


    def format_duration(self,duration):

        if isinstance(
            duration,
            int
        ):

            total_seconds = duration


        else:

            duration = str(
                duration
            )


            try:

                parts = duration.split(":")


                # HH:MM:SS

                if len(parts) == 3:

                    hours = int(
                        parts[0]
                    )

                    minutes = int(
                        parts[1]
                    )

                    seconds = int(
                        parts[2]
                    )


                    total_seconds = (
                        hours * 3600
                        + minutes * 60
                        + seconds
                    )


                else:

                    total_seconds = int(
                        duration
                    )


            except ValueError:

                return duration


        hours = (
            total_seconds // 3600
        )

        minutes = (
            total_seconds % 3600
        ) // 60

        seconds = (
            total_seconds % 60
        )


        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )


    def wrap_text(self,text):

        return "\u200b".join(
            text
        )


    def name_fits(self,text,width):

        metrics = (
            self.table.fontMetrics()
        )


        rect = metrics.boundingRect(
            QRect(
                0,
                0,
                width,
                100000
            ),
            Qt.TextFlag.TextWordWrap.value,
            text
        )


        max_height = (
            metrics.lineSpacing()
            * self.MAX_NAME_LINES
        )


        return (
            rect.height()
            <= max_height
        )


    def fit_name(self,name):

        width = (
            self.table.columnWidth(0)
            - 24
        )


        full_text = self.wrap_text(
            name
        )


        if width <= 0:

            return full_text


        if self.name_fits(
            full_text,
            width
        ):

            return full_text


        low = 0

        high = len(name)


        while low < high:

            mid = (
                low + high + 1
            ) // 2


            candidate = (
                self.wrap_text(
                    name[:mid].rstrip()
                )
                + "..."
            )


            if self.name_fits(
                candidate,
                width
            ):

                low = mid

            else:

                high = mid - 1


        return (
            self.wrap_text(
                name[:low].rstrip()
            )
            + "..."
        )


    def refit_names(self):

        for row,name in enumerate(
            self.full_names
        ):

            item = self.table.item(
                row,
                0
            )


            if item is not None:

                item.setText(
                    self.fit_name(name)
                )

                item.setToolTip(
                    name
                )


    def adjust_row_heights(self):

        self.refit_names()


        max_height = (
            self.table.fontMetrics().lineSpacing()
            * self.MAX_NAME_LINES
            + 30
        )


        for row in range(
            self.table.rowCount()
        ):

            self.table.resizeRowToContents(
                row
            )


            height = self.table.rowHeight(
                row
            )


            height = max(
                self.MIN_ROW_HEIGHT,
                min(
                    height,
                    max_height
                )
            )


            self.table.setRowHeight(
                row,
                height
            )


    def resizeEvent(self,event):

        super().resizeEvent(
            event
        )


        QTimer.singleShot(
            0,
            self.adjust_row_heights
        )


    def showEvent(self,event):

        super().showEvent(
            event
        )

        # IMPORTANT:
        # Read JSON again every time
        # History page is opened.

        self.load_history()


        QTimer.singleShot(
            0,
            self.adjust_row_heights
        )


    def load_history(self):

        print("========================================")
        print("[History] Reading JSON from:")
        print(PROGRESS_FILE)
        print("========================================")


        self.table.setRowCount(
            0
        )

        self.full_names = []


        if not os.path.exists(
            PROGRESS_FILE
        ):

            print(
                "[History] study_progress.json not found."
            )

            return


        try:

            with open(
                PROGRESS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                sessions_data = json.load(
                    file
                )


            print(
                "[History] Records loaded:",
                len(sessions_data)
            )


        except (
            json.JSONDecodeError,
            OSError
        ) as e:

            print(
                f"[History] Could not read JSON: {e}"
            )

            return


        if not isinstance(
            sessions_data,
            list
        ):

            print(
                "[History] JSON data is not a list."
            )

            return


        self.table.setRowCount(
            len(sessions_data)
        )


        for row,data in enumerate(
            sessions_data
        ):

            name = str(
                data.get(
                    "description",
                    "(no description)"
                )
            )


            self.full_names.append(
                name
            )


            start_time = str(
                data.get(
                    "start_time",
                    ""
                )
            )


            if " " in start_time:

                date_text,start_text = (
                    start_time.split(
                        " ",
                        1
                    )
                )

            else:

                date_text = start_time

                start_text = ""


            end_time = str(
                data.get(
                    "end_time",
                    ""
                )
            )


            if " " in end_time:

                _,end_text = (
                    end_time.split(
                        " ",
                        1
                    )
                )

            else:

                end_text = end_time


            duration_text = (
                self.format_duration(
                    data.get(
                        "duration",
                        ""
                    )
                )
            )


            status = str(
                data.get(
                    "status",
                    ""
                )
            )


            coin_earned = str(
                data.get(
                    "coin_earned",
                    0
                )
            )


            row_data = [

                name,

                str(
                    date_text
                ),

                str(
                    start_text
                ),

                str(
                    end_text
                ),

                str(
                    duration_text
                ),

                status,

                coin_earned
            ]


            for column,value in enumerate(
                row_data
            ):

                if column == 0:

                    display_value = (
                        self.fit_name(
                            name
                        )
                    )

                else:

                    display_value = value


                item = QTableWidgetItem(
                    display_value
                )


                if column == 0:

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignLeft
                        |
                        Qt.AlignmentFlag.AlignVCenter
                    )

                    item.setToolTip(
                        name
                    )

                else:

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                        |
                        Qt.AlignmentFlag.AlignVCenter
                    )


                self.table.setItem(
                    row,
                    column,
                    item
                )


        self.adjust_row_heights()


    def refresh_history(self):

        self.load_history()