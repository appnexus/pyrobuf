import unittest

from create_message import create_an_test


class CachingTest(unittest.TestCase):

    def test_basic_no_difference(self):
        test = create_an_test()
        self.assertEqual(test.SerializeToString(),
                         test.SerializeToString(cache=True))

    def test_basic_caching(self):
        test = create_an_test()
        serialized = test.SerializeToString()
        print(serialized)
        test.ParseFromString(serialized, cache=True)
        self.assertEqual(serialized, test.SerializeToString(cache=True))
        self.assertEqual(serialized, test.SerializeToString(cache=True))

    def test_update(self):
        test = create_an_test()
        serialized = test.SerializeToString(cache=True)
        test.field = test.field + 1
        self.assertNotEqual(serialized, test.SerializeToString(cache=True))
        test.ParseFromString(serialized, cache=True)
        test.field = test.field + 1
        self.assertNotEqual(serialized, test.SerializeToString(cache=True))

    def test_update_child(self):
        test = create_an_test()
        serialized = test.SerializeToString(cache=True)
        test.substruct.field1 = test.substruct.field1 + 1
        self.assertNotEqual(serialized, test.SerializeToString(cache=True))
        test.ParseFromString(serialized, cache=True)
        test.substruct.field1 = test.substruct.field1 + 1
        self.assertNotEqual(serialized, test.SerializeToString(cache=True))
