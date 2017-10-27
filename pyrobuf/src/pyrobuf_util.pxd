from libc.stdint cimport *

cdef safe_fill(char *dest, const unsigned char *source, size_t max_len)

cdef safe_dup(const unsigned char *source, size_t max_len)

cdef int32_t get_varint32(const unsigned char *memory, int *offset)

cdef int64_t get_varint64(const unsigned char *memory, int *offset)

cdef int32_t get_signed_varint32(const unsigned char *memory, int *offset)

cdef int64_t get_signed_varint64(const unsigned char *memory, int *offset)

cdef int set_varint32(int32_t varint, bytearray buf)

cdef int set_varint64(int64_t varint, bytearray buf)

cdef int set_signed_varint32(int32_t varint, bytearray buf)

cdef int set_signed_varint64(int64_t varint, bytearray buf)

cdef bint skip_generic(const unsigned char *memory, int *offset, int size, int wire_type)
