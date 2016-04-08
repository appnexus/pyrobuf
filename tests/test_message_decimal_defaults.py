import unittest

import pytest
from proto_lib_fixture import proto_lib


TestDecimalDefaultsMessage = None


@pytest.mark.usefixtures('proto_lib')
class DecimalDefaultsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global TestDecimalDefaultsMessage
        from test_decimal_defaults_proto import TestDecimalDefaultsMessage

    def setUp(self):
        self.message = TestDecimalDefaultsMessage()

    def test_zero_point_zero(self):
        self.assertEqual(self.message.zero_point_zero, 0.0)

    def test_point_zero(self):
        self.assertEqual(self.message.point_zero, 0.0)

    def test_default_of_zero_point_five(self):
        self.assertEqual(self.message.zero_point_five, 0.5)

    def test_default_of_minus_zero_point_zero(self):
        self.assertEqual(self.message.minus_zero_point_zero, -0.0)

    def test_default_of_point_five(self):
        self.assertEqual(self.message.point_five, 0.5)

    def test_default_of_minus_point_zero(self):
        self.assertEqual(self.message.minus_point_zero, -0.0)

    def test_default_of_minus_point_five(self):
        self.assertEqual(self.message.minus_point_five, -0.5)

    def test_default_of_pi(self):
        self.assertEqual(self.message.pi, 3.141592653589793)

    def test_default_of_one_e_6(self):
        self.assertEqual(self.message.one_e_6, 1e6)

    def test_default_of_one_point_zero_e_6(self):
        self.assertEqual(self.message.one_point_zero_e_6, 1.0e6)

    def test_default_of_one_capital_e_6(self):
        self.assertEqual(self.message.one_capital_e_6, 1E6)

    def test_default_of_minus_one_e_6(self):
        self.assertEqual(self.message.minus_one_e_6, -1e6)

    def test_default_of_one_e_plus_6(self):
        self.assertEqual(self.message.one_e_plus_6, 1e+6)

    def test_default_of_one_e_minus_6(self):
        self.assertEqual(self.message.one_e_minus_6, 1e-6)
