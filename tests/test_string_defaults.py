import unittest

import pytest
from proto_lib_fixture import proto_lib


TestStringDefaultsMessage = None


@pytest.mark.usefixtures('proto_lib')
class StringDefaultsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global TestStringDefaultsMessage
        from test_string_defaults_proto import TestStringDefaultsMessage

    def setUp(self):
        self.message = TestStringDefaultsMessage()

    def test_string_message_field_with_default_of_hello_world(self):
        self.assertEqual("Hello World!", self.message.hello)

    def test_string_message_field_with_default_of_empty_string(self):
        self.assertEqual("", self.message.empty)

    def test_string_message_field_with_default_of_three_spaces(self):
        self.assertEqual("   ", self.message.spaces)

    def test_string_message_field_with_default_using_single_quotes(self):
        self.assertEqual("Single quotes", self.message.single_quotes)

    def test_string_message_field_with_default_containing_escaped_chars(self):
        self.assertEqual("Escaped \" quote\n", self.message.escaped_quote)
