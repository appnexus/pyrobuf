import os
import sys
import unittest
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')


TestDeprecatedField = None


class DecimalDefaultsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lib = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                   if name.startswith('lib')].pop())

        if lib not in sys.path:
            sys.path.insert(0, lib)

        global TestDeprecatedField
        from test_deprecated_field_proto import TestDeprecatedField

    def setUp(self):
        warnings.filterwarnings("error")
        self.message = TestDeprecatedField()

    def test_deprecation_warning(self):
        with self.assertRaises(DeprecationWarning):
            x = self.message.old_field

        with self.assertRaises(DeprecationWarning):
            self.message.old_field = 4
