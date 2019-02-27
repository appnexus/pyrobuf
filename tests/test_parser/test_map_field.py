import pytest

from pyrobuf.parse_proto import Parser


map_field_with_enum = """
syntax = "proto3";


enum IPAddressFamily {
  INVALID = 0;
  IPv4 = 1;
  IPv6 = 2;
};

message TenantNetworkPolicy {
  string tenant_name = 1;
  map<int, IPAddressFamily> scopes = 2;
}
"""

map_field_with_message = """
syntax = "proto3";


message ScopeInfo {
  string id = 1;
}

message TenantNetworkPolicy {
  string tenant_name = 1;
  map<string, ScopeInfo> scopes = 2;
}
"""

map_field_with_builtin_types = """
syntax = "proto3";

message TenantNetworkPolicy {
  string tenant_name = 1;
  map<int, string> scopes = 2;
}
"""


class TestMapField(object):

    @staticmethod
    def parsing_result(string):
        return Parser(string).parse()

    def test_map_field_with_message(self):
        result = self.parsing_result(map_field_with_message)
        message = result['messages'][1]

        # assert that all field are listed in the message
        assert [f.name for f in message.fields.values()] == ['tenant_name', 'scopes']

        # assert things about the scope map field
        scopes_field = message.fields[2]
        assert scopes_field.name == 'scopes'
        assert scopes_field.token_type == 'MAP_FIELD'
        assert scopes_field.key_type == 'string'
        # Validate the map value type
        assert scopes_field.type == 'message'
        assert scopes_field.message_name == 'ScopeInfo'

    def test_map_field_with_enum(self):
        result = self.parsing_result(map_field_with_enum)
        message = result['messages'][0]

        # assert that all field are listed in the message
        assert [f.name for f in message.fields.values()] == ['tenant_name', 'scopes']

        # assert things about the ips map field
        scopes_field = message.fields[2]
        assert scopes_field.name == 'scopes'
        assert scopes_field.token_type == 'MAP_FIELD'
        assert scopes_field.key_type == 'int'
        assert scopes_field.type == 'enum'
        assert scopes_field.enum_def == result['enums'][0]

    def test_map_field_with_builtin_types(self):
        result = self.parsing_result(map_field_with_builtin_types)
        message = result['messages'][0]

        # assert that all field are listed in the message
        assert [f.name for f in message.fields.values()] == ['tenant_name', 'scopes']

        # assert things about the ips map field
        scopes_field = message.fields[2]
        assert scopes_field.name == 'scopes'
        assert scopes_field.token_type == 'MAP_FIELD'
        assert scopes_field.key_type == 'int'
        assert scopes_field.type == 'string'

