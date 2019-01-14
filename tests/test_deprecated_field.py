import unittest
import warnings


class DecimalDefaultsTest(unittest.TestCase):
    def setUp(self):
        from test_message_field_types_proto import TestDeprecatedField
        warnings.filterwarnings("error")
        self.message = TestDeprecatedField()

    def test_deprecation_warning(self):
        with self.assertRaises(DeprecationWarning):
            x = self.message.old_field

        with self.assertRaises(DeprecationWarning):
            self.message.old_field = 4
