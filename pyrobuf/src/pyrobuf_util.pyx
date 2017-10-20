from libc.stdint cimport *
from libc.string cimport *

include "pyrobuf_defs.pxi"


IF PYROBUF_UNAME_SYSNAME == "Windows":
    cdef extern from "strndup.c":
        char * strndup (const char *s, size_t n)


cdef safe_fill(char *dest, const unsigned char *source, size_t max_len):
    """
    Fill preallocated buffer "dest" from string "source" up to length max_len,
    check for string null values, and append a null terminator.
    """
    cdef const char *cast = <const char *>source
    if max_len == 0 or cast == NULL or cast[0] == b'\0':
        dest[0] = b'\0'
        return

    if max_len >= 4 and str(cast).upper() == "NULL":
        dest[0] = b'\0'
        return

    strncpy(dest, cast, max_len - 1)
    dest[max_len - 1] = b'\0'


cdef safe_dup(const unsigned char *source, size_t max_len):
    """
    Return a new string duplicated from string "source" up to length max_len,
    and with a null terminator appended.
    """
    cdef const char *cast = <const char *>source
    if max_len == 0 or cast == NULL or cast[0] == b'\0':
        return b''

    s = b'' + strndup(cast, max_len)
    if max_len >= 4 and str(s).upper() == "NULL":
        return b''

    return s


cdef int32_t get_varint32(const unsigned char *varint, int *offset):
    """
    Deserialize a protobuf varint starting from give offset in memory; update
    offset based on number of bytes consumed.
    """
    cdef int32_t value = 0
    cdef int32_t base = 1
    cdef int index = 0
    cdef int val_byte

    while True:
        val_byte = varint[offset[0] + index]
        value += (val_byte & 0x7F) * base
        if (val_byte & 0x80):
            base *= 128
            index += 1
        else:
            offset[0] += (index + 1)
            return value


cdef int64_t get_varint64(const unsigned char *varint, int *offset):
    """
    Deserialize a protobuf varint starting from give offset in memory; update
    offset based on number of bytes consumed.
    """
    cdef int64_t value = 0
    cdef int64_t base = 1
    cdef int index = 0
    cdef int val_byte

    while True:
        val_byte = varint[offset[0] + index]
        value += (val_byte & 0x7F) * base
        if (val_byte & 0x80):
            base *= 128
            index += 1
        else:
            offset[0] += (index + 1)
            return value

def get_varint(data, offset=0):
    """
    Return an integer value obtained by decoding varint data from the given
    byte string beginning at the specified offset.
    """
    cdef int _offset = offset
    return get_varint64(data, &_offset)


cdef int32_t get_signed_varint32(const unsigned char *varint, int *offset):
    """
    Deserialize a signed protobuf varint starting from give offset in memory;
    update offset based on number of bytes consumed.
    """
    cdef uint32_t value = 0
    cdef int32_t base = 1
    cdef int index = 0
    cdef int val_byte

    while True:
        val_byte = varint[offset[0] + index]
        value += (val_byte & 0x7F) * base
        if (val_byte & 0x80):
            base *= 128
            index += 1
        else:
            offset[0] += (index + 1)
            return <int32_t>((value >> 1) ^ (-(value & 1))) # zigzag decoding

cdef int64_t get_signed_varint64(const unsigned char *varint, int *offset):
    """
    Deserialize a signed protobuf varint starting from give offset in memory;
    update offset based on number of bytes consumed.
    """
    cdef uint64_t value = 0
    cdef int64_t base = 1
    cdef int index = 0
    cdef int val_byte

    while True:
        val_byte = varint[offset[0] + index]
        value += (val_byte & 0x7F) * base
        if (val_byte & 0x80):
            base *= 128
            index += 1
        else:
            offset[0] += (index + 1)
            return <int64_t>((value >> 1) ^ (-(value & 1))) # zigzag decoding

