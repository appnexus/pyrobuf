import unittest

from pyrobuf_list import *

class DoubleListTest(unittest.TestCase):

    def test_append_get_set_len(self):
        x = DoubleList()

        for i in range(40):
            x.append(i)

        for i in range(40):
            self.failUnlessEqual(x[i], i)
            x[i] *= 2

        for i in range(40):
            self.failUnlessEqual(x[i], 2 * i)

        with self.assertRaises(IndexError):
            x[40]

        with self.assertRaises(IndexError):
            x[-41] = 1

        self.failUnlessEqual(x[-1], x[39])
        self.failUnlessEqual(x[-5], x[35])

        self.failUnlessEqual(len(x), 40)

    def test_extend(self):
        x1 = DoubleList()
        x2 = DoubleList()

        for i in range(5):
            x1.append(i)
            x2.append(5 + i)

        x1.extend(x2)

        for i in range(10):
            self.failUnlessEqual(x1[i], i)

    def test_insert(self):
        x = DoubleList()

        for i in range(16):
            x.append(i)

        for i in range(16):
            x.insert(8 + i, 10 * i)

        for i in range(16):
            self.failUnlessEqual(x[8 + i], 10 * i)

    def test_pop(self):
        x = DoubleList()

        for i in range(5):
            x.append(i)

        for i in range(5):
            a = x.pop()
            self.failUnlessEqual(a, 5 - i - 1)
            self.failUnlessEqual(len(x), 5 - i - 1)

        with self.assertRaises(IndexError):
            x.pop()

    def test_remove(self):
        x = DoubleList()

        for i in range(5):
            x.append(i)

        x.remove(3)
        self.assertEquals(x[3], 4)

        with self.assertRaises(ValueError):
            x.remove(7)

if __name__ == "__main__":
    unittest.main()
