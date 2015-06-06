import os
import sys
import unittest

import mockings

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../core'))
sys.path.insert(1, path)

import database

class TestDatabase(unittest.TestCase):

	db = None

	def setUp(self):
		self.db = database.getInstance(":memory:", True)

	def testSetKeyValuePair(self):
		self.db.set("some_key", "some_value")
		self.assertEquals("some_value", self.db.get("some_key"))

	def testGetNonExistingKeyValuePair(self):
		self.assertEquals(None, self.db.get("some_key"))

	def testSetDictionary(self):
		self.db.set("some_key", { "a" : 1, "b" : 2})
		retrievedDict = self.db.get("some_key")
		self.assertEquals({ "a" : 1, "b" : 2}, retrievedDict)

def main():
    unittest.main()

if __name__ == '__main__':
    main()