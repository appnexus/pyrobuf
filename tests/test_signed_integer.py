import random


def gen_rand_int32():
    return random.randint(-2**31, 2**31-1)


def gen_rand_uint32():
    return random.randint(0, 2**32-1)


def gen_rand_int64():
    return random.randint(-2**63, 2**63-1)


def gen_rand_uint64():
    return random.randint(0, 2**64-1)


def test_int32():
    from test_signed_integer_proto import Int
    a = Int()
    v = gen_rand_int32()
    a.Int32 = v
    assert Int.FromString(a.SerializeToString()).Int32 == v


def test_int64():
    from test_signed_integer_proto import Int
    a = Int()
    v = gen_rand_int64()
    a.Int64 = v
    assert Int.FromString(a.SerializeToString()).Int64 == v


def test_uint32():
    from test_signed_integer_proto import Int
    a = Int()
    v = gen_rand_uint32()
    a.UInt32 = v
    assert Int.FromString(a.SerializeToString()).UInt32 == v


def test_uint64():
    from test_signed_integer_proto import Int
    a = Int()
    v = gen_rand_uint64()
    a.UInt64 = v
    assert Int.FromString(a.SerializeToString()).UInt64 == v


def test_sint32():
    from test_signed_integer_proto import Int
    a = Int()
    v = gen_rand_int32()
    a.SInt32 = v
    assert Int.FromString(a.SerializeToString()).SInt32 == v


def test_sint64():
    from test_signed_integer_proto import Int
    a = Int()
    v = gen_rand_int64()
    a.SInt64 = v
    assert Int.FromString(a.SerializeToString()).SInt64 == v
