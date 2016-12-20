import unittest

import pytest
from proto_lib_fixture import proto_lib

M = None
MN = None
MN2 = None


@pytest.mark.usefixtures('proto_lib')
class NestedTest(unittest.TestCase):
    """
    Verifies we can create instance from nested proto file.
    https://github.com/appnexus/pyrobuf/issues/55
    """

    @classmethod
    def setUpClass(cls):
        global M
        global MN
        global MN2
        from test_nested_issue55_proto import M, MN, MN2

    def test_use_nested(self):
        """
        Simple test that just verifies we can creates M, N and N2 objects.
        """
        message_m = M()
        message_n = MN()
        message_n2 = MN2()


if __name__ == "__main__":
    unittest.main()

