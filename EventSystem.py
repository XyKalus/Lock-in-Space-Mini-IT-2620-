import datetime as dt
from datetime import timedelta
import calendar
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set an event date')
        self.setGeometry(600,250,750,500) # (x,y,width,height)
        self.setWindowIcon(QIcon("cat.png"))

        label = QLabel("test", self)
        label.setFont(QFont('Arial',15))
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())       

if __name__ == "__main__":
    main()


def eventsystem():
    today = dt.datetime.today() 
    print(today)

    #this entire section is for the user to input their event times, the E in each variable represents "Event"
    Eyear = (int(input('enter your event year: ')))
    Emonth = (int(input('enter your event month: ')))
    Eday = (int(input('enter your event day: ')))
    Ehour = (int(input('input the starting hour: ')))
    Eminute = (int(input('input the starting minute: ')))


    #checks if months goes beyond 12 and add year value by 1 for every 12 months it goes over
    if Emonth > 12:  
        extra_years = (Emonth - 1) // 12
        Eyear += extra_years
        Emonth = ((Emonth - 1) % 12) + 1

    empty, DaysInMonth = calendar.monthrange(Eyear,Emonth) 
    #checks how many days are in the month selected, this is used to determine at what value (28,30 or 31) to change Emonth to the following the month
    print(DaysInMonth) 
    #"empty" is ignored because we only want to know the amount of days in EventMonth (Emonth), not EventYear (Eyear), its only purpose is so Eyear is never defined because it is not needed

    if Eday > DaysInMonth:
        extra_days = (Eday - 1)// dt.datetime.month(Emonth)

    date2 = dt.datetime(Eyear,Emonth,Eday,Ehour,Eminute)
    print(date2)

    calc = date2 - today

    print(calc)

