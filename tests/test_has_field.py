import unittest


Test = None
TestRef = None
TestSs1 = None
TestSs1Thing = None


class HasFieldTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Test, TestRef, TestSs1, TestSs1Thing
        from test_message_proto import Test, TestSs1, TestSs1Thing
        from test_ref_message_proto import TestRef

    def test_has_field_for_repeated_field_raises_value_error(self):
        message = Test()
        self.assertRaises(ValueError, message.HasField, 'list_fieldx')

    def test_has_field_for_unset_scalar_field_returns_false(self):
        message = Test()
        self.assertFalse(message.HasField('timestamp'))

    def test_has_field_for_set_scalar_field_returns_true(self):
        message = Test()
        message.timestamp = 123
        self.assertTrue(message.HasField('timestamp'))

    def test_has_field_for_cleared_scalar_field_returns_false(self):
        message = Test()
        message.timestamp = 123
        message.ClearField('timestamp')
        self.assertFalse(message.HasField('timestamp'))

    def test_has_field_for_unset_message_field_returns_false(self):
        message = Test()
        self.assertFalse(message.HasField('substruct'))

    def test_has_field_for_set_message_field_returns_true(self):
        message = Test()
        message.substruct.field2 = "something"
        self.assertTrue(message.HasField('substruct'))

    def test_has_field_for_cleared_message_field_returns_false(self):
        message = Test()
        message.substruct.field2 = "something"
        message.ClearField('substruct')
        self.assertFalse(message.HasField('substruct'))

    def test_has_field_for_scalar_field_of_cleared_message_returns_false(self):
        message = Test()
        message.timestamp = 123
        message.Clear()
        self.assertFalse(message.HasField('timestamp'))

    def test_has_field_for_message_field_of_cleared_message_returns_false(self):
        message = Test()
        message.substruct.field2 = "something"
        message.Clear()
        self.assertFalse(message.HasField('substruct'))

    def test_has_field_for_indirectly_set_message_field_returns_true(self):
        message = Test()
        message.substruct.field3.field1 = 3.14159
        self.assertTrue(message.HasField('substruct'))

    def test_has_field_for_cleared_indirectly_set_message_field_returns_false(self):
        message = Test()
        message.substruct.field3.field1 = 3.14159
        message.ClearField('substruct')
        self.assertFalse(message.HasField('substruct'))

    def test_has_field_for_message_field_set_by_repeated_field_returns_true(self):
        message = Test()
        message.substruct.list.append(3)
        self.assertTrue(message.HasField('substruct'))

    def test_has_field_for_message_field_set_by_repeated_message_field_returns_true(self):
        message = Test()
        message.substruct.list_object.append(TestSs1Thing())
        self.assertTrue(message.HasField('substruct'))

    def test_has_field_for_string_field_set_by_deserialization_returns_true(self):
        ref_message = TestRef()
        ref_message.field3 = "Hello World"
        ref_message2 = TestRef.FromString(ref_message.SerializeToString())
        self.assertTrue(ref_message2.HasField('field3'))

    def test_has_field_for_scalar_field_set_by_deserialization_returns_true(self):
        ref_message = TestRef()
        ref_message.field1 = 1
        ref_message2 = TestRef.FromString(ref_message.SerializeToString())
        self.assertTrue(ref_message2.HasField('field1'))

    def test_has_field_for_message_field_set_by_deserialization_returns_true(self):
        ss1_message = TestSs1()
        ss1_message.field3.field1 = 3.14159
        ss1_message2 = TestSs1.FromString(ss1_message.SerializeToString())
        self.assertTrue(ss1_message2.field3._is_present_in_parent)
