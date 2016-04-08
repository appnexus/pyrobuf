import unittest

import pytest
from proto_lib_fixture import proto_lib


EmptyMessageWithNoFields = None


@pytest.mark.usefixtures('proto_lib')
class EmptyMessageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
