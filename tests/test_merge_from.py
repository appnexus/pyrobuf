import unittest

Test = None
TestSs1 = None
TestSs3 = None


class MergeFromTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Test, TestSs1, TestSs3
        from test_message_proto import Test, TestSs1, TestSs3

    def test_merge_from_wrong_type_raises_type_error(self):
        dest = Test()
        self.assertRaises(TypeError, dest.MergeFrom, 1)

    def test_merge_from_empty_message_notifies_parent(self):
        source = TestSs1()
        dest = Test()
        dest.substruct.MergeFrom(source)
        self.assertTrue(dest.HasField('substruct'))

    def test_merge_from_empty_message_does_not_set_scalar_field(self):
        source = TestSs3()
        dest = TestSs3()
        dest.MergeFrom(source)
        self.assertFalse(dest.HasField('int_field'))

    def test_merge_from_empty_message_does_not_set_enum_field(self):
        source = Test()
        dest = Test()
        dest.MergeFrom(source)
        self.assertFalse(dest.HasField('enum_field'))

    def test_merge_from_empty_message_does_not_set_message_field(self):
        source = TestSs3()
        dest = TestSs3()
        dest.MergeFrom(source)
        self.assertFalse(dest.HasField('substruct_ref'))

    def test_merge_from_does_set_scalar_field_that_is_set_in_source(self):
        source = TestSs3()
        dest = TestSs3()
        source.int_field = 3
        dest.MergeFrom(source)
        self.assertEqual(dest.int_field, 3)

    def test_merge_from_does_set_enum_field_that_is_set_in_source(self):
        source = Test()
        dest = Test()
        source.enum_field = Test.TEST_ENUM_FIELD_2
        dest.MergeFrom(source)
        self.assertEqual(dest.enum_field, Test.TEST_ENUM_FIELD_2)

    def test_merge_from_does_merge_message_field_that_is_set_in_source(self):
        source = TestSs3()
        dest = TestSs3()
        source.substruct_ref.timestamp = 123
        dest.MergeFrom(source)
        self.assertEqual(dest.substruct_ref.timestamp, 123)

    def test_merge_from_does_not_set_field_that_is_not_set_in_source(self):
        source = TestSs3()
        dest = TestSs3()
        source.int_field = 3
        dest.MergeFrom(source)
        self.assertFalse(dest.HasField('another_int_field'))

    def test_merge_from_does_not_modify_field_that_is_not_set_in_source(self):
        source = TestSs3()
        dest = TestSs3()
        source.int_field = 3
        dest.another_int_field = 5
        dest.MergeFrom(source)
        self.assertEqual(dest.another_int_field, 5)

    def test_merge_from_overwrites_scalar_field_that_is_set_in_source(self):
        source = TestSs3()
        dest = TestSs3()
        source.int_field = 5
        dest.int_field = 3
        dest.MergeFrom(source)
        self.assertEqual(dest.int_field, 5)

    def test_merge_from_overwrites_message_field_that_is_set_in_source(self):
        source = TestSs3()
        dest = TestSs3()
        source.substruct_ref.timestamp = 123
        dest.substruct_ref.timestamp = 456
        dest.MergeFrom(source)
        self.assertEqual(dest.substruct_ref.timestamp, 123)

    def test_merge_from_sets_repeated_scalar_field_that_is_set_in_source(self):
        source = Test()
        dest = Test()
        source.list_fieldx.append(3)
        dest.MergeFrom(source)
        self.assertEqual(len(dest.list_fieldx), 1)
        self.assertEqual(dest.list_fieldx[0], 3)

    def test_merge_from_extends_repeated_scalar_field_that_is_set_in_source(self):
        source = Test()
        dest = Test()
        source.list_fieldx.append(3)
        dest.list_fieldx.append(4)
        dest.MergeFrom(source)
        self.assertEqual(len(dest.list_fieldx), 2)
        self.assertEqual(dest.list_fieldx[0], 4)
        self.assertEqual(dest.list_fieldx[1], 3)

    def test_merge_from_sets_repeated_message_field_that_is_set_in_source(self):
        source = Test()
        dest = Test()
        source.list_ref.add().field1 = 3
        dest.MergeFrom(source)
        self.assertEqual(len(dest.list_ref), 1)
        self.assertEqual(dest.list_ref[0].field1, 3)

    def test_merge_from_extends_repeated_message_field_that_is_set_in_source(self):
        source = Test()
        dest = Test()
        source.list_ref.add().field1 = 3
        dest.list_ref.add().field1 = 4
        dest.MergeFrom(source)
        self.assertEqual(len(dest.list_ref), 2)
        self.assertEqual(dest.list_ref[0].field1, 4)
        self.assertEqual(dest.list_ref[1].field1, 3)
