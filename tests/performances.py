import os
import sys
import time

from create_message import *


HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')
lib_path = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                if name.startswith('lib')].pop())
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

GOOGLE = True

try:
    import messages.test_message_pb2 as google_test
except ImportError:
    GOOGLE = False

import test_message_proto as an_test


def main():
    if GOOGLE:
        t1 = create_google_test()

    t2 = create_an_test()
    buf = ""

    if GOOGLE:
        start = time.time()
        for i in range(100000):
            buf = t1.SerializeToString()

        end = time.time()
        print("Google took %f seconds to serialize" % (end - start))

    start = time.time()
    for i in range(100000):
        buf = t2.SerializeToString()

    end = time.time()
    print("Pyrobuf took %f seconds to serialize" % (end - start))

    if GOOGLE:
        start = time.time()
        for i in range(100000):
            t1.ParseFromString(buf)

        end = time.time()
        print("Google took %f seconds to deserialize" % (end - start))

    start = time.time()
    for i in range(100000):
        t2.ParseFromString(buf)

    end = time.time()
    print("Pyrobuf took %f seconds to deserialize" % (end - start))

    start = time.time()
    for i in range(100000):
        assert t2.HasField('field')
        assert t2.HasField('string_field')

    end = time.time()
    print("HasField took %f seconds" % (end - start))


if __name__ == "__main__":
    main()
