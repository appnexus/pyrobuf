import pyrobuf_util


def test_varint_encode_0():
    assert pyrobuf_util.to_varint(0) == b'\x00'


def test_varint_encode_1():
    assert pyrobuf_util.to_varint(1) == b'\x01'


def test_varint_encode_12345():
    assert pyrobuf_util.to_varint(12345) == b'\xb9`'


def test_varint_encode_max_int32():
    assert pyrobuf_util.to_varint(2**31-1) == b'\xff\xff\xff\xff\x07'


def test_varint_encode_max_int64():
    assert pyrobuf_util.to_varint(2**63-1) == b'\xff\xff\xff\xff\xff\xff\xff\xff\x7f'


def test_varint_encode_negative_1():
    assert pyrobuf_util.to_varint(-1) == b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'


def test_varint_encode_negative_12345():
    assert pyrobuf_util.to_varint(-12345) == b'\xc7\x9f\xff\xff\xff\xff\xff\xff\xff\x01'


def test_varint_encode_negative_max_int32():
    assert pyrobuf_util.to_varint(-2**31) == b'\x80\x80\x80\x80\xf8\xff\xff\xff\xff\x01'


def test_varint_encode_negative_max_int64():
    assert pyrobuf_util.to_varint(-2**63) == b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01'


def test_varint_decode_0():
    assert pyrobuf_util.from_varint(b'\x00') == (0, 1)


def test_varint_decode_1():
    assert pyrobuf_util.from_varint(b'\x01') == (1, 1)


def test_varint_decode_12345():
    assert pyrobuf_util.from_varint(b'\xb9`') == (12345, 2)


def test_varint_decode_max_int32():
    assert pyrobuf_util.from_varint(b'\xff\xff\xff\xff\x07') == (2**31-1, 5)


def test_varint_decode_max_int64():
    assert pyrobuf_util.from_varint(b'\xff\xff\xff\xff\xff\xff\xff\xff\x7f') == (2**63-1, 9)


def test_varint_decode_negative_1():
    assert pyrobuf_util.from_varint(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01') == (-1, 10)


def test_varint_decode_negative_12345():
    assert pyrobuf_util.from_varint(b'\xc7\x9f\xff\xff\xff\xff\xff\xff\xff\x01') == (-12345, 10)


def test_varint_decode_negative_max_int32():
    assert pyrobuf_util.from_varint(b'\x80\x80\x80\x80\xf8\xff\xff\xff\xff\x01') == (-2**31, 10)


def test_varint_decode_negative_max_int64():
    assert pyrobuf_util.from_varint(b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01') == (-2**63, 10)


# Now for signed varints

def test_signed_varint_encode_0():
    assert pyrobuf_util.to_signed_varint(0) == b'\x00'


def test_signed_varint_encode_1():
    assert pyrobuf_util.to_signed_varint(1) == b'\x02'


def test_signed_varint_encode_12345():
    assert pyrobuf_util.to_signed_varint(12345) == b'\xf2\xc0\x01'


def test_signed_varint_encode_max_int32():
    assert pyrobuf_util.to_signed_varint(2**31-1) == b'\xfe\xff\xff\xff\x0f'


def test_signed_varint_encode_max_int64():
    assert pyrobuf_util.to_signed_varint(2**63-1) == b'\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01'


def test_signed_varint_encode_negative_1():
    assert pyrobuf_util.to_signed_varint(-1) == b'\x01'


def test_signed_varint_encode_negative_12345():
    assert pyrobuf_util.to_signed_varint(-12345) == b'\xf1\xc0\x01'


def test_signed_varint_encode_negative_max_int32():
    assert pyrobuf_util.to_signed_varint(-2**31) == b'\xff\xff\xff\xff\x0f'


def test_signed_varint_encode_negative_max_int64():
    assert pyrobuf_util.to_signed_varint(-2**63) == b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'


def test_signed_varint_decode_0():
    assert pyrobuf_util.from_signed_varint(b'\x00') == (0, 1)


def test_signed_varint_decode_1():
    assert pyrobuf_util.from_signed_varint(b'\x02') == (1, 1)


def test_signed_varint_decode_12345():
    assert pyrobuf_util.from_signed_varint(b'\xf2\xc0\x01') == (12345, 3)


def test_signed_varint_decode_max_int32():
    assert pyrobuf_util.from_signed_varint(b'\xfe\xff\xff\xff\x0f') == (2**31-1, 5)


def test_signed_varint_decode_max_int64():
    assert pyrobuf_util.from_signed_varint(b'\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01') == (2**63-1, 10)


def test_signed_varint_decode_negative_1():
    assert pyrobuf_util.from_signed_varint(b'\x01') == (-1, 1)


def test_signed_varint_decode_negative_12345():
    assert pyrobuf_util.from_signed_varint(b'\xf1\xc0\x01') == (-12345, 3)


def test_signed_varint_decode_negative_max_int32():
    assert pyrobuf_util.from_signed_varint(b'\xff\xff\xff\xff\x0f') == (-2**31, 5)


def test_signed_varint_decode_negative_max_int64():
    assert pyrobuf_util.from_signed_varint(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01') == (-2**63, 10)
