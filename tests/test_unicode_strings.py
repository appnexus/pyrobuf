import unittest

Test = None
TestSs1 = None

# Alpha, Beta, Gamma, Delta
GREEK_LETTERS = u"\u0391\u0392\u0393\u0394"


class TestUnicodeStrings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Test, TestSs1, TestFieldTypes
        from test_message_proto import Test, TestSs1

    def test_unicode_string_parse_from_string(self):
        message = Test.FromString(b'\x1a\x08\xce\x91\xce\x92\xce\x93\xce\x94')
        self.assertEqual(message.string_field, GREEK_LETTERS)

    def test_unicode_string_parse_from_dict(self):
        message = Test()
        message.ParseFromDict({'string_field': u"\u0391\u0392\u0393\u0394", 'req_field': 1})
        self.assertEqual(message.string_field, GREEK_LETTERS)

    def test_unicode_string_parse_from_json(self):
        message = Test()
        message.ParseFromJson('{"string_field": "\\u0391\\u0392\\u0393\\u0394", "req_field": 1}')
        self.assertEqual(message.string_field, GREEK_LETTERS)

    def test_unicode_string_serialize_to_string(self):
        message = Test()
        message.string_field = GREEK_LETTERS
        self.assertEqual(message.SerializePartialToString(), b'\x1a\x08\xce\x91\xce\x92\xce\x93\xce\x94')

    def test_unicode_string_serialize_to_dict(self):
        message = Test()
        message.string_field = GREEK_LETTERS
        message.req_field = 1
        self.assertEqual(
            message.SerializeToDict(), {'string_field': u"\u0391\u0392\u0393\u0394", 'req_field': 1}
        )

    def test_unicode_string_serialize_to_json(self):
        # Use TestSs1 here because Test has a required field
        message = TestSs1()
        message.field2 = GREEK_LETTERS
        self.assertEqual(
            message.SerializeToJson(), '{"field2": "\\u0391\\u0392\\u0393\\u0394"}'
        )

    def test_repeated_unicode_parse_from_string(self):
        message = TestSs1.FromString(b'2\x04\xce\x91\xce\x922\x04\xce\x93\xce\x94')
        self.assertEqual(message.list_string, [u"\u0391\u0392", u"\u0393\u0394"])

    def test_repeated_unicode_parse_from_dict(self):
        message = TestSs1()
        message.ParseFromDict({'list_string': [u'\u0391\u0392', u'\u0393\u0394']})
        self.assertEqual(message.list_string, [u"\u0391\u0392", u"\u0393\u0394"])

    def test_repeated_unicode_parse_from_json(self):
        message = TestSs1()
        message.ParseFromJson('{"list_string": ["\\u0391\\u0392", "\\u0393\\u0394"]}')
        self.assertEqual(message.list_string, [u"\u0391\u0392", u"\u0393\u0394"])

    def test_repeated_unicode_string_serialize_to_string(self):
        message = TestSs1()
        message.list_string.append(GREEK_LETTERS[:2])  # Alpha, Beta
        message.list_string.append(GREEK_LETTERS[2:])  # Gamma, Delta
        self.assertEqual(message.SerializePartialToString(), b'2\x04\xce\x91\xce\x922\x04\xce\x93\xce\x94')

    def test_repeated_unicode_string_serialize_to_dict(self):
        message = TestSs1()
        message.list_string.append(GREEK_LETTERS[:2])  # Alpha, Beta
        message.list_string.append(GREEK_LETTERS[2:])  # Gamma, Delta
        self.assertEqual(message.SerializeToDict(), {'list_string': [u'\u0391\u0392', u'\u0393\u0394']})

    def test_repeated_unicode_string_serialize_to_json(self):
        message = TestSs1()
        message.list_string.append(GREEK_LETTERS[:2])  # Alpha, Beta
        message.list_string.append(GREEK_LETTERS[2:])  # Gamma, Delta
        self.assertEqual(message.SerializeToJson(), '{"list_string": ["\\u0391\\u0392", "\\u0393\\u0394"]}')
