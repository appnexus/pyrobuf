import pytest
from proto_lib_fixture import proto_lib


def test_before_overflow(proto_lib):
    from issue_11_proto import A
    a = A()
    a.a0 = 0x7FFFFFFF
    assert A.FromString(a.SerializeToString()).a0 == 2147483647


def test_after_overflow(proto_lib):
    from issue_11_proto import A
    a = A()
    a.a0 = 0x80000000
    assert A.FromString(a.SerializeToString()).a0 == 2147483648
