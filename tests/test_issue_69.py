def test_message_a():
    from issue_69_proto import A, B
    a = A()
    assert type(a.b.a.b) == B


def test_message_b():
    from issue_69_proto import A, B
    b = B()
    assert type(b.a.b.a) == A
