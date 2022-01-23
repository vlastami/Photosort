import unittest

import main as m


class MyTestCase(unittest.TestCase):
    def test_photosort(self):
        self.assertEqual(m.create_sequence(9), "009")


if __name__ == '__main__':
    unittest.main()

