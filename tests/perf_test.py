import time

import messages.test_message_pb2 as google_test
import test_message_proto as an_test

from create_message import *

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
