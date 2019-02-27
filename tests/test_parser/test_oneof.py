from pyrobuf.parse_proto import Parser

proto_def = """
syntax = "proto3";

message LBService {
  // Virtual IP used by clients to reach the service behind load balancers.
  string vip = 1;

  oneof ServiceName {
    // URL used by clients to reach service behind load balancers.
    string url = 2;

    // Service name if a non-standard mechanism is used for service discovery.
    string name = 3;
  }
}
"""


class TestOneOf(object):

    def test_oneof(self):
        result = Parser(proto_def).parse()
        message = result['messages'][0]

        # assert that all field are listed in the message
        assert [f.name for f in message.fields.values()] == ['vip', 'url', 'name']

        # assert that the oneofs list their child field names
        assert len(message.oneofs) == 1
        assert 'ServiceName' in message.oneofs
        assert message.oneofs['ServiceName'].fields == ['url', 'name']

