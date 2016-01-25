import os

import pytest

from pyrobuf.__main__ import gen_message


HERE = os.path.dirname(os.path.abspath(__file__))
FIRST = ['test_ref_message.proto', 'test_message.proto']
PROTO = [os.path.join(HERE, 'proto', filename) for filename in FIRST]
PROTO.extend(os.path.join(HERE, 'proto', filename)
             for filename in os.listdir(os.path.join(HERE, 'proto'))
             if filename not in FIRST)

@pytest.mark.parametrize('proto', PROTO)
def test_gen_all_message(proto):
    gen_message(proto, out='tests/out', build='tests/build')
