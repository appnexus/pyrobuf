import unittest

Test = None
TestRef = None


class MergeFromTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Test, TestRef
        from test_message_proto import Test
        from test_ref_message_proto import TestRef

    def test_extend_with_generic_list(self):
        t = Test()
        refs = [TestRef(), TestRef(), TestRef()]

        for i in range(3):
            refs[i].field1 = i

        t.list_ref.extend(refs)

        for i in range(3):
            self.assertEqual(t.list_ref[i].field1, i)
            self.assertIsNot(t.list_ref[i], refs[i])

    def test_set_list_with_keyword_arg(self):
        refs = [TestRef(), TestRef(), TestRef()]

        for i in range(3):
            refs[i].field1 = i

        t = Test(list_ref=refs)

        for i in range(3):
            self.assertEqual(t.list_ref[i].field1, i)
            self.assertIsNot(t.list_ref[i], refs[i])
