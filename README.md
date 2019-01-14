# Pyrobuf Library

### Introduction

Pyrobuf is an alternative to Google's Python Protobuf library.

It generates lightning-fast Cython code that's 2-4x faster than Google's Python
Protobuf library using their C++ backend and 20-40x faster than Google's pure-python
implementation.

What's more, Pyrobuf is self-contained and easy to install.


### Requirements

Pyrobuf requires Cython, and Jinja2. If you want to contribute to pyrobuf you
may also want to install pytest.

Pyrobuf *does not* require protoc.

Pyrobuf has been tested with Python 2.7 and Python 3.5.

Pyrobuf appears to be working on OSX, Linux and Windows (for the latter getting
Cython to work properly is the trickiest bit especially if you are still using
2.7).


### Contributing

People use protobuf in many different ways. Pyrobuf handles the use cases of
AppNexus and other contributors, but is not yet a 100% drop-in replacement to
what protoc would generate.

You can help make it so!

Fork and clone the repository, then run:

    $ python setup.py develop

It will generate the platform specific `pyrobuf_list` then compile
the `pyrobuf_list` and `pyrobuf_util` modules.


### Unit Testing

You can run the test suite (a work in progress) using py.test directly:

    $ py.test

Or using the `test` command (which installs pytest if not already available):

    $ python setup.py test

Either method will automatically build all the protobuf message specs in
`tests/proto` and point the `PYTHONPATH` to the built messages before running
the tests.

Re-running the `develop` or `test` commands will automatically re-build the
`pyrobuf_list` and `pyrobuf_util` modules if necessary.

The `clean` command does the house keeping for you:

    $ python setup.py clean

If you find that pyrobuf does not work for one of your proto files, add a minimal
proto file to `tests/proto` that breaks before submitting a pull request.

Pull requests including a breaking test are gold!

Improving testing is in the cards.


### Installation

You may very well be able to just use pyrobuf as is... just pip it!

```
$ pip install pyrobuf
```
Should do the trick!

To check, you may want to make sure the following command does not raise an
exception:

    $ python -c "import pyrobuf_list"

If it does raise an exception try:

```
$ pip install pyrobuf -v -v -v --upgrade --force --no-cache
```


### Compiling

When you `pip install pyrobuf` you get the pyrobuf CLI tool ...:

    $ pyrobuf --help
    usage: pyrobuf [-h] [--out-dir OUT_DIR] [--build-dir BUILD_DIR] [--install]
                   source

    a Cython based protobuf compiler

    positional arguments:
      source                filename.proto or directory containing proto files

    optional arguments:
      -h, --help            show this help message and exit
      --out-dir OUT_DIR     cythonize output directory [default: out]
      --build-dir BUILD_DIR
                            C compiler build directory [default: build]
      --install             install the extension [default: False]
      --package             the name of the package to install to

If you do not want to have to deal with setuptools entry_points idiosyncrasies
you can also do:

    $ python -m pyrobuf --help


### Use

Suppose you have installed `test_message.proto` which contains a spec for the
message `Test`. In Python, you can import your new message class by running:
```
from test_message_proto import Test
```

With the message class imported, we can create a new message:
```
test = Test()
```

Now that we have instantiated a message `test`, we can fill individual fields:
```
>>> test.field = 5
>>> test.req_field = 2
>>> test.string_field = "hello!"
>>> test.list_fieldx.append(12)
>>> test.test_ref.field2 = 3.14
```

And access those same fields:
```
>>> test.string_field
'hello!'
```

Once we have at least filled out any "required" fields, we can serialize to a
byte array:
```
>>> test.SerializeToString()
bytearray(b'\x10\x05\x1a\x06hello! \x0c2\t\x19\x1f\x85\xebQ\xb8\x1e\t@P\x02')
```

We can also deserialize a protobuf message to our message instance:
```
>>> test.ParseFromString('\x10\x05\x1a\x06hello! \x0c2\t\x19\x1f\x85\xebQ\xb8\x1e\t@P\x02')
25
```
Note that the `ParseFromString` method returns the number of bytes consumed.

