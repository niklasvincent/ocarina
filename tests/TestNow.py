import os
import sys
import unittest

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core'))
sys.path.insert(1, path)

from now import Now

class TestNow(unittest.TestCase):

	def testIsMonthly(self):
		lastDayOfMonth = Now(tweak = "2015-02-28 11:00:00")
		self.assertTrue(lastDayOfMonth.isMonthly())

def main():
    unittest.main()

if __name__ == '__main__':
    main()