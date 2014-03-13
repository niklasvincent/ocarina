import calendar
import datetime

class Now:

    days = [ 
            'Monday', 
            'Tuesday', 
            'Wednesday', 
            'Thursday', 
            'Friday', 
            'Saturday', 
            'Sunday' 
            ]

    def __init__(self):
        self.date = datetime.datetime.today().timetuple()
        self.year = self.date[0]
        self.month = self.date[1]
        self.day = self.date[2]
        self.weekday = self.date[6] + 1
        self.day_name = self.days[self.weekday]
        self.yday = self.date[7]
        self.time = datetime.datetime.time( datetime.datetime.now() )
        self.hour = str( self.time ).split( ':' )[0]
        self.nbr_of_days_in_month = calendar.monthrange( self.year, self.month )[1]

    def isDay(self, day_name):
        return self.day_name == day_name.capitalize()

    def isDaily(self):
        """ Run daily at 11 PM """
        return self.hour == 23

    def isWeekly(self):
        """ Run sunday at 11 PM """
        return ( self.wekday == 7 and self.hour == 23 )

    def isMonthly(self):
        """ Run on at 11 PM last day of month """
        return self.day == self.nbr_of_days_in_month

    def isHourly(self):
        """ It is always hourly """
        return True

    def isWeekDay(self):
        return self.weekday <= 5

    def isWeekend(self):
        return self.weekday > 5

    def isMorning(self):
        """ Define morning as between 5 AM and 7 AM local time """
        return ( self.hour >= 5 and self.hour <= 7 )

    def isMidnight(self):
        return self.hour == 0

    def isEvening(self):
        return 

    def isWorkingHours(self):
        return True
