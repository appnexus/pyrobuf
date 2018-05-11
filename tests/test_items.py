import unittest

from create_message import create_an_test


class ItemsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global Test
        from test_message_proto import Test

    def test_fields(self):
        test = create_an_test()
        fields = [
            'timestamp',
            'field',
            'string_field',
            'list_fieldx',
            'substruct',
            'test_ref',
            'enum_field',
            'list_ref',
            'another_substruct',
            'req_field',
            'negative_32'
        ]
        self.assertEqual(fields, list(test.Fields()))

    def test_items(self):
        test = create_an_test()
        for field, value in test.Items():
            self.assertEqual(value, getattr(test, field))

    def test_setters(self):
        source = create_an_test()
        dest = Test()

        for setter, value in zip(dest.Setters(), source.Values()):
            setter(value)

        for source_val, dest_val in zip(source.Values(), dest.Values()):
            self.assertEqual(source_val, dest_val)
