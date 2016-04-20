import unittest

from pyrobuf_list import BytesList, StringList


NON_STRING_VALUE = 1


class TestBytesList(unittest.TestCase):
    def test_append(self):
        bytes_list = BytesList()
        bytes_list.append(b"some string")
        self.assertEqual(bytes_list, [b"some string"])

    def test_append_with_non_string(self):
        bytes_list = BytesList()
        with self.assertRaises(TypeError):
            bytes_list.append(NON_STRING_VALUE)

    def test_append_with_unicode_string(self):
        bytes_list = BytesList()
        with self.assertRaises(TypeError):
            bytes_list.append(u"some string")

    def test_delitem(self):
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        del bytes_list[2]
        self.assertEqual(bytes_list, [b"zero", b"one", b"three"])

    def test_delitem_with_slice(self):
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        del bytes_list[1:3]
        self.assertEqual(bytes_list, [b"zero", b"three"])

    def test_extend(self):
        bytes_list = BytesList()
        bytes_list.extend([b"some string", b"another string"])
        self.assertEqual(bytes_list, [b"some string", b"another string"])

    def test_extend_with_non_string(self):
        bytes_list = BytesList()
        with self.assertRaises(TypeError):
            bytes_list.extend([b"some string", NON_STRING_VALUE])

    def test_extend_with_unicode_string(self):
        bytes_list = BytesList()
        with self.assertRaises(TypeError):
            bytes_list.extend([u"some string"])

    def test_extend_with_empty_sequence(self):
        bytes_list = BytesList()
        bytes_list.extend([])
        self.assertEqual(bytes_list, [])

    def test_insert(self):
        bytes_list = BytesList()
        bytes_list.insert(0, b"some string")
        self.assertEqual(bytes_list, [b"some string"])

    def test_insert_with_non_string(self):
        bytes_list = BytesList()
        with self.assertRaises(TypeError):
            bytes_list.insert(0, NON_STRING_VALUE)

    def test_insert_with_byte_string(self):
        bytes_list = BytesList()
        with self.assertRaises(TypeError):
            bytes_list.insert(0, u"some string")

    def test_setitem_using_integer(self):
        bytes_list = BytesList()
        bytes_list.append(b"some string")
        bytes_list[0] = b"another string"
        self.assertEqual(bytes_list[0], b"another string")

    def test_setitem_using_slice(self):
        # This will call BytesList.__setslice__ on Python 2
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        bytes_list[1:3] = [b"four", b"five"]
        self.assertEqual(bytes_list, [b"zero", b"four", b"five", b"three"])

    def test_setitem_using_slice_with_non_string(self):
        # This will call BytesList.__setslice__ on Python 2
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        with self.assertRaises(TypeError):
            bytes_list[1:3] = [u"four", NON_STRING_VALUE]

    def test_setitem_using_slice_with_empty_sequence(self):
        # This will call BytesList.__setslice__ on Python 2
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        bytes_list[1:3] = []
        self.assertEqual(bytes_list, [b"zero", b"three"])

    def test_setitem_using_stepped_slice(self):
        # This will call BytesList.__setitem__ on both Python 2 and Python 3
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        bytes_list[0:3:2] = [b"four", b"five"]
        self.assertEqual(bytes_list, [b"four", b"one", b"five", b"three"])

    def test_setitem_using_stepped_slice_with_non_string(self):
        # This will call BytesList.__setitem__ on both Python 2 and Python 3
        bytes_list = BytesList()
        bytes_list.extend([b"zero", b"one", b"two", b"three"])
        with self.assertRaises(TypeError):
            bytes_list[0:3:2] = [b"four", NON_STRING_VALUE]


class TestStringList(unittest.TestCase):
    def test_append(self):
        str_list = StringList()
        str_list.append(u"some string")
        self.assertEqual(str_list, [u"some string"])

    def test_append_with_non_string(self):
        str_list = StringList()
        with self.assertRaises(TypeError):
            str_list.append(NON_STRING_VALUE)

    def test_append_with_byte_string(self):
        str_list = StringList()
        str_list.append(b"some string")
        self.assertEqual(str_list[0], b"some string".decode('utf-8'))

    def test_delitem(self):
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        del str_list[2]
        self.assertEqual(str_list, [u"zero", u"one", u"three"])

    def test_delitem_with_slice(self):
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        del str_list[1:3]
        self.assertEqual(str_list, [u"zero", u"three"])

    def test_extend(self):
        str_list = StringList()
        str_list.extend([u"some string", u"another string"])
        self.assertEqual(str_list, [u"some string", u"another string"])

    def test_extend_with_non_string(self):
        str_list = StringList()
        with self.assertRaises(TypeError):
            str_list.extend([u"some string", NON_STRING_VALUE])

    def test_extend_with_byte_string(self):
        str_list = StringList()
        str_list.extend([b"some string"])
        self.assertEqual(str_list[0], b"some string".decode('utf-8'))

    def test_extend_with_empty_sequence(self):
        str_list = StringList()
        str_list.extend([])
        self.assertEqual(str_list, [])

    def test_insert(self):
        str_list = StringList()
        str_list.insert(0, u"some string")
        self.assertEqual(str_list, [u"some string"])

    def test_insert_with_non_string(self):
        str_list = StringList()
        with self.assertRaises(TypeError):
            str_list.insert(0, NON_STRING_VALUE)

    def test_insert_with_byte_string(self):
        str_list = StringList()
        str_list.insert(0, b"some string")
        self.assertEqual(str_list[0], b"some string".decode('utf-8'))

    def test_setitem_using_integer(self):
        str_list = StringList()
        str_list.append(u"some string")
        str_list[0] = u"another string"
        self.assertEqual(str_list[0], u"another string")

    def test_setitem_using_slice(self):
        # This will call StringList.__setslice__ on Python 2
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        str_list[1:3] = [u"four", u"five"]
        self.assertEqual(str_list, [u"zero", u"four", u"five", u"three"])

    def test_setitem_using_slice_with_non_string(self):
        # This will call StringList.__setslice__ on Python 2
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        with self.assertRaises(TypeError):
            str_list[1:3] = [u"four", NON_STRING_VALUE]

    def test_setitem_using_slice_with_empty_sequence(self):
        # This will call StringList.__setslice__ on Python 2
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        str_list[1:3] = []
        self.assertEqual(str_list, [u"zero", u"three"])

    def test_setitem_using_stepped_slice(self):
        # This will call StringList.__setitem__ on both Python 2 and Python 3
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        str_list[0:3:2] = [u"four", u"five"]
        self.assertEqual(str_list, [u"four", u"one", u"five", u"three"])

    def test_setitem_using_stepped_slice_with_non_string(self):
        # This will call StringList.__setitem__ on both Python 2 and Python 3
        str_list = StringList()
        str_list.extend([u"zero", u"one", u"two", u"three"])
        with self.assertRaises(TypeError):
            str_list[0:3:2] = [u"four", NON_STRING_VALUE]
