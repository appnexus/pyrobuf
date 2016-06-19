import unittest

from pyrobuf_list import *


class DoubleListTest(unittest.TestCase):

    def test_append_get_set_len(self):
        x = DoubleList()

        for i in range(40):
            x.append(i)

        for i in range(40):
            self.assertEqual(x[i], i)
            x[i] *= 2

        for i in range(40):
            self.assertEqual(x[i], 2 * i)

        with self.assertRaises(IndexError):
            x[40]

        with self.assertRaises(IndexError):
            x[-41] = 1

        self.assertEqual(x[-1], x[39])
        self.assertEqual(x[-5], x[35])

        self.assertEqual(len(x), 40)

    def test_extend(self):
        x1 = DoubleList()
        x2 = DoubleList()

        for i in range(5):
            x1.append(i)
            x2.append(5 + i)

        x1.extend(x2)

        for i in range(10):
            self.assertEqual(x1[i], i)

    def test_insert(self):
        x = DoubleList()

        for i in range(16):
            x.append(i)

        for i in range(16):
            x.insert(8 + i, 10 * i)

        for i in range(16):
            self.assertEqual(x[8 + i], 10 * i)

    def test_pop(self):
        x = DoubleList()

        for i in range(5):
            x.append(i)

        for i in range(5):
            a = x.pop()
            self.assertEqual(a, 5 - i - 1)
            self.assertEqual(len(x), 5 - i - 1)

        with self.assertRaises(IndexError):
            x.pop()

    def test_remove(self):
        x = DoubleList()

        for i in range(5):
            x.append(i)

        x.remove(3)
        self.assertEqual(x[3], 4)

        with self.assertRaises(ValueError):
            x.remove(7)

    def test_extend_with_generic_list(self):
        x1 = DoubleList()
        x2 = [1.0, 2.0, 3.0, 4.0, 5.0]

        x1.extend(x2)

        for i in range(5):
            self.assertEqual(x1[i], x2[i])


if __name__ == "__main__":
    unittest.main()
