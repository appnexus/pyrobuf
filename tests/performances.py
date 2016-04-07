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

import messages.test_message_pb2 as google_test
import test_message_proto as an_test


def main():
    t1 = create_google_test()
    t2 = create_an_test()

    buf1 = ""
    buf2 = bytearray()

    start = time.time()
    for i in xrange(100000):
        buf1 = t1.SerializeToString()
    
    end = time.time()
    print("Google took %f seconds to serialize" % (end - start))

    start = time.time()
    for i in xrange(100000):
        buf2 = t2.SerializeToString()

    end = time.time()
    print("Pyrobuf took %f seconds to serialize" % (end - start))

    start = time.time()
    for i in xrange(100000):
        t1.ParseFromString(buf1)

    end = time.time()
    print("Google took %f seconds to deserialize" % (end - start))

    start = time.time()
    for i in xrange(100000):
        t2.ParseFromString(buf1)

    end = time.time()
    print("Pyrobuf took %f seconds to deserialize" % (end - start))

if __name__ == "__main__":
    main()
