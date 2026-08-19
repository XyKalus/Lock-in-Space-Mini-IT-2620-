# # import calendar 
# # import datetime

# # year = datetime.datetime.now().year
# # # txtcal = calendar.TextCalendar(firstweekday=0)
# # # print(txtcal)

# # # days = list(calendar.day_name)
# # # print(days)

# # # calmonth = calendar.month_name
# # # print(calmonth)

# # # htmlcal = calendar.HTMLCalendar
# # # print(htmlcal)

# # # year = int(input('enter the year: '))
# # # month = int(input('enter the month: '))

# # # print(calendar.month(year,month) )
# # all_month = print(calendar.calendar(year))
# # print(all_month)

# # test = int(input('type the month'))
# # monthy = datetime.month(test)
# # termendous = calendar.calendar(monthy)
# # print(termendous)


# """
# Core event model for a calendar app.

# Design idea:
# - An Event has a start (datetime) and a duration (timedelta).
#   Duration naturally lets an event cross midnight -- you don't need
#   any special "spans two days" flag, a timedelta of e.g. 5 hours
#   starting at 22:00 just ends at 03:00 the next day.
# - Recurrence is a separate concern layered on top: given a base event,
#   "does this event occur on day X?" expands the recurrence rule and
#   checks each candidate occurrence.

# Next steps once this feels right:
#   - persist events (JSON to start, SQLite later)
#   - hook get_events_on_day() into your existing `calendar` module output
#   - eventually swap print statements for a real UI
# """

# from dataclasses import dataclass, field
# from datetime import datetime, timedelta, date
# from enum import Enum
# from typing import Optional, List, Tuple
# import itertools


# class Recurrence(Enum):
#     NONE = "none"
#     DAILY = "daily"
#     WEEKLY = "weekly"
#     MONTHLY = "monthly"
#     YEARLY = "yearly"


# @dataclass
# class Event:
#     title: str
#     start: datetime                 # first/only occurrence's start date+time
#     duration: timedelta             # how long it lasts; can cross midnight
#     recurrence: Recurrence = Recurrence.NONE
#     recurrence_end: Optional[date] = None   # None = repeats forever
#     description: str = ""

#     @property
#     def end(self) -> datetime:
#         """End of the FIRST occurrence."""
#         return self.start + self.duration

#     def _advance(self, dt: datetime, n: int) -> datetime:
#         """Return the n-th recurrence's start datetime after the base start."""
#         if self.recurrence == Recurrence.DAILY:
#             return dt + timedelta(days=n)
#         if self.recurrence == Recurrence.WEEKLY:
#             return dt + timedelta(weeks=n)
#         if self.recurrence == Recurrence.MONTHLY:
#             # naive month add, handles year rollover and clamps day-of-month
#             month_index = dt.month - 1 + n
#             year = dt.year + month_index // 12
#             month = month_index % 12 + 1
#             day = min(dt.day, _days_in_month(year, month))
#             return dt.replace(year=year, month=month, day=day)
#         if self.recurrence == Recurrence.YEARLY:
#             try:
#                 return dt.replace(year=dt.year + n)
#             except ValueError:
#                 # e.g. Feb 29 on a non-leap year -> fall back to Feb 28
#                 return dt.replace(year=dt.year + n, day=28)
#         raise ValueError("_advance called on a non-recurring event")

#     def occurrences_overlapping(
#         self, range_start: date, range_end: date
#     ) -> List[Tuple[datetime, datetime]]:
#         """
#         Return (occurrence_start, occurrence_end) datetimes for every
#         occurrence of this event that overlaps [range_start, range_end].
#         Handles occurrences whose duration crosses midnight.
#         """
#         results: List[Tuple[datetime, datetime]] = []

#         if self.recurrence == Recurrence.NONE:
#             candidates = [self.start]
#         else:
#             # Walk occurrences until we've passed range_end or recurrence_end.
#             candidates = []
#             for n in itertools.count():
#                 occ_start = self._advance(self.start, n)
#                 if occ_start.date() > range_end:
#                     break
#                 if self.recurrence_end and occ_start.date() > self.recurrence_end:
#                     break
#                 candidates.append(occ_start)
#                 if n > 10000:  # safety valve against infinite loops
#                     break

#         for occ_start in candidates:
#             occ_end = occ_start + self.duration
#             # overlap test: occurrence must intersect [range_start, range_end]
#             if occ_end.date() >= range_start and occ_start.date() <= range_end:
#                 results.append((occ_start, occ_end))

#         return results

#     def occurs_on(self, day: date) -> bool:
#         return len(self.occurrences_overlapping(day, day)) > 0


# def _days_in_month(year: int, month: int) -> int:
#     if month == 12:
#         next_month = date(year + 1, 1, 1)
#     else:
#         next_month = date(year, month + 1, 1)
#     return (next_month - date(year, month, 1)).days


# def get_events_on_day(events: List[Event], day: date) -> List[Tuple[Event, datetime, datetime]]:
#     """
#     Given a list of events and a target day, return every occurrence
#     touching that day as (event, occurrence_start, occurrence_end).
#     Useful for plugging straight into your `calendar` module loop:

#         for day_num in cal.itermonthdays(year, month):
#             if day_num == 0:
#                 continue
#             d = date(year, month, day_num)
#             todays = get_events_on_day(all_events, d)
#     """
#     out = []
#     for ev in events:
#         for occ_start, occ_end in ev.occurrences_overlapping(day, day):
#             out.append((ev, occ_start, occ_end))
#     return out


# # ---------------------------------------------------------------------------
# # Demo
# # ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     events = [
#         Event(
#             title="New Year party",
#             start=datetime(2026, 12, 31, 22, 0),
#             duration=timedelta(hours=5),  # crosses into Jan 1
#         ),
#         Event(
#             title="Team standup",
#             start=datetime(2026, 8, 3, 9, 0),
#             duration=timedelta(minutes=15),
#             recurrence=Recurrence.WEEKLY,
#             recurrence_end=date(2026, 9, 30),
#         ),
#         Event(
#             title="Rent due",
#             start=datetime(2026, 8, 1, 0, 0),
#             duration=timedelta(hours=1),
#             recurrence=Recurrence.MONTHLY,
#             recurrence_end=None,  # repeats forever
#         ),
#     ]

#     for check_day in [date(2026, 8, 3), date(2027, 1, 1), date(2026, 9, 1)]:
#         print(f"\nEvents on {check_day}:")
#         for ev, s, e in get_events_on_day(events, check_day):
#             print(f"  {ev.title}: {s.strftime('%Y-%m-%d %H:%M')} -> {e.strftime('%Y-%m-%d %H:%M')}")

import datetime as dt

target_datetime = dt.datetime(2030,1,2,12,30,1)
current = dt.datetime.now()

if target_datetime < current :
    print('passed')
else : 
    print('it is yet to come')