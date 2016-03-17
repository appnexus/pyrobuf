import os
import sys
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')


TestFieldTypes = None


class MergeFromTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lib = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                   if name.startswith('lib')].pop())

        if lib not in sys.path:
            sys.path.insert(0, lib)

        global TestFieldTypes
        from test_message_field_types_proto import TestFieldTypes

    def test_bytes_payload_serialize_to_string(self):
        message = TestFieldTypes()
        message.payload = b'\x01\x02\x03'
        self.assertEqual(message.SerializeToString(), '\n\x03\x01\x02\x03')

    def test_bytes_payload_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString('\n\x03\x01\x02\x03')
        self.assertEqual(message.payload, '\x01\x02\x03')

    def test_uninitialized_message_serialize_to_json(self):
        message = TestFieldTypes()
        self.assertEqual(message.SerializeToJson(), '{}')

    def test_bytes_payload_serialize_to_json(self):
        message = TestFieldTypes()
        message.payload = b'\x01\x02\x03'
        self.assertEqual(message.SerializeToJson(), '{"payload": "\\u0001\\u0002\\u0003"}')

    def test_bytes_payload_parse_from_json(self):
        message = TestFieldTypes()
        message.ParseFromJson('{"payload": "\\u0001\\u0002\\u0003"}')
        self.assertEqual(message.payload, '\x01\x02\x03')

    def test_bytes_payload_with_default_has_default_value(self):
        message = TestFieldTypes()
        self.assertEqual(message.payload_with_default, 'Hello World')

    def test_packed_var_width_list_serialize_to_string(self):
        message = TestFieldTypes()
        message.packed_var_width_list.append(1)
        message.packed_var_width_list.append(-2)
        message.packed_var_width_list.append(3)
        self.assertEqual(message.SerializeToString(), '\x1a\x0c\x01\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x03')

    def test_packed_var_width_list_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString('\x1a\x0c\x01\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x03')
        self.assertEqual(len(message.packed_var_width_list), 3)
        self.assertEqual(message.packed_var_width_list[0], 1)
        self.assertEqual(message.packed_var_width_list[1], -2)
        self.assertEqual(message.packed_var_width_list[2], 3)

    def test_packed_fixed_width_list_serialize_to_string(self):
        message = TestFieldTypes()
        message.packed_fixed_width_list.append(1)
        message.packed_fixed_width_list.append(-2)
        message.packed_fixed_width_list.append(3)
        self.assertEqual(message.SerializeToString(), '"\x0c\x01\x00\x00\x00\xfe\xff\xff\xff\x03\x00\x00\x00')

    def test_packed_fixed_width_list_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString('"\x0c\x01\x00\x00\x00\xfe\xff\xff\xff\x03\x00\x00\x00')
        self.assertEqual(len(message.packed_fixed_width_list), 3)
        self.assertEqual(message.packed_fixed_width_list[0], 1)
        self.assertEqual(message.packed_fixed_width_list[1], -2)
        self.assertEqual(message.packed_fixed_width_list[2], 3)

    def test_list_bytes_serialize_to_string(self):
        message = TestFieldTypes()
        message.list_bytes.append('Et')
        message.list_bytes.append('tu,')
        message.list_bytes.append('Brute?')
        self.assertEqual(message.SerializeToString(), '*\x02Et*\x03tu,*\x06Brute?')

    def test_list_bytes_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString('*\x02Et*\x03tu,*\x06Brute?')
        self.assertEqual(len(message.list_bytes), 3)
        self.assertEqual(message.list_bytes, ['Et', 'tu,', 'Brute?'])
