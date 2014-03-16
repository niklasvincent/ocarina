import calendar
from datetime import datetime

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

    def __init__(self, tweak=None):
        self.time = datetime.now().timetuple()
        if tweak is not None:
            try:
                fmt = '%Y-%m-%d %H:%M:%S'
                self.time = datetime.strptime( tweak, fmt ).timetuple()
            except:
                pass

        self.year = self.time.tm_year
        self.month = self.time.tm_mon
        self.day = self.time.tm_mday
        self.weekday = self.time.tm_wday + 1
        self.day_name = self.days[self.weekday -1]
        self.yday = self.time.tm_yday
        self.hour = self.time.tm_hour
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

    def isClosestBankDay(self, day):
        if self.day == day and self.isWeekDay():
            return True
        if self.day == day - 1 and self.isDay( 'Friday' ):
            return True
        if self.day == day - 2 and self.isDay( 'Friday' ):
            return True
        return False
