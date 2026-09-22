from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout,QTableWidget, QTableWidgetItem, QPushButton,QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class HistoryPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.show_statistics = controller
        self.setup_history_page()

    def setup_history_page(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30,20,30,20)
        main_layout.setSpacing(15)

        # back btn 
        back_btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.setFixedSize(100,35)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Connect Back button
        self.back_btn.clicked.connect(self.show_statistics)

        self.back_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #4285F4;
                border-radius: 8px;
                font-weight: bold;
            }
        """)

        back_btn_layout.addWidget(self.back_btn)
        back_btn_layout.addStretch()
        main_layout.addLayout(back_btn_layout)
        
        # History title
        self.title = QLabel("Study History")

        self.title.setFont(
            QFont(
                "Arial",
                28,
                QFont.Weight.Bold
            )
        )

        self.title.setAlignment( Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title)
          

        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Name",
            "Date",
            "Start Time",
            "End Time",
            "Duration",
            "Status"
        ])

        sessions_data = []

        self.table.setRowCount(
            len(sessions_data)
        )

        for row, data in enumerate(
            sessions_data
        ):
            for column, value in enumerate(
                data
            ):
                item = QTableWidgetItem(
                    value
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.table.setMinimumHeight(
            180
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #EEEEEE;
                border-radius: 10px;
                gridline-color: #EEEEEE;
            }

            QHeaderView::section {
                background: #F8F8F8;
                border: none;
                padding: 10px;
                font-weight: bold;
                color: #444444;
            }

            QTableWidget::item {
                padding: 10px;
            }
        """)

        main_layout.addWidget(
            self.table
        )

        main_layout.addStretch()

        self.setLayout(
            main_layout
        )