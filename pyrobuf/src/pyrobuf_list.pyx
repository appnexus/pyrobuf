from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from libc.stdint cimport *

cdef class TypedList(list):

    def __init__(self, type list_type):
        self._list_type = list_type

    property list_type:
        def __get__(self):
            return self._list_type

    def __setitem__(self, i, x):
        try:
            assert isinstance(x, self._list_type)
        except AssertionError:
            raise Exception("type mismatch")

        super(TypedList, self).__setitem__(i, x)


    def __setslice__(self, i, j, x):
        try:
            assert isinstance(x, TypedList)
            assert self._list_type == x.list_type
        except AssertionError:
            raise Exception("type mismatch")

        super(TypedList, self).__setslice__(i, j, x)

    def add(self):
        elt = self._list_type()
        self.append(elt)
        return elt

    def append(self, x):
        try:
            assert isinstance(x, self._list_type)
        except AssertionError:
            raise Exception("type mismatch")

        super(TypedList, self).append(x)

    def extend(self, x):
        try:
            assert isinstance(x, TypedList)
            assert self._list_type == x.list_type
        except AssertionError:
            raise Exception("type mismatch")

        super(TypedList, self).extend(x)

    def insert(self, i, x):
        try:
            assert isinstance(x, self._list_type)
        except AssertionError:
            raise Exception("type mismatch")

        super(TypedList, self).insert(i, x)






cdef class Int64List:

    def __cinit__(self, size_t size=16):
        self._data = <int64_t *>PyMem_Malloc(size * sizeof(int64_t))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, int64_t x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, int64_t x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, int64_t x):
        cdef int64_t *mem

        if self._n_items == self._size:
            mem = <int64_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(int64_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, Int64List x):
        cdef int64_t *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <int64_t *>PyMem_Realloc(self._data, new_size * sizeof(int64_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, int64_t x):
        cdef int64_t *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <int64_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(int64_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, int64_t x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class Uint64List:

    def __cinit__(self, size_t size=16):
        self._data = <uint64_t *>PyMem_Malloc(size * sizeof(uint64_t))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, uint64_t x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, uint64_t x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, uint64_t x):
        cdef uint64_t *mem

        if self._n_items == self._size:
            mem = <uint64_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(uint64_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, Uint64List x):
        cdef uint64_t *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <uint64_t *>PyMem_Realloc(self._data, new_size * sizeof(uint64_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, uint64_t x):
        cdef uint64_t *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <uint64_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(uint64_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, uint64_t x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class CharList:

    def __cinit__(self, size_t size=16):
        self._data = <char *>PyMem_Malloc(size * sizeof(char))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, char x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, char x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, char x):
        cdef char *mem

        if self._n_items == self._size:
            mem = <char *>PyMem_Realloc(self._data, 2 * self._size * sizeof(char))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, CharList x):
        cdef char *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <char *>PyMem_Realloc(self._data, new_size * sizeof(char))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, char x):
        cdef char *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <char *>PyMem_Realloc(self._data, 2 * self._size * sizeof(char))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, char x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class Int32List:

    def __cinit__(self, size_t size=16):
        self._data = <int32_t *>PyMem_Malloc(size * sizeof(int32_t))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, int32_t x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, int32_t x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, int32_t x):
        cdef int32_t *mem

        if self._n_items == self._size:
            mem = <int32_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(int32_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, Int32List x):
        cdef int32_t *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <int32_t *>PyMem_Realloc(self._data, new_size * sizeof(int32_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, int32_t x):
        cdef int32_t *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <int32_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(int32_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, int32_t x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class IntList:

    def __cinit__(self, size_t size=16):
        self._data = <int *>PyMem_Malloc(size * sizeof(int))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, int x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, int x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, int x):
        cdef int *mem

        if self._n_items == self._size:
            mem = <int *>PyMem_Realloc(self._data, 2 * self._size * sizeof(int))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, IntList x):
        cdef int *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <int *>PyMem_Realloc(self._data, new_size * sizeof(int))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, int x):
        cdef int *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <int *>PyMem_Realloc(self._data, 2 * self._size * sizeof(int))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, int x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class DoubleList:

    def __cinit__(self, size_t size=16):
        self._data = <double *>PyMem_Malloc(size * sizeof(double))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, double x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, double x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, double x):
        cdef double *mem

        if self._n_items == self._size:
            mem = <double *>PyMem_Realloc(self._data, 2 * self._size * sizeof(double))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, DoubleList x):
        cdef double *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <double *>PyMem_Realloc(self._data, new_size * sizeof(double))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, double x):
        cdef double *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <double *>PyMem_Realloc(self._data, 2 * self._size * sizeof(double))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, double x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class FloatList:

    def __cinit__(self, size_t size=16):
        self._data = <float *>PyMem_Malloc(size * sizeof(float))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, float x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, float x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, float x):
        cdef float *mem

        if self._n_items == self._size:
            mem = <float *>PyMem_Realloc(self._data, 2 * self._size * sizeof(float))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, FloatList x):
        cdef float *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <float *>PyMem_Realloc(self._data, new_size * sizeof(float))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, float x):
        cdef float *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <float *>PyMem_Realloc(self._data, 2 * self._size * sizeof(float))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, float x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1



