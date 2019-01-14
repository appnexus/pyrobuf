import time
from array import array

from pyrobuf_list import *


def main():
    start = time.time()
    x = []
    y = 0

    for i in range(1000000):
        x.append(float(i))

    for i in x:
        y += i

    end = time.time()
    print("list took %f seconds" % (end - start))

    start = time.time()
    x = TypedList(float)
    y = 0

    for i in range(1000000):
        x.append(float(i))

    for i in x:
        y += i

    end = time.time()
    print("TypedList took %f seconds" % (end - start))

    start = time.time()
    x = DoubleList()
    y = 0

    for i in range(1000000):
        x.append(float(i))

    for i in x:
        y += i

    end = time.time()
    print("DoubleList took %f seconds" % (end - start))

    start = time.time()
    x = FloatList()
    y = 0

    for i in range(1000000):
        x.append(float(i))

    for i in x:
        y += i

    end = time.time()
    print("FloatList took %f seconds" % (end - start))

    start = time.time()
    x = array('f')
    y = 0

    for i in range(1000000):
        x.append(float(i))

    for i in x:
        y += i

    end = time.time()
    print("array 'f' took %f seconds" % (end - start))

    start = time.time()
    x = array('d')
    y = 0

    for i in xrange(1000000):
        x.append(float(i))

    for i in x:
        y += i

    end = time.time()
    print("array 'd' took %f seconds" % (end - start))

    start = time.time()
    x = []
    y = 0

    for i in range(1000000):
        x.append(i)

    for i in x:
        y += i

    end = time.time()
    print("list took %f seconds" % (end - start))

    start = time.time()
    x = IntList()
    y = 0

    for i in range(1000000):
        x.append(i)

    for i in x:
        y += i

    end = time.time()
    print("IntList took %f seconds" % (end - start))

    start = time.time()
    x = Int32List()
    y = 0

    for i in range(1000000):
        x.append(i)

    for i in x:
        y += i

    end = time.time()
    print("Int32List took %f seconds" % (end - start))

    start = time.time()
    x = array('i')
    y = 0

    for i in range(1000000):
        x.append(i)

    for i in x:
        y += i

    end = time.time()
    print("array 'i' took %f seconds" % (end - start))


if __name__ == "__main__":
    main()
