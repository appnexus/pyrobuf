import unittest

TestFieldTypes = None


class MessageFieldTypesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global TestFieldTypes
        from test_message_field_types_proto import TestFieldTypes

    def test_bytes_payload_serialize_to_string(self):
        message = TestFieldTypes()
        message.payload = b'\x01\x02\x03\xf0\xf1\xf2'
        self.assertEqual(message.SerializeToString(), b'\n\x06\x01\x02\x03\xf0\xf1\xf2')

    def test_bytes_payload_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString(b'\n\x06\x01\x02\x03\xf0\xf1\xf2')
        self.assertEqual(message.payload, b'\x01\x02\x03\xf0\xf1\xf2')

    def test_uninitialized_message_serialize_to_json(self):
        message = TestFieldTypes()
        self.assertEqual(message.SerializeToJson(), '{}')

    def test_bytes_payload_serialize_to_json(self):
        message = TestFieldTypes()
        message.payload = b'\x01\x02\x03'
        self.assertEqual(message.SerializeToJson(), '{"payload": "AQID"}')

    def test_bytes_payload_parse_from_json(self):
        message = TestFieldTypes()
        message.ParseFromJson('{"payload": "AQID"}')
        self.assertEqual(message.payload, b'\x01\x02\x03')

    def test_bytes_payload_with_default_has_default_value(self):
        message = TestFieldTypes()
        self.assertEqual(message.payload_with_default, b'Hello World')

    def test_packed_var_width_list_serialize_to_string(self):
        message = TestFieldTypes()
        message.packed_var_width_list.append(1)
        message.packed_var_width_list.append(-2)
        message.packed_var_width_list.append(3)
        self.assertEqual(message.SerializeToString(), b'\x1a\x0c\x01\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x03')

    def test_packed_var_width_list_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString(b'\x1a\x0c\x01\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x03')
        self.assertEqual(len(message.packed_var_width_list), 3)
        self.assertEqual(message.packed_var_width_list[0], 1)
        self.assertEqual(message.packed_var_width_list[1], -2)
        self.assertEqual(message.packed_var_width_list[2], 3)

    def test_packed_fixed_width_list_serialize_to_string(self):
        message = TestFieldTypes()
        message.packed_fixed_width_list.append(1)
        message.packed_fixed_width_list.append(-2)
        message.packed_fixed_width_list.append(3)
        self.assertEqual(message.SerializeToString(), b'"\x0c\x01\x00\x00\x00\xfe\xff\xff\xff\x03\x00\x00\x00')

    def test_packed_fixed_width_list_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString(b'"\x0c\x01\x00\x00\x00\xfe\xff\xff\xff\x03\x00\x00\x00')
        self.assertEqual(len(message.packed_fixed_width_list), 3)
        self.assertEqual(message.packed_fixed_width_list[0], 1)
        self.assertEqual(message.packed_fixed_width_list[1], -2)
        self.assertEqual(message.packed_fixed_width_list[2], 3)

    def test_list_bytes_serialize_to_string(self):
        message = TestFieldTypes()
        message.list_bytes.append(b'Et')
        message.list_bytes.append(b'tu,')
        message.list_bytes.append(b'Brute?')
        self.assertEqual(message.SerializeToString(), b'*\x02Et*\x03tu,*\x06Brute?')

    def test_list_bytes_parse_from_string(self):
        message = TestFieldTypes()
        message.ParseFromString(b'*\x02Et*\x03tu,*\x06Brute?')
        self.assertEqual(len(message.list_bytes), 3)
        self.assertEqual(message.list_bytes, [b'Et', b'tu,', b'Brute?'])

    def test_list_bytes_serialize_to_string_with_nonascii_chars(self):
        message = TestFieldTypes()
        message.list_bytes.append(b"abc\x93def\x10ghi")
        self.assertEqual(message.SerializePartialToString(), b'*\x0babc\x93def\x10ghi')

    def test_list_bytes_parse_from_string_with_nonascii_chars(self):
        message = TestFieldTypes()
        message.ParseFromString(b'*\x0babc\x93def\x10ghi')
        self.assertEqual(message.list_bytes, [b"abc\x93def\x10ghi"])
