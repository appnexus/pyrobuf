import unittest

TestOneof = None
SubMsg = None


class TestOneofTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global TestOneof, SubMsg
        from test_oneof_3_proto import TestOneof, SubMsg

    def test_one_of(self):
        test = TestOneof()
        self.assertFalse(test.HasField('oneof_int64'))
        self.assertFalse(test.HasField('oneof_string'))
        self.assertFalse(test.HasField('oneof_float'))
        self.assertFalse(test.HasField('oneof_submsg'))
        self.assertEqual(0, test.oneof_int64)
        self.assertEqual(0.0, test.oneof_float)
        self.assertEqual('', test.oneof_string)

        test.oneof_int64 = 42
        self.assertTrue(test.HasField('oneof_int64'))
        self.assertEqual(test.oneof_int64, 42)
        self.assertFalse(test.HasField('oneof_string'))
        self.assertFalse(test.HasField('oneof_float'))
        self.assertFalse(test.HasField('oneof_submsg'))
        self.assertEqual(0.0, test.oneof_float)
        self.assertEqual('', test.oneof_string)

        test.oneof_string = 'the string'
        self.assertTrue(test.HasField('oneof_string'))
        self.assertEqual(test.oneof_string, 'the string')
        self.assertFalse(test.HasField('oneof_int64'))
        self.assertFalse(test.HasField('oneof_float'))
        self.assertFalse(test.HasField('oneof_submsg'))
        self.assertEqual(0, test.oneof_int64)
        self.assertEqual(0.0, test.oneof_float)

        test.oneof_float = 42.0
        self.assertTrue(test.HasField('oneof_float'))
        self.assertEqual(test.oneof_float, 42.0)
        self.assertFalse(test.HasField('oneof_int64'))
        self.assertFalse(test.HasField('oneof_string'))
        self.assertFalse(test.HasField('oneof_submsg'))
        self.assertEqual(0, test.oneof_int64)
        self.assertEqual('', test.oneof_string)

        test.oneof_submsg.some_field = 42
        self.assertTrue(test.HasField('oneof_submsg'))
        self.assertTrue(isinstance(test.oneof_submsg, SubMsg))
        self.assertFalse(test.HasField('oneof_int64'))
        self.assertFalse(test.HasField('oneof_float'))
        self.assertFalse(test.HasField('oneof_string'))
        self.assertEqual(0, test.oneof_int64)
        self.assertEqual(0.0, test.oneof_float)
        self.assertEqual('', test.oneof_string)

    def test_oneof_clears(self):
        test = TestOneof()

        test.oneof_int64 = 42
        test.ClearField('oneof_int64')
        self.assertFalse(test.HasField('oneof_int64'))
        self.assertEqual(0, test.oneof_int64)

        test.oneof_submsg.some_field = 42
        self.assertTrue(test.HasField('oneof_submsg'))
        test.ClearField('oneof_submsg')
        self.assertFalse(test.HasField('oneof_submsg'))
