import unittest

TestRef = None


class BoolFieldTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global TestRef
        from test_ref_message_proto import TestRef

    def test_bool_field(self):
        message = TestRef()
        self.assertIsInstance(message.field4, bool)
        self.assertIs(message.field4, False)
        message.field4 = True
        self.assertIs(message.field4, True)
