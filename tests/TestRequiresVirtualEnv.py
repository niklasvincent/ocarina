import os
import sys
import unittest

import mockings

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core'))
sys.path.insert(1, path)

from now import Now
import chords

class TestRequiresVirtualEnv(unittest.TestCase):

	def testModuleWithRequirements(self):
		now = Now(tweak = "2015-01-01 12:00:00")
		self.assertTrue(chords.requiresVirtualEnv(
			mockings.createModule(
				"WithRequirements",
				"requirements = ['oauth2']\ndef main():\n\tpass"
			),
			now,
			mockings.getLogger()
		))

	def testModuleWithoutRequirements(self):
		now = Now(tweak = "2015-01-01 12:00:00")
		self.assertFalse(chords.requiresVirtualEnv(
			mockings.createModule(
				"WithRequirements",
				"def main():\n\tpass"
			),
			now,
			mockings.getLogger()
		))


def main():
    unittest.main()

if __name__ == '__main__':
    main()