def get_signed_varint(data, offset=0):
    """
    Return an integer value obtained by decoding signed-varint data from the
    given byte string beginning at the specified offset.
    """
    cdef int _offset = offset
    return get_signed_varint64(data, &_offset)


cdef int set_varint32(int32_t varint, bytearray buf):
    """
    Serialize an integer into a protobuf varint; return the number of bytes
    serialized.
    """

	# Negative numbers are always 10 bytes, so we need a uint64_t to
    # facilitate encoding
    cdef uint64_t enc = varint
    cdef uint8_t bits = enc & 0x7f
    enc >>= 7
    cdef int idx = 1
    while enc:
        buf.append(<unsigned char>(0x80|bits))
        bits = enc & 0x7f
        enc >>= 7
        idx += 1
    buf.append(<unsigned char>bits)
    return idx + 1

cdef int set_varint64(int64_t varint, bytearray buf):
    """
    Serialize an integer into a protobuf varint; return the number of bytes
    serialized.
    """

    # Negative numbers are always 10 bytes, so we need a uint64_t to
    # facilitate encoding
    cdef uint64_t enc = varint
    cdef uint8_t bits = enc & 0x7f
    enc >>= 7
    cdef int idx = 1
    while enc:
        buf.append(<unsigned char>(0x80|bits))
        bits = enc & 0x7f
        enc >>= 7
        idx += 1
    buf.append(<unsigned char>bits)
    return idx + 1

def to_varint(varint):
    """
    Return a byte string containing the varint encoded form of the specified
    varint.
    """
    buf = bytearray()
    set_varint64(varint, buf)
    return buf


cdef int set_signed_varint32(int32_t varint, bytearray buf):
    """
    Serialize an integer into a signed protobuf varint; return the number of
    bytes serialized.
    """
    cdef uint32_t enc
    cdef uint8_t bits
    cdef int idx = 1

    enc = (varint << 1) ^ (varint >> 31) # zigzag encoding
    bits = enc & 0x7f
    enc >>= 7
    while enc:
        buf.append(<unsigned char>(bits | 0x80))
        bits = enc & 0x7f
        enc >>= 7
        idx += 1

    buf.append(<unsigned char>bits)
    return idx + 1


cdef int set_signed_varint64(int64_t varint, bytearray buf):
    """
    Serialize an integer into a signed protobuf varint; return the number of
    bytes serialized.
    """
    cdef uint64_t enc
    cdef uint8_t bits
    cdef int idx = 1

    enc = (varint << 1) ^ (varint >> 63) # zigzag encoding
    bits = enc & 0x7f
    enc >>= 7
    while enc:
        buf.append(<unsigned char>(bits | 0x80))
        bits = enc & 0x7f
        enc >>= 7
        idx += 1

    buf.append(<unsigned char>bits)
    return idx + 1


def to_signed_varint(varint):
    """
    Return a byte string containing the signed-varint encoded form of the
    specified varint.
    """
    buf = bytearray()
    set_signed_varint64(varint, buf)
    return buf


def from_varint(data, offset=0):
    """
    Return a (integer value, new_offset) pair obtained by decoding varint data
    from the given byte string beginning at the specified offset.
    """
    cdef int _offset = offset
    result = get_varint64(data, &_offset)
    return result, _offset


def from_signed_varint(data, offset=0):
    """
    Return a (integer value, new_offset) pair obtained by decoding signed varint
    data from the given byte string beginning at the specified offset.
    """
    cdef int _offset = offset
    result = get_signed_varint64(data, &_offset)
    return result, _offset


cdef bint skip_generic(const unsigned char *memory, int *offset, int size, int wire_type):
    """
    Parse field of given wire type to update offset.
    """
    cdef int64_t skip

    if wire_type == 0:
        get_varint64(memory, offset)
    elif wire_type == 1:
        offset[0] += 8
    elif wire_type == 2:
        skip = get_varint64(memory, offset)
        offset[0] += skip
    elif wire_type == 5:
        offset[0] += 4
    else:
        return False

    return offset[0] <= size
