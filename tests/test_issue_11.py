import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')


@pytest.fixture(scope='module')
def lib():
    lib_path = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                    if name.startswith('lib')].pop())
    if lib not in sys.path:
        sys.path.insert(0, lib)
    return lib_path


def test_before_overflow(lib):
    from issue_11_proto import A
    a = A()
    a.a0 = 0x7FFFFFFF
    assert A.FromString(a.SerializeToString()).a0 == 2147483647


def test_after_overflow(lib):
    from issue_11_proto import A
    a = A()
    a.a0 = 0x80000000
    assert A.FromString(a.SerializeToString()).a0 == 2147483648
