import pytest
from proto_lib_fixture import proto_lib


def test_message_a(proto_lib):
    from issue_69_proto import A, B
    a = A()
    assert type(a.b.a.b) == B


def test_message_b(proto_lib):
    from issue_69_proto import A, B
    b = B()
    assert type(b.a.b.a) == A
