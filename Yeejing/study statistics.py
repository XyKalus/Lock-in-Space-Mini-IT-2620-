import sys
import os
import json
import re
from datetime import date, timedelta, datetime

from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QHBoxLayout,QFrame,QPushButton,QStackedWidget,QToolTip
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter,QColor,QFont,QFontDatabase

from history_page import HistoryPage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(BASE_DIR,"study_progress.json")

SAMPLE_WEEKLY_MINUTES = [
    60,     # Monday
    120,    # Tuesday
    45,     # Wednesday
    90,     # Thursday
    180,    # Friday
    150,    # Saturday
    60      # Sunday
]

SAMPLE_MONTHLY_MINUTES = [
    60,     # January
    120,    # February
    210,    # March
    90,     # April
    300,    # May
    150,    # June
    240,    # July
    180,    # August
    360,    # September
    120,    # October
    270,    # November
    420     # December
]

def load_study_data():
    if not os.path.exists(PROGRESS_FILE):
        return []

    try:
        with open(PROGRESS_FILE,"r",encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            if isinstance(
                data.get("sessions"),
                list
            ):
                return data["sessions"]

            if isinstance(
                data.get("records"),
                list
            ):
                return data["records"]

        return []

    except Exception as e:
        print("Error loading study_progress.json:",e)
        return []


def is_completed(record):
    return record.get("status") == "Completed"


def duration_to_minutes(duration):
    if duration is None:
        return 0

    if isinstance(duration,(int, float)):
        return float(duration)

    text = str(duration).strip()

    if not text:
        return 0


    if ":" in text:
        try:
            parts = text.split(":")

            if len(parts) == 3:

                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])

                return (hours * 60 + minutes+ seconds / 60)
                   
            if len(parts) == 2:
                minutes = int( parts[0])
                seconds = int(parts[1])

                return (minutes + seconds / 60)

        except ValueError:
            return 0

    total = 0

    hour_match = re.search(
        r"(\d+(?:\.\d+)?)\s*hours?",
        text.lower()
    )

    if hour_match:
        total += (
            float(
                hour_match.group(1)
            )
            * 60
        )

    minute_match = re.search(
        r"(\d+(?:\.\d+)?)\s*minutes?",
        text.lower()
    )

    if minute_match:

        total += float(
            minute_match.group(1)
        )


    if total == 0:
        hour_match = re.search(
            r"(\d+(?:\.\d+)?)\s*h\b",
            text.lower()
        )

        if hour_match:

            total += (
                float(
                    hour_match.group(1)
                )
                * 60
            )

        minute_match = re.search(
            r"(\d+(?:\.\d+)?)\s*m\b",
            text.lower()
        )

        if minute_match:

            total += float(
                minute_match.group(1)
            )

    if total > 0:
        return total


    try:
        return float(
            text
        )

    except ValueError:
        return 0


def format_minutes(minutes):
    minutes = int(round(minutes))
    hours = minutes // 60
    mins = minutes % 60

    if hours > 0 and mins > 0:
        return f"{hours}h {mins}m"

    elif hours > 0:
        return f"{hours}h"

    else:
        return f"{mins}m"


def get_record_date(record):
    value = record.get(
        "start_time",
        record.get(
            "Start Time",
            record.get(
                "date",
                record.get(
                    "Date",
                    ""
                )
            )
        )
    )

    if not value:
        return None

    if isinstance( value,date):
        return value

    value = str(value).strip()

    try:
        return datetime.strptime(
            value[:10],
            "%Y-%m-%d"
        ).date()

    except ValueError:
        pass


    try:
        return datetime.strptime(
            value[:10],
            "%d/%m/%Y"
        ).date()

    except ValueError:
        pass

    try:
        return datetime.strptime(
            value[:10],
            "%d-%m-%Y"
        ).date()

    except ValueError:
        pass

    return None

