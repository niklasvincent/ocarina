import os
import sys
import unittest

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core'))
sys.path.insert(1, path)

from now import Now

class TestNow(unittest.TestCase):

	def testDateParsing(self):
		date = Now(tweak = "2015-01-01 12:00:00")
		self.assertEquals(date.year, 2015)
		self.assertEquals(date.month, 1)
		self.assertEquals(date.day, 1)
		self.assertEquals(date.hour, 12)
		self.assertEquals(date.yday, 1)
		self.assertEquals(date.weekday, 4)
		self.assertEquals(date.nbr_of_days_in_month, 31)
		self.assertEquals(date.day_name, "Thursday")

	def testIsDay(self):
		thursday = Now(tweak = "2015-01-01 12:00:00")
		self.assertTrue(thursday.isDay("Thursday"))

	def testIsDaily(self):
		daily = Now(tweak = "2015-01-01 23:00:00")
		self.assertTrue(daily.isDaily())

	def testIsWeekly(self):
		weekly = Now(tweak = "2015-01-04 23:00:00")
		self.assertTrue(weekly.isWeekly())

	def testIsMonthly(self):
		lastDayOfMonth = Now(tweak = "2015-02-28 11:00:00")
		self.assertTrue(lastDayOfMonth.isMonthly())

	def testIsHourly(self):
		self.assertTrue(Now().isHourly())

	def testIsWeekDay(self):
		thursday = Now(tweak = "2015-01-01 12:00:00")
		self.assertTrue(thursday.isWeekDay())

	def testIsWeekend(self):
		saturday = Now(tweak = "2015-01-03 12:00:00")
		self.assertTrue(saturday.isWeekend())

	def testIsMorning(self):
		morning = Now(tweak = "2015-01-01 06:00:00")
		self.assertTrue(morning.isMorning())
		evening = Now(tweak = "2015-01-01 15:00:00")
		self.assertFalse(evening.isMorning())

	def testIsMidnight(self):
		midnight = Now(tweak = "2015-01-01 00:00:00")
		self.assertTrue(midnight.isMidnight())


def main():
    unittest.main()

if __name__ == '__main__':
    main()