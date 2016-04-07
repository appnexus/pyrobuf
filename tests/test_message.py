import unittest

import pytest

from create_message import *


@pytest.mark.usefixtures('lib')
class MessageTest(unittest.TestCase):

    def test_ser_deser(self):
        t1 = create_google_test()
        t2 = create_an_test()
        buf1 = t1.SerializeToString()
        buf2 = t2.SerializeToString()

        self.assertEqual(buf1, str(buf2))

        t1.ParseFromString(buf1)
        t2.ParseFromString(buf1)
        buf1 = t1.SerializeToString()
        buf2 = t2.SerializeToString()

        self.assertEqual(buf1, str(buf2))

    def test_json(self):
        test = create_an_test()
        json = test.SerializeToJson()

        test.ParseFromJson(json)
        self.assertEqual(json, test.SerializeToJson())

    def test_dict(self):
        test = create_an_test()
        json = test.SerializeToDict()

        test.ParseFromDict(json)
        self.assertEqual(json, test.SerializeToDict())

if __name__ == "__main__":
    unittest.main()