In addition to serializing and deserializing to and from protobuf messages,
Pyrobuf also allows us to serialize and deserialize to and from JSON and native
Python dictionaries:
```
>>> test.SerializeToJson()
'{"field": 5, "req_field": 2, "list_fieldx": [12], "string_field": "hello!", "test_ref": {"field2": 3.14}}'

>>> test.ParseFromJson('{"field": 5, "req_field": 2, "list_fieldx": [12], "string_field": "hello!", "test_ref": {"field2": 3.14}}')

>>> test.SerializeToDict()
{'field': 5,
 'list_fieldx': [12],
 'req_field': 2,
 'string_field': 'hello!',
 'test_ref': {'field2': 3.14}}

>>> test.ParseFromDict({'field': 5, 'list_fieldx': [12], 'req_field': 2, 'string_field': 'hello!', 'test_ref': {'field2': 3.14}})
```

Finally, the `pyrobuf_util` module contains functions for encoding and decoding integers.

```
>>> import pyrobuf_util
>>> pyrobuf_util.to_varint(2**16-1)
bytearray(b'\xff\xff\x03')
>>> pyrobuf_util.from_varint(b'\xff\xff\x03', offset=0)
(65535L, 3)
>>> pyrobuf_util.to_signed_varint(-2**16)
bytearray(b'\xff\xff\x07')
>>> pyrobuf_util.from_signed_varint(b'\xff\xff\x07', offset=0)
(-65536L, 3)
```

The `from_varint` and `from_signed_varint` functions return both the decoded integer and
the offset of the first byte after the encoded integer in the source data.

### Packaging

If you are compiling multiple messages or a directory of messages and don't want them
all to be built to their own separate package but instead want a single namespace
containing all your messages, you can specify a package name:
```
pyrobuf /path/to/proto/specs --install --package=my_messages
```

Then you can import your message classes from the `my_messages` pakcage:
```
>>> from my_messages import MyMessage1, MyMessage2
```

### Distributing a Python Package with Pyrobuf Modules

Suppose you have a Python package called 'sample' arranged on disk as follows:
```
sample/
    proto/
        my_message.proto
    sample/
        __init__.py
    setup.py
```

Pyrobuf adds a new setup keyword `pyrobuf_modules` which can be used to specify either
individual protobuf files or folders containing protobuf files. For example, the `setup.py`
file could look like this:
 
```
from setuptools import setup, find_packages

setup(
    name="sample",
    version="0.1",
    packages=find_packages(),
    description="A sample package",
    install_requires=['pyrobuf'],
    setup_requires=['pyrobuf'],
    pyrobuf_modules="proto"
)
```

In addition to the package "sample", setuptools will also build a package named
"sample_proto" which will contain the compiled Protobuf messages.

Once installed this sample package can be used as follows:

```
>>> from sample_proto import MyMessage
>>> my_message = MyMessage()
```

### Performance

On my development machine (Ubuntu 14.04), Pyrobuf is roughly 2.0x as fast as
Google's library for message serialization and 2.3x as fast for message
deserialization when using the C++ backend for Google's library:
```
> python tests/perf_test.py
Google took 1.649168 seconds to serialize
Pyrobuf took 0.825525 seconds to serialize
Google took 1.113041 seconds to deserialize
Pyrobuf took 0.466113 seconds to deserialize
```

When not using the C++ backend, Pyrobuf is roughly 25x as fast for serialization
and 55x as fast for deserialization:
```
Google took 20.215662 seconds to serialize
Pyrobuf took 0.819555 seconds to serialize
Google took 24.990137 seconds to deserialize
Pyrobuf took 0.455732 seconds to deserialize
```

### Differences from the Google library

If pyrobuf is missing a feature from protoc that you need, let us know! We are
trying to make it as easy as possible for you to help make pyrobuf better.

For the most part, Pyrobuf should be a drag-and-drop replacement for the Google
protobuf library. There are a few differences, though. First, Pyrobuf does not
currently implement the `ListFields`, `WhichOneOf`, `HasExtension`,
`ClearExtension` and `ByteSize` methods.

Second, Pyrobuf simply assumes that the schema being used for a given message
is the same on the send and receive ends, so changing the type of a field on
one end without changing it on the other may cause bugs; adding or removing
fields will not break anything.