cdef class Uint32List:

    def __cinit__(self, size_t size=16):
        self._data = <uint32_t *>PyMem_Malloc(size * sizeof(uint32_t))
        if not self._data:
            raise MemoryError()

        self._n_items = 0
        self._size = size

    def __dealloc__(self):
        PyMem_Free(self._data)

    def __contains__(self, uint32_t x):
        cdef int i
        for i in range(self._n_items):
            if self._data[i] == x:
                return True

        return False

    def __delitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        cdef int j
        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]

        self._n_items -= 1

    def __getitem__(self, int i):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        return self._data[i]

    def __iter__(self):
        cdef size_t idx = 0
        while idx < self._n_items:
            yield self._data[idx]
            idx += 1

    def __len__(self):
        return self._n_items

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, int i, uint32_t x):
        if i < 0:
            i += self._n_items

        if i >= self._n_items or i < 0:
            raise IndexError("list index out of range")

        self._data[i] = x

    def __str__(self):
        return str(list(self))

    cpdef append(self, uint32_t x):
        cdef uint32_t *mem

        if self._n_items == self._size:
            mem = <uint32_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(uint32_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        self._data[self._n_items] = x
        self._n_items += 1

    cpdef extend(self, Uint32List x):
        cdef uint32_t *mem
        cdef size_t new_len = self._n_items + len(x)
        cdef size_t new_size
        cdef size_t i

        if new_len > self._size:
            new_size = max(new_len, 2 * self._size)
            mem = <uint32_t *>PyMem_Realloc(self._data, new_size * sizeof(uint32_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size = new_size

        for i in range(len(x)):
            self._data[self._n_items + i] = x[i]

        self._n_items = new_len

    cpdef insert(self, int i, uint32_t x):
        cdef uint32_t *mem
        cdef int j

        if i < 0:
            i += self._n_items

        if i > self._n_items or i < 0:
            raise IndexError("list index out of range")

        if self._n_items == self._size:
            mem = <uint32_t *>PyMem_Realloc(self._data, 2 * self._size * sizeof(uint32_t))
            if not mem:
                raise MemoryError()

            self._data = mem
            self._size *= 2

        for j in range(self._n_items, i, -1):
            self._data[j] = self._data[j - 1]

        self._data[i] = x
        self._n_items += 1

    cpdef pop(self):
        if self._n_items == 0:
            raise IndexError("pop from empty list")

        self._n_items -= 1
        return self._data[self._n_items]

    cpdef remove(self, uint32_t x):
        cdef int i
        cdef int j
        cdef bint found = 0

        for i in range(self._n_items):
            if self._data[i] == x:
                found = 1
                break

        if found == 0:
            raise ValueError("x not in list")

        for j in range(i, self._n_items):
            self._data[j] = self._data[j + 1]
        
        self._n_items -= 1

