import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

class TestFunc(unittest.TestCase):

    def test_func(self):
        self.assertEqual(1, True)

if __name__ == '__main__':
    unittest.main()