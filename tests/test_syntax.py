import unittest

from pyrobuf.parse_proto import Parser


syntax2_explicit = '''
syntax = "proto2";

message SearchRequest {
  required string query = 1;
  optional int32 page_number = 2;
  optional int32 result_per_page = 3;
}
'''

syntax2_implicit = '''
message SearchRequest {
  required string query = 1;
  optional int32 page_number = 2;
  optional int32 result_per_page = 3;
}
'''

syntax3_explicit = '''
syntax = "proto3";

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
}
'''


class SyntaxTest(unittest.TestCase):

    def test_syntax2(self):
        parser = Parser(syntax2_implicit)
        parser.parse()
        parser = Parser(syntax2_explicit)
        parser.parse()

    def test_syntax3(self):
        parser = Parser(syntax3_explicit)
        parser.parse()
