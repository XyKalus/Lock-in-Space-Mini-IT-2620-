import calendar 
import datetime

year = datetime.datetime.now().year
# txtcal = calendar.TextCalendar(firstweekday=0)
# print(txtcal)

# days = list(calendar.day_name)
# print(days)

# calmonth = calendar.month_name
# print(calmonth)

# htmlcal = calendar.HTMLCalendar
# print(htmlcal)

# year = int(input('enter the year: '))
# month = int(input('enter the month: '))

# print(calendar.month(year,month) )
all_month = print(calendar.calendar(year))
print(all_month)

