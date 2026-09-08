import sys
import json
import os
from datetime import date, timedelta

from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter,QColor,QPen,QFont


class WeeklyChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.usage = self.load_usage()

        self.setMinimumHeight(300)
        self.setMinimumWidth(650)

    def load_usage(self):

        if not os.path.exists("study_progress.json"):
            return {}

        try:
            with open("study_progress.json", "r") as file:
                return json.load(file)

        except:
            return {}

    def get_week_data(self):

        data = []

        today = date.today()

        for i in range(6, -1, -1):
            current_day = today - timedelta(days=i)
            key = str(current_day)
            seconds = self.usage.get(key, 0)
            minutes = seconds / 60
            data.append((current_day, minutes))

        return data

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()

     
        painter.fillRect(self.rect(),QColor(248, 250, 253))

        data = self.get_week_data()

        max_minutes = max([item[1] for item in data] + [1])

        if max_minutes < 60:
            chart_max = 60
        elif max_minutes < 120:
            chart_max = 120
        elif max_minutes < 180:
            chart_max = 180
        else:
            chart_max = ((int(max_minutes) // 60) + 1) * 60

       
        left = 55
        right = 20
        top = 30
        bottom = 50

        chart_width = width - left - right
        chart_height = height - top - bottom

        grid_count = 4

        painter.setPen(
            QPen(QColor(225, 230, 238), 1)
        )

        painter.setFont(
            QFont("Arial", 9)
        )

        for i in range(grid_count + 1):

            value = chart_max * i / grid_count

            y = (top +chart_height -(value / chart_max) * chart_height)
            painter.drawLine(left,int(y),width - right,int(y))

            if value >= 60:
                label = f"{int(value / 60)}h"
            else:
                label = f"{int(value)}m"

            painter.setPen(
                QColor(150, 155, 165)
            )

            painter.drawText(
                5,
                int(y + 4),
                label
            )

            painter.setPen(
                QPen(QColor(225, 230, 238), 1)
            )

        bar_spacing = chart_width / 7
        bar_width = bar_spacing * 0.48

        for index, (day, minutes) in enumerate(data):

            x = ( left +index * bar_spacing +(bar_spacing - bar_width) / 2)
          
            bar_height = (  minutes / chart_max    ) * chart_height
            
    
            y = (top + chart_height -  bar_height)

            painter.setPen(Qt.NoPen)

            painter.setBrush(
                QColor(65, 120, 230)
            )

            painter.drawRoundedRect(
                QRectF(x,y,bar_width,bar_height),6,6)
           
            painter.setPen(
                QColor(50, 60, 75)
            )

            painter.setFont(
                QFont("Arial", 9, QFont.Bold)
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

            painter.drawText(QRectF(x - 15, y - 25,bar_width + 30,20),Qt.AlignCenter,text)

            day_name = day.strftime("%a")

            painter.setPen(
                QColor(80, 90, 105)
            )

            painter.setFont(
                QFont("Arial", 9, QFont.Bold)
            )

            painter.drawText(
                QRectF(x - 10,top + chart_height + 12,bar_width + 20,25),Qt.AlignCenter,day_name)

        painter.end()


class UsageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.usage = self.load_usage()
        self.initUI()

    def load_usage(self):

        if not os.path.exists("study_progress.json"):
            return {}

        try:
            with open("study_progress.json", "r") as file:
                return json.load(file)

        except:
            return {}

    def get_week_data(self):

        data = []

        today = date.today()

        for i in range(6, -1, -1):

            current_day = today - timedelta(days=i)

            key = str(current_day)

            seconds = self.usage.get(key, 0)

            data.append(
                (current_day, seconds)
            )

        return data

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)

        if hours > 0:
            return f"{hours}h {minutes}m"

        return f"{minutes}m"

    def initUI(self):

        self.setWindowTitle("Weekly Study Progress")

        self.setFixedSize(720, 520)

        data = self.get_week_data()

        total_seconds = sum(seconds for day, seconds in data)
        title = QLabel("Weekly Overview")

        title.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 30px;
                font-weight: bold;
                color: #202A3A;
            }
        """)
  
        subtitle = QLabel(
            "Your 7-day progress summary"
        )

        subtitle.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 16px;
                color: #758095;
            }
        """)

    
        total_label = QLabel(
            f"Total study time : {self.format_time(total_seconds)}"
        )


        chart = WeeklyChart()

        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        info_layout = QVBoxLayout()

        info_layout.addWidget(total_label)

    
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.addLayout(title_layout)

        main_layout.addLayout(info_layout)
        main_layout.addWidget(chart)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UsageWindow()
    window.show()
    sys.exit(app.exec_())