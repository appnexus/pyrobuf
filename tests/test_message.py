import unittest

from create_message import *

class MessageTest(unittest.TestCase):

    def test_ser_deser(self):
        t1 = create_google_test()
        t2 = create_an_test()
        buf1 = t1.SerializeToString()
        buf2 = t2.SerializeToString()

        self.failUnlessEqual(buf1, str(buf2))

        t1.ParseFromString(buf1)
        t2.ParseFromString(buf1)
        buf1 = t1.SerializeToString()
        buf2 = t2.SerializeToString()

        self.failUnlessEqual(buf1, str(buf2))

    def test_json(self):
        test = create_an_test()
        json = test.SerializeToJson()

        test.ParseFromJson(json)
        self.failUnlessEqual(json, test.SerializeToJson())

    def test_dict(self):
        test = create_an_test()
        json = test.SerializeToDict()

        test.ParseFromDict(json)
        self.failUnlessEqual(json, test.SerializeToDict())

if __name__ == "__main__":
    unittest.main()
