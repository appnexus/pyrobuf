import unittest

from pyrobuf.parse_proto import Parser


class TestMissingLBraces(unittest.TestCase):
    def test_enum_with_missing_lbrace_raises_exception(self):
        s = "enum MissingLBrace    NO = 0;    YES = 1;}"
        parser = Parser(s)

        self.assertRaises(Exception, parser.parse)

    def test_message_with_missing_lbrace_raises_exception(self):
        s = "message MissingLBrace    required int32 i = 1;    optional int32 j = 2;}"
        parser = Parser(s)

        self.assertRaises(Exception, parser.parse)
