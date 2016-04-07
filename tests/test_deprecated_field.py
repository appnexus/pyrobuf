import unittest
import warnings

import pytest
from proto_lib_fixture import proto_lib


@pytest.mark.usefixtures('proto_lib')
class DecimalDefaultsTest(unittest.TestCase):
    def setUp(self):
        from test_deprecated_field_proto import TestDeprecatedField
        warnings.filterwarnings("error")
        self.message = TestDeprecatedField()

    def test_deprecation_warning(self):
        with self.assertRaises(DeprecationWarning):
            x = self.message.old_field

        with self.assertRaises(DeprecationWarning):
            self.message.old_field = 4
