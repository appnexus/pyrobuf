import unittest

from pyrobuf.parse_proto import Parser

zero_index_proto = """
message TestZeroIndex {
    required string zero = 0;
}
"""

field_name_collision_proto = """
message TestFieldNameCollision {
    required int32 dupe_name = 1;
    required bytes dupe_name = 2;
}
"""

index_collision_proto = """
message TestIndexCollision {
    required int32 index_one = 1;
    required int64 same_index = 1;
}
"""

nonzero_first_value_proto3 = """
syntax = "proto3";

enum TestNonzeroFirstValue {
    nonzero = 1;
}
"""

enum_name_collision_proto = """
enum TestEnumNamCollision {
    dupe_name = 1;
    dupe_name = 2;
}
"""

value_collision_proto = """
enum TestEValueCollision {
    value_one = 0;
    same_value = 0;
}
"""

global_enum_to_message_collision_proto = """
enum TestEnum {
    dupe_name = 0;
}
message dupe_name {
}
"""

enum_to_field_collision_proto = """
message TestEnumToFieldCollision {
    enum TestEnum {
        dupe_name = 0;
    }
    int32 dupe_name = 1;
}
"""

recursive_message_to_enum_collision_proto = """
message RecursiveMessage {
    message dupe_name {
    }
    enum TestEnum {
        dupe_name = 0;
    }
}
"""

recursive_message_to_field_collision_proto = """
message RecursiveMessage {
    message dupe_name {
    }
    int32 dupe_name = 1;
}
"""



class FieldValidityTest(unittest.TestCase):
    def test_zero_index_field(self):
        with self.assertRaises(AssertionError):
            Parser(zero_index_proto).parse()

    def test_field_name_collision(self):
        with self.assertRaises(AssertionError):
            Parser(field_name_collision_proto).parse()

    def test_field_index_collision(self):
        with self.assertRaises(AssertionError):
            Parser(index_collision_proto).parse()

    def test_enum_nonzero_first_value_in_proto3(self):
        with self.assertRaises(AssertionError):
            Parser(nonzero_first_value_proto3).parse()

    def test_enum_name_collision(self):
        with self.assertRaises(AssertionError):
            Parser(enum_name_collision_proto).parse()

    def test_enum_value_collision(self):
        with self.assertRaises(AssertionError):
            Parser(value_collision_proto).parse()

    def test_global_enum_to_message_collision(self):
        with self.assertRaises(AssertionError):
            Parser(global_enum_to_message_collision_proto).parse()

    def test_enum_to_field_collision(self):
        with self.assertRaises(AssertionError):
            Parser(enum_to_field_collision_proto).parse()

    def test_recursive_message_to_enum_collision(self):
        with self.assertRaises(AssertionError):
            Parser(recursive_message_to_enum_collision_proto).parse()

    def test_recursive_message_to_field_collision(self):
        with self.assertRaises(AssertionError):
            Parser(recursive_message_to_field_collision_proto).parse()


if __name__ == "__main__":
    unittest.main()
