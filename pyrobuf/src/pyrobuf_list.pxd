from libc.stdint cimport *

cdef class TypedList(list):
    
    cdef type _list_type





cdef class Int64List:

    cdef int64_t *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, int64_t x)
    cpdef extend(self, Int64List x)
    cpdef insert(self, int i, int64_t x)
    cpdef pop(self)
    cpdef remove(self, int64_t x)



cdef class Uint64List:

    cdef uint64_t *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, uint64_t x)
    cpdef extend(self, Uint64List x)
    cpdef insert(self, int i, uint64_t x)
    cpdef pop(self)
    cpdef remove(self, uint64_t x)



cdef class CharList:

    cdef char *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, char x)
    cpdef extend(self, CharList x)
    cpdef insert(self, int i, char x)
    cpdef pop(self)
    cpdef remove(self, char x)



cdef class Int32List:

    cdef int32_t *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, int32_t x)
    cpdef extend(self, Int32List x)
    cpdef insert(self, int i, int32_t x)
    cpdef pop(self)
    cpdef remove(self, int32_t x)



cdef class IntList:

    cdef int *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, int x)
    cpdef extend(self, IntList x)
    cpdef insert(self, int i, int x)
    cpdef pop(self)
    cpdef remove(self, int x)



cdef class DoubleList:

    cdef double *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, double x)
    cpdef extend(self, DoubleList x)
    cpdef insert(self, int i, double x)
    cpdef pop(self)
    cpdef remove(self, double x)



cdef class FloatList:

    cdef float *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, float x)
    cpdef extend(self, FloatList x)
    cpdef insert(self, int i, float x)
    cpdef pop(self)
    cpdef remove(self, float x)



cdef class Uint32List:

    cdef uint32_t *_data
    cdef size_t _n_items
    cdef size_t _size

    cpdef append(self, uint32_t x)
    cpdef extend(self, Uint32List x)
    cpdef insert(self, int i, uint32_t x)
    cpdef pop(self)
    cpdef remove(self, uint32_t x)

