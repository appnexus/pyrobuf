import os
import sys
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')


EmptyMessageWithNoFields = None


class EmptyMessageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lib = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                   if name.startswith('lib')].pop())

        if lib not in sys.path:
            sys.path.insert(0, lib)

        global EmptyMessageWithNoFields
        from test_empty_message_proto import EmptyMessageWithNoFields

    def setUp(self):
        self.message = EmptyMessageWithNoFields()

    def test_message_with_no_fields_parse_from_string(self):
        self.assertEqual(0, self.message.ParseFromString(""))

    def test_message_with_no_fields_serialize_to_string(self):
        self.assertEqual("", self.message.SerializeToString())

    def test_message_with_no_fields_serialize_to_json(self):
        self.assertEqual("{}", self.message.SerializeToJson())

    def test_message_with_no_fields_serialize_to_dict(self):
        self.assertEqual({}, self.message.SerializeToDict())