def get_record_duration(record):
    duration = record.get(
        "duration",
        record.get(
            "Duration",
            0
        )
    )

    return duration_to_minutes(
        duration
    )


class BarChart(QWidget):
    def __init__(self, chart_type="weekly"):
        super().__init__()
        self.chart_type = chart_type
        self.setMinimumHeight(285 )

        self.bar_color = QColor(66,133,244)
        self.setMouseTracking(True)
        self.hover_index = -1


    def get_week_data(self):
        today = date.today()

        monday = (today - timedelta (days=today.weekday()))
         
        records = load_study_data()
        data = []

        for i in range(7):
            current_day = (monday + timedelta( days=i))

            total_minutes = (SAMPLE_WEEKLY_MINUTES[i])

            for record in records:
                if not is_completed(record):
                    continue

                record_date = get_record_date(record)

                if record_date is None:
                    continue

                if record_date == current_day:
                    total_minutes += ( get_record_duration(record))

            data.append((current_day,total_minutes))
              

        return data

    def get_month_data(self):
        today = date.today()
        records = load_study_data()
        data = []

        for month in range(1, 13):
            total_minutes = ( SAMPLE_MONTHLY_MINUTES[ month - 1])

            for record in records:
                if not is_completed(record):
                    continue

                record_date = get_record_date(record)

                if record_date is None:
                    continue

                if (record_date.year == today.year and record_date.month == month):
                    total_minutes += (get_record_duration(record))
                
            data.append((month,total_minutes))

        return data


    def get_chart_max(self,max_minutes):
        if max_minutes <= 0:
            return 60

        if max_minutes <= 60:
            return 60

        chart_max = (int((max_minutes + 29)// 30) * 30)
        chart_max += 30

        return chart_max

    def get_chart_geometry(self):
        width = self.width()
        height = self.height()

        top = 25
        bottom = 70
        horizontal_margin = 35
        chart_left = horizontal_margin

        chart_right = (width - horizontal_margin)
        chart_width = (chart_right - chart_left)
        chart_height = (height - top - bottom)
        
        return (chart_left,chart_right,top, chart_height,chart_width)

    def mouseMoveEvent(self,event):
        (left,right,top,chart_height,chart_width) = self.get_chart_geometry()

        if chart_width <= 0:
            return

        if self.chart_type == "weekly":
            data = self.get_week_data()

        else:
            data = self.get_month_data()

        if not data:
            return

        bar_spacing = (chart_width / len(data))

        bar_width = (bar_spacing * 0.48)

        mouse_x = (event.position().x() )

        index = int( (mouse_x - left) / bar_spacing)

        if ( index < 0 or index >= len(data)):
            QToolTip.hideText()
            self.hover_index = -1
            self.update()

            return

        x = (left+ index * bar_spacing+ (bar_spacing- bar_width) / 2)

        if ( mouse_x >= x and mouse_x <= x + bar_width):
            period, minutes = data[index]

            tooltip_text = format_minutes(minutes)
            self.hover_index = index

            QToolTip.showText( event.globalPosition().toPoint(), tooltip_text,self)
            self.update()

        else:
            QToolTip.hideText()
            self.hover_index = -1
            self.update()

    def leaveEvent(self,event):
        QToolTip.hideText()
        self.hover_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        painter.fillRect(self.rect(),QColor(248,250,253))

        if self.chart_type == "weekly":
            data = self.get_week_data()

        else:
            data = self.get_month_data()

        if not data:
            painter.end()
            return

        max_minutes = max(( item[1] for item in data),default=0)

        chart_max = self.get_chart_max(max_minutes)

        (left,right,top,chart_height,chart_width) = self.get_chart_geometry()

        if chart_width <= 0:
            painter.end()
            return

        if chart_height <= 0:
            painter.end()
            return

        bar_spacing = (chart_width / len(data))
        bar_width = ( bar_spacing * 0.48)

        today = date.today()

        if self.chart_type == "weekly":
            today_index = today.weekday()

        else:
            today_index = today.month - 1

        highlight_x = (left + today_index * bar_spacing )

        painter.setPen( Qt.PenStyle.NoPen)
        painter.setBrush(QColor(66,133,244,25))
        painter.drawRect( QRectF(highlight_x,top,bar_spacing,chart_height))

        for index, (period,minutes) in enumerate(data):
            x = (left + index* bar_spacing+ (bar_spacing - bar_width) / 2)

            if chart_max > 0:
                bar_height = (minutes / chart_max* chart_height)

            else:
                bar_height = 0

            y = (top + chart_height- bar_height)

            painter.setPen(Qt.PenStyle.NoPen)

            if index == today_index:
                painter.setBrush(self.bar_color)
              
            else:
                painter.setBrush(QColor(66,133,244,200))

            if index == self.hover_index:
                painter.setBrush(QColor(40,110,220))

            if minutes > 0:
                painter.drawRoundedRect(QRectF(x,y,bar_width,bar_height),6,6)

            painter.setPen(QColor(50,60,75))

            if self.chart_type == "weekly":
                day_name = period.strftime("%a")

                painter.drawText(QRectF(x - 15,top + chart_height+ 10,bar_width + 30,18),Qt.AlignmentFlag.AlignCenter,day_name)

                date_text = period.strftime("%d %b")

                painter.drawText(QRectF(x - 20,top+ chart_height+ 30,bar_width + 40,18),Qt.AlignmentFlag.AlignCenter,date_text)

            else:
                month_name = date(today.year,period,1).strftime("%b")
                painter.drawText(QRectF(x - 15,top+ chart_height+ 10,bar_width + 30,18),Qt.AlignmentFlag.AlignCenter,month_name)

        painter.end()

class StudyStatistics(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100,800)
        self.setGeometry(250,25,1100,800)
        self.setup_ui()

    def setup_ui(self):
        self.pages = QStackedWidget()

        # Statistics Page
        self.statistics_page = QWidget()
        self.study_statistics_page()
        self.pages.addWidget(self.statistics_page)

        # History Page
        self.history_page = HistoryPage(self.show_statistics)
        self.pages.addWidget(self.history_page)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.pages)
        self.setLayout(main_layout)

    # CALCULATE STATISTICS
    def calculate_statistics(self):
        records = load_study_data()
        today = date.today()
        today_minutes = 0
        total_minutes = 0

        for record in records:
            if not is_completed(record):
                continue

            minutes = get_record_duration(record)
            total_minutes += minutes
            record_date = get_record_date(record)

            if record_date == today:
                today_minutes += minutes

        return (today_minutes,total_minutes)

    # UPDATE STATISTICS (TOTAL TIME USAGE & TODAY TIME USAGE)
    def update_statistics(self):
        (today_minutes, total_minutes) = self.calculate_statistics()
        self.today_progress.setText(
            "Today's Progress\n\n"+ format_minutes(today_minutes))

        self.total_study_time.setText(
            "Total Study Time\n\n"+ format_minutes(total_minutes))

        self.weekly_chart.update()
        self.monthly_chart.update()

    # STATISTICS PAGE
    def study_statistics_page(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30,20,30,20)
        main_layout.setSpacing(12)
        
        # QUIT BTN
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0,0,0,0)
        top_bar.addStretch()

        self.quit_btn = QPushButton("X")
        self.quit_btn.setFixedSize(45,45)
        self.quit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quit_btn.clicked.connect(self.close) #connect to main code

        self.quit_btn.setStyleSheet(
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

        top_bar.addWidget(self.quit_btn)
        main_layout.addLayout(top_bar)

        #TITLE
        title = QLabel("Study Statistics")
        title.setFont( QFont(font_family,40))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # HISTORY BTN
        history_layout = QHBoxLayout()
        history_layout.addStretch()
        self.history_btn = QPushButton("History")
        self.history_btn.setFixedSize(110,35)
        self.history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.history_btn.clicked.connect(self.show_history)

        self.history_btn.setStyleSheet(
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

        history_layout.addWidget(self.history_btn)
        main_layout.addLayout(history_layout )

        #TODAY TOTAL TIME AND ALL TOTAL SUM
        stats_layout = QHBoxLayout()
        self.today_progress = QLabel("Today's Progress\n\n0m")

        self.today_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.today_progress.setStyleSheet(
            """
            QLabel {
                background-color: white;
                color: black;
                border-radius: 10px;
                padding: 15px;
            }
            """
        )

        self.total_study_time = QLabel("Total Study Time\n\n0m")
        self.total_study_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.total_study_time.setStyleSheet(
            """
            QLabel {
                background-color: white;
                color: black;
                border-radius: 10px;
                padding: 15px;
            }
            """
        )

        stats_layout.addWidget(self.today_progress)
        stats_layout.addWidget(self.total_study_time)
        main_layout.addLayout(stats_layout)

        # WEEKLY / MONTHLY BUTTONS
        week_month_layout = QHBoxLayout()
        self.weekly = QPushButton("Weekly")
        self.weekly.setFixedSize(105,36)
        self.weekly.setCursor(Qt.CursorShape.PointingHandCursor)

        self.weekly.setStyleSheet(
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

        self.weekly.clicked.connect(self.show_weekly)
        self.monthly = QPushButton("Monthly")
        self.monthly.setFixedSize(105,36)
        self.monthly.setCursor(Qt.CursorShape.PointingHandCursor)

        self.monthly.setStyleSheet(
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

        self.monthly.clicked.connect(self.show_monthly)
        week_month_layout.addWidget(self.weekly)
        week_month_layout.addWidget(self.monthly)
        week_month_layout.addStretch()
        main_layout.addLayout(week_month_layout)

        # CHART FRAME
        self.chart_frame = QFrame()
        self.chart_frame.setFixedHeight(355)
        self.chart_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 1px solid #EEEEEE;
                border-radius: 12px;
            }
            """
        )

        chart_layout = QVBoxLayout(self.chart_frame)

        chart_layout.setContentsMargins(20,8,20,8)
        chart_layout.setSpacing(3)

        self.chart_pages = QStackedWidget()
        self.weekly_chart = BarChart("weekly")
        self.monthly_chart = BarChart("monthly")
        self.chart_pages.addWidget(self.weekly_chart)
        self.chart_pages.addWidget(self.monthly_chart)

        # DEFAULT SHOW AS WEEKLY CHART FIRST
        self.chart_pages.setCurrentWidget(self.weekly_chart)
        chart_layout.addWidget(self.chart_pages)
        main_layout.addWidget(self.chart_frame)
        self.statistics_page.setLayout(main_layout)
        self.update_statistics()

    def show_history(self):
        self.history_page.refresh_history()
        self.pages.setCurrentWidget(self.history_page)

    # SHOW WEEKLY
    def show_weekly(self):
        self.chart_pages.setCurrentWidget(self.weekly_chart)
    
        self.weekly_chart.hover_index = -1
        QToolTip.hideText()
        self.weekly_chart.update()


    def show_monthly(self):
        self.chart_pages.setCurrentWidget(self.monthly_chart)
        self.monthly_chart.hover_index = -1
        QToolTip.hideText()
        self.monthly_chart.update()

    def show_statistics(self):
        self.update_statistics()
        self.pages.setCurrentWidget(self.statistics_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_id = (QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "Cave-Story.ttf")))

    if font_id != -1:
        families = (QFontDatabase.applicationFontFamilies(font_id))

        if families:
            font_family = families[0]
            app.setFont(QFont(font_family,20))

    window = StudyStatistics()
    window.show()
    sys.exit(app.exec())