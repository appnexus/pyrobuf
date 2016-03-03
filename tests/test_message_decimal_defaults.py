import os
import sys
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')


TestDecimalDefaultsMessage = None


class DecimalDefaultsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lib = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                   if name.startswith('lib')].pop())

        if lib not in sys.path:
            sys.path.insert(0, lib)

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
