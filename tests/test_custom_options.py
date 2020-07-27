import unittest

TestCustomOptions = None


class TestCustomOptionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global TestCustomOptions
        from test_custom_options_proto import TestCustomOptions

    def test_fields(self):
        test = TestCustomOptions()
        self.assertEqual("bar", test.field2)
        self.assertEqual(1, test.field3)
