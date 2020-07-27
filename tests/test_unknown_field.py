import unittest


GOOGLE_SERIALIZED_MESSAGE = b'\x08\x80\x89\x9a\x81\x02\x10\xc1S\x1a\tgo goats! \x00 d \xc8\x01 ' \
    b'\xac\x02 \x90\x03*A\x08\xb9`\x12\x05hello\x1a\x12\tH\xe1z\x14\xae.\x96@\x12\x07goodbye!\xd7' \
    b'\xa3p=\n/v@*\r\tn\x86\x1b\xf0\xf9!\t@\x12\x02pi2\tsomething2\x17\x08\x80\x89\x9a\x81\x02\x10' \
    b'\xd7\x08\x19\x8d\x97n\x12\x83\xc0\xf3?"\x03fooB\x17\x08\x80\x89\x9a\x81\x02\x10\xd7\x08\x19' \
    b'\x8d\x97n\x12\x83\xc0\xf3?"\x03fooJ7\n\nwhat\'s up?\x12\x0cnothing much\x18\x18 W*\x17\x08' \
    b'\x80\x89\x9a\x81\x02\x10\xd7\x08\x19\x8d\x97n\x12\x83\xc0\xf3?"\x03fooP\xee\x87\xfb\xff\xff' \
    b'\xff\xff\xff\xff\x01X\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'


class MessageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global TestTruncated
        from test_truncated_proto import TestTruncated

    def test_deser(self):
        test = TestTruncated()
        parsed = test.ParseFromString(GOOGLE_SERIALIZED_MESSAGE)
        self.assertEqual(parsed, len(GOOGLE_SERIALIZED_MESSAGE))
        self.assertEqual(test.req_field, -80914)
        self.assertEqual(test.negative_32, -1)


if __name__ == "__main__":
    unittest.main()
