import sys
from datetime import date, timedelta

from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QHBoxLayout,QFrame,QPushButton,QStackedWidget,QSizePolicy
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont

from history_page import HistoryPage

class BarChart(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(285)

        self.labels = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        self.bar_color = QColor(66, 133, 244)

    def get_week_data(self):
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        data = []

        for i in range(7):
            current_day = monday + timedelta(days=i)
            data.append((current_day,0))
            
        return data

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
        width = self.width()
        height = self.height()

        painter.fillRect(self.rect(), QColor(248, 250, 253))

        data = self.get_week_data()

        max_minutes = max([item[1] for item in data] + [1])

        if max_minutes <= 60:
            chart_max = 60
        elif max_minutes <= 120:
            chart_max = 120
        elif max_minutes <= 180:
            chart_max = 180
        else:
            chart_max = ((int(max_minutes) // 60) + 1) * 60

        left = 55
        right = 20
        top = 25
        bottom = 70

        chart_width = width - left - right
        chart_height = height - top - bottom

        grid_count = 4

        bar_spacing = chart_width / 7

        today = date.today()
        today_index = today.weekday()

        # Highlight today's column
        highlight_x = left + today_index * bar_spacing

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(
            QColor(66, 133, 244, 25)
        )

        painter.drawRect(
            QRectF(
                highlight_x,
                top,
                bar_spacing,
                chart_height
            )
        )

        # Grid lines
        grid_pen = QPen(
            QColor(225, 230, 238),
            1,
            Qt.PenStyle.DashLine
        )

        painter.setFont(
            QFont(
                "Arial",
                9
            )
        )

        for i in range(grid_count + 1):
            value = chart_max * i / grid_count

            y = (top  +  chart_height - (value / chart_max) * chart_height)

            painter.setPen(grid_pen)

            painter.drawLine(left,int(y),width - right,int(y))
            
            if value >= 60:
                label = f"{int(value / 60)}h"
            else:
                label = f"{int(value)}m"

            painter.setPen(QColor(150, 155, 165))
               
            painter.drawText(5, int(y + 4), label)
           

        # Bars
        bar_width = bar_spacing * 0.48

        for index, (day, minutes) in enumerate(data):

            x = (left + index * bar_spacing+ (bar_spacing - bar_width) / 2)
              
            bar_height = (minutes / chart_max ) * chart_height
        
            y = (top + chart_height - bar_height)
            
            painter.setPen(Qt.PenStyle.NoPen)
          
            if index == today_index:
                painter.setBrush(self.bar_color)

            else:
                painter.setBrush(QColor(66, 133, 244, 200))

            if minutes > 0:
                painter.drawRoundedRect(
                    QRectF(
                        x,
                        y,
                        bar_width,
                        bar_height
                    ),
                    6,
                    6
                )

            # Value
            painter.setPen(
                QColor(50, 60, 75)
            )

            painter.setFont(
                QFont(
                    "Arial",
                    9,
                    QFont.Weight.Bold
                )
            )

            if minutes >= 60:
                hours = int(minutes // 60)
                mins = int(minutes % 60)

                if mins == 0:
                    text = f"{hours}h"
                else:
                    text = f"{hours}h {mins}m"
            else:
                text = f"{int(minutes)}m"

            painter.drawText(QRectF(x - 15, y - 25,bar_width + 30,20),Qt.AlignmentFlag.AlignCenter,text)
                              
            # Day
            day_name = day.strftime("%a")
            date_text = day.strftime("%d %b")

            painter.setPen(
                QColor(80, 90, 105)
            )

            painter.setFont(
                QFont(
                    "Arial",
                    9,
                    QFont.Weight.Bold
                )
            )

            painter.drawText(QRectF(x - 15, top + chart_height + 10,bar_width + 30,18),Qt.AlignmentFlag.AlignCenter,day_name)
          
            painter.setFont(
                QFont(
                    "Arial",
                    8
                )
            )

            painter.drawText(QRectF(x - 20, top + chart_height + 30,bar_width + 40,18),Qt.AlignmentFlag.AlignCenter,date_text)
           
        painter.end()


class StudyStatistics(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Study Statistics")

        # Fixed size
        self.setFixedSize(900, 650)

        self.setup_ui()

    def setup_ui(self):
        self.pages = QStackedWidget()
        self.statistics_page = QWidget()
        self.study_statistics_page()
        self.pages.addWidget(self.statistics_page)
        self.history_page = HistoryPage(self.show_statistics)
        self.pages.addWidget(self.history_page)
            
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.pages)
        self.setLayout(main_layout)

       
    def study_statistics_page(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30,20,30,20)
        main_layout.setSpacing(12)

        # TITLE
        title = QLabel("Study Statastics")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # History button
        history_layout = QHBoxLayout()
        history_layout.addStretch()

        self.history_btn = QPushButton("History")
        self.history_btn.setFixedSize(110,35)
        self.history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.history_btn.clicked.connect(self.show_history)

        self.history_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #4285F4;
                border-radius: 8px;
                font-weight: bold;
            }
        """)


        history_layout.addWidget(self.history_btn)
        main_layout.addLayout(history_layout)

        # TODAY'S PRGRESS &TOTAL STUDY TIME LAYOUT
        layout = QHBoxLayout()
        
        # today's progress label
        self.today_progress = QLabel("Today's Progress\n\n h m")

        self.today_progress.setStyleSheet("""
                    QLabel {
                        background-color: white;
                        color :black;
                        border-radius: 10px;
                        padding: 15px;
                        font-size: 16px;
                    }
                """)
        
        # total study time label
        self.total_study_time = QLabel("Total study time\n\nh m")
    
        self.total_study_time.setStyleSheet("""
            QLabel {
                background-color: white;
                color :black;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
            }
        """)

        layout.addWidget(self.today_progress)
        layout.addWidget(self.total_study_time)

        main_layout.addLayout(layout)

        # WEEK&MONTH BTN
        week_month_layout = QHBoxLayout()

        # WEEKLY BTN
        self.weekly = QPushButton("Weekly")
        self.weekly.setFixedSize(105, 36)
        self.weekly.setCursor(Qt.CursorShape.PointingHandCursor)

        self.weekly.setStyleSheet("""
                    QPushButton {
                        border: 1px solid #4285F4;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                """)
        
        # MONTHLY BTN

        self.monthly = QPushButton("Monthly")
        self.monthly.setFixedSize(105, 36)
        self.monthly.setCursor(Qt.CursorShape.PointingHandCursor)

        self.monthly.setStyleSheet("""
                QPushButton {
                    border: 1px solid #4285F4;
                    border-radius: 8px;
                    font-weight: bold;
                }
            """)
        
        week_month_layout.addWidget(self.weekly)
        week_month_layout.addWidget(self.monthly)
        week_month_layout.addStretch()
        main_layout.addLayout(week_month_layout)

        # Study Time chart
        chart_frame = QFrame()

        chart_frame.setFixedHeight(
            355
        )

        chart_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #EEEEEE;
                border-radius: 12px;
            }
        """)

        chart_layout = QVBoxLayout(chart_frame)

        chart_layout.setContentsMargins(20,8,20,8)
        

        chart_layout.setSpacing(3)

        chart_title = QLabel("Study Time")

        chart_title.setFont(
            QFont(
                "Arial",
                16,
                QFont.Weight.Bold
            )
        )

        chart_title.setStyleSheet("""
            color: #333333;
            border: none;
        """)

        chart_layout.addWidget(
            chart_title
        )

        chart = BarChart()

        chart.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        chart_layout.addWidget(chart)

        chart_layout.addStretch()

        main_layout.addWidget(chart_frame)
            
        self.statistics_page.setLayout(main_layout)
    
    
    def show_history(self):
        self.pages.setCurrentWidget(self.history_page)

    def show_statistics(self):
        self.pages.setCurrentWidget(self.statistics_page)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyStatistics()
    window.show()
    sys.exit(app.exec())