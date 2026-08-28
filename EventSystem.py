import datetime as dt
from datetime import timedelta
import calendar

def eventsystem():
    today = dt.datetime.today() 
    print(today)

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

    empty, gus = calendar.monthrange(Eyear,Emonth) 
    #checks how many days are in the month selected, this is used to determine at what value (28,30 or 31) to change Emonth to the following the month
    print(gus)

    if Eday > gus:
        extra_days = (Eday - 1)// dt.datetime.month(Emonth)

    date2 = dt.datetime(Eyear,Emonth,Eday,Ehour,Eminute)
    print(date2)

    calc = date2 - today

    print(calc)

eventsystem()