import unittest

from pyrobuf.parse_proto import Parser


class TestMissingLBraces(unittest.TestCase):
    def test_enum_with_missing_lbrace_raises_exception(self):
        s = "enum MissingLBrace    NO = 0;    YES = 1;}"
        parser = Parser()

        self.assertRaises(Exception, parser.parse, s)

    def test_enum_with_missing_lbrace_raises_exception_with_correct_message(self):
        s = "enum MissingLBrace    NO = 0;    YES = 1;}"
        parser = Parser()

        try:
            parser.parse(s)
        except Exception as e:
            self.assertEqual("missing opening paren at pos 22: 'NO = 0;   '", str(e))

    def test_message_with_missing_lbrace_raises_exception(self):
        s = "message MissingLBrace    required int32 i = 1;    optional int32 j = 2;}"
        parser = Parser()

        self.assertRaises(Exception, parser.parse, s)

    def test_message_with_missing_lbrace_raises_exception_with_correct_message(self):
        s = "message MissingLBrace    required int32 i = 1;    optional int32 j = 2;}"
        parser = Parser()

        try:
            parser.parse(s)
        except Exception as e:
            self.assertEqual("missing opening paren at pos 25: 'required i'", str(e))
