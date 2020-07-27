import unittest

Test = None
TestSs1 = None
TestSs3 = None


class MergeFromTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Test, TestSs1, TestSs3
        from test_message_proto import Test, TestSs1, TestSs3

    def test_message_init_with_bad_keyword_arg_raises_value_error(self):
        self.assertRaises(ValueError, Test, non_existant=3)

    def test_message_init_with_scalar_field_keyword_arg_sets_value(self):
        message = Test(req_field=3)
        self.assertEqual(message.req_field, 3)

    def test_message_init_with_message_field_keyword_arg_merges(self):
        ss3_message = TestSs3()
        ss3_message.int_field = 7
        message = Test(another_substruct=ss3_message)
        self.assertFalse(message.another_substruct is ss3_message)
        self.assertEqual(message.another_substruct.int_field, 7)

    def test_message_init_with_repeated_scalar_field_keyword_arg_extends(self):
        source_message = Test()
        source_message.list_fieldx.append(7)
        source_message.list_fieldx.append(8)
        source_message.list_fieldx.append(9)
        message = Test(list_fieldx=source_message.list_fieldx)
        self.assertEqual(list(message.list_fieldx), [7, 8, 9])

    def test_message_init_with_repeated_message_field_keyword_arg_extends(self):
        source_message = Test()
        source_message.list_ref.add().timestamp = 123
        source_message.list_ref.add().timestamp = 456
        message = Test(list_ref=source_message.list_ref)
        self.assertEqual(message.list_ref[0].timestamp, 123)
        self.assertEqual(message.list_ref[1].timestamp, 456)

    def test_message_init_by_repeated_field_add_method_passes_keyword_args(self):
        message = Test()
        message.list_ref.add(timestamp=123, field1=456)
        self.assertEqual(message.list_ref[0].timestamp, 123)
        self.assertEqual(message.list_ref[0].field1, 456)
