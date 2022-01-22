import unittest
from exif import Image

import main as m


class MyTestCase(unittest.TestCase):
    def test_photosort(self):
        self.assertRaises(AttributeError, m.latitude, None)


if __name__ == '__main__':
    unittest.main()
