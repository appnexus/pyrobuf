import unittest

from create_message import create_an_test


class ItemsTest(unittest.TestCase):

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
