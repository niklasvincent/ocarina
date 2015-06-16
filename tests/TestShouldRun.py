import os
import sys
import unittest

import mockings

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core'))
sys.path.insert(1, path)

from now import Now
import chords

class TestShouldRun(unittest.TestCase):

	def testModuleWithoutShouldRunMethod(self):
		now = Now(tweak = "2015-01-01 12:00:00")
		self.assertFalse(chords.shouldRun(
			mockings.createModule(
				"WithoutShouldRunMethod",
				"def main():\n\tpass"
			),
			now,
			mockings.getLogger()
		))

	def testModuleWithFalseShouldRunMethod(self):
		now = Now(tweak = "2015-01-01 12:00:00")
		self.assertFalse(chords.shouldRun(
			mockings.createModule(
				"WithoutShouldRunMethod",
				"def shouldRun(now):\n\treturn False"
			),
			now,
			mockings.getLogger()
		))

	def testModuleWithTrueShouldRunMethod(self):
		now = Now(tweak = "2015-01-01 12:00:00")
		self.assertTrue(chords.shouldRun(
			mockings.createModule(
				"ModuleWithTrueShouldRunMethod",
				"def shouldRun(now):\n\treturn True"
			),
			now,
			mockings.getLogger()
		))

	def testModuleWithExceptionThrowingShouldRun(self):
		now = Now(tweak = "2015-01-01 12:00:00")
		self.assertFalse(chords.shouldRun(
		mockings.createModule(
				"ModuleWithExceptionThrowingShouldRun",
				"def shouldRun(now):\n\traise Exception('Something went wrong')"
			),
			now,
			mockings.getLogger()
		))


def main():
    unittest.main()

if __name__ == '__main__':
    main()