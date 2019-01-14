import unittest

TestRepeatedEnum = None


class RepeatedEnumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global TestRepeatedEnum
        from test_repeated_enum_proto import TestRepeatedEnum

    def test_repeated_enum_serde(self):
        message1 = TestRepeatedEnum()
        message2 = TestRepeatedEnum()

        message1.list_enum.append(2)
        message1.list_enum.append(0)
        message1.list_enum.append(1)

        buf = message1.SerializeToString()
        message2.ParseFromString(buf)

        for i in range(len(message1.list_enum)):
            self.assertEqual(message1.list_enum[i], message2.list_enum[i])

if __name__ == "__main__":
    unittest.main()
