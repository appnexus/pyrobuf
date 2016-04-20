import os
import re


class Parser(object):

    tokens = {
        'COMMENT_OL': r'\/\/.*?\n',
        'COMMENT_ML': r'\/\*(?:.|[\r\n])*?\*\/',
        'OPTION': r'option\s+(.*?);',
        'IMPORT': r'import\s+"(.+?).proto"[ ]*;',
        'MESSAGE': r'message\s+([A-Z][0-9A-Za-z]*)',
        'FIELD': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+);',
        'FIELD_WITH_DEFAULT': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[\s*default\s*=\s*([0-9A-Za-z][0-9A-Za-z_]*|-?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')\s*\];',
        'FIELD_PACKED': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[packed\s*=\s*true\];',
        'FIELD_DEPRECATED': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[deprecated\s*=\s*true\];',
        'ENUM': r'enum\s+([A-Za-z_][0-9A-Za-z_]*)',
        'ENUM_FIELD': r'([A-Za-z_][0-9A-Za-z_]*);',
        'ENUM_FIELD_WITH_VALUE': r'([A-Za-z_][0-9A-Za-z_]*)\s*=\s*(-\d+|\d+|0x[0-9A-Fa-f]+);',
        'LBRACE': r'\{',
        'RBRACE': r'\}',
        'SKIP': r'[ \t]',
        'NEWLINE': r'[\r\n]',
        'PACKAGE': r'package\s.*;'
    }

    scalars = (
        'double', 'float', 'int32', 'int64', 'uint32', 'uint64', 'sint32', 'sint64',
        'fixed32', 'fixed64', 'sfixed32', 'sfixed64', 'bool', 'enum', 'timestamp'
    )

    list_type_map = {
        'float':    'FloatList',
        'double':   'DoubleList',
        'enum':     'Int32List',
        'int32':    'Int32List',
        'sint32':   'Int32List',
        'sfixed32': 'Int32List',
        'uint32':   'Uint32List',
        'fixed32':  'Uint32List',
        'bool':     'Uint32List',
        'int64':    'Int64List',
        'sint64':   'Int64List',
        'sfixed64': 'Int64List',
        'uint64':   'Uint64List',
        'fixed64':  'Uint64List',
        'string':   'StringList',
        'bytes':    'BytesList'
    }

    c_type_map = {
        'float':    'float',
        'double':   'double',
        'int32':    'int32_t',
        'sint32':   'int32_t',
        'sfixed32': 'int32_t',
        'uint32':   'uint32_t',
        'fixed32':  'uint32_t',
        'int64':    'int64_t',
        'sint64':   'int64_t',
        'sfixed64': 'int64_t',
        'uint64':   'uint64_t',
        'fixed64':  'uint64_t',
        'bool':     'uint32_t',
        'enum':     'int32_t',
        'timestamp':'uint32_t'
    }

    getter_map = {
        'bool':     'get_varint32',
        'enum':     'get_varint32',
        'int32':    'get_varint32',
        'sint32':   'get_signed_varint32',
        'uint32':   'get_varint32',
        'int64':    'get_varint64',
        'sint64':   'get_signed_varint64',
        'uint64':   'get_varint64'
    }

    setter_map = {
        'bool':     'set_varint32',
        'enum':     'set_varint32',
        'int32':    'set_varint32',
        'sint32':   'set_signed_varint32',
        'uint32':   'set_varint32',
        'int64':    'set_varint64',
        'sint64':   'set_signed_varint64',
        'uint64':   'set_varint64'
    }

    def __init__(self):
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.tokens.items())
        self.get_token = re.compile(token_regex).match
        self.token_getter = {key: re.compile(val).match for key, val in self.tokens.items()}

    def tokenize(self, s):
        pos = 0
        line = 1

        m = self.get_token(s, pos)
        while m is not None:
            token_type = m.lastgroup
            subm = self.token_getter[token_type](m.group(token_type))
            vals = subm.groups()

            if token_type == 'OPTION':
                yield ParserOption(pos, *vals)

            elif token_type == 'IMPORT':
                yield ParserImport(pos, *vals)

            elif token_type == 'MESSAGE':
                yield ParserMessage(pos, *vals)

            elif token_type in ('FIELD', 'FIELD_WITH_DEFAULT'):
                yield ParserField(pos, *vals)

            elif token_type == 'FIELD_PACKED':
                yield ParserFieldPacked(pos, *vals)

            elif token_type == 'FIELD_DEPRECATED':
                yield ParserFieldDeprecated(pos, *vals)

            elif token_type == 'ENUM':
                yield ParserEnum(pos, *vals)

            elif token_type in ('ENUM_FIELD', 'ENUM_FIELD_WITH_VALUE'):
                yield ParserEnumField(pos, *vals)

            elif token_type == 'LBRACE':
                yield ParserLBrace(pos)

            elif token_type == 'RBRACE':
                yield ParserRBrace(pos)

            elif token_type == 'NEWLINE':
                line += 1

            pos = m.end()
            m = self.get_token(s, pos)

        if pos != len(s):
            raise Exception("Unexpected character '%s' in line %d: '%s'" % (s[pos], line, s[pos-10:pos+10]))

    def parse(self, s, cython_info=True, fname=''):
        tokens = self.tokenize(s)
        rep = {'imports': [], 'messages': [], 'enums': []}
        enums = {}
        imported = {'messages': {}, 'enums': {}}

        for token in tokens:
            if token.token_type == 'OPTION':
                continue

            elif token.token_type == 'IMPORT':
                rep['imports'].append(token.value)

                # Google's protoc only supports the use of messages and enums from direct imports.
                # So messages and enums from indirect imports are not fetched here.
                imported_rep = self._parse_import(token.value + '.proto', fname)
                imported['messages'].update((m.name, m) for m in imported_rep['messages'])
                imported['enums'].update((e.name, e) for e in imported_rep['enums'])

            elif token.token_type == 'MESSAGE':
                rep['messages'].append(self._parse_message(s, token, tokens, enums, imported['enums']))

            elif token.token_type == 'ENUM':
                ret = self._parse_enum(s, token, tokens)
                rep['enums'].append(ret)
                enums[token.name] = token

            else:
                raise Exception("unexpected %s token at character %d: '%s'" % (token.typ, token.pos, s[token.pos:token.pos+10]))

        if cython_info:
            for message in rep['messages']:
                self.add_cython_info(message)

        return rep

    def parse_from_filename(self, fname):
        with open(fname, 'r') as fp:
            s = fp.read()

        return self.parse(s, fname=fname)

    def _parse_import(self, fname, parent_fname):
        i_parser = Parser()
        actual_fname = fname if os.path.isabs(fname) else os.path.join(os.path.dirname(parent_fname), fname)
        rep = i_parser.parse_from_filename(actual_fname)
        return rep

    def _parse_message(self, s, current, tokens, enums, imported_enums):
        token = next(tokens)
        try:
            assert token.token_type == 'LBRACE'
        except AssertionError:
            raise Exception("missing opening paren at pos %d: '%s'" % (token.pos, s[token.pos:token.pos+10]))

        for token in tokens:
            if token.token_type == 'MESSAGE':
                current.messages[token.name] = self._parse_message(s, token, tokens, enums, imported_enums)

            elif token.token_type == 'ENUM':
                current.enums[token.name] = self._parse_enum(s, token, tokens)

            elif token.token_type == 'FIELD':
                if current.messages.get(token.type) is not None:
                    token.message_def = current.messages[token.type]
                    token.message_name = token.type
                    token.type = 'message'
                    token.is_nested = True

                elif current.enums.get(token.type) is not None:
                    if token.default is not None:
                        for entry in current.enums[token.type].fields:
                            if token.default == entry.name:
                                default = entry.value
                                enum_default = entry.name
                                break

                        token.default = default
                        token.enum_default = enum_default

                    token.is_nested = True
                    token.enum_def = current.enums[token.type]
                    token.enum_name = token.type
                    token.type = 'enum'

                elif enums.get(token.type) is not None:
                    if token.default is not None:
                        for entry in enums[token.type].fields:
                            if token.default == entry.name:
                                default = entry.value
                                enum_default = entry.name
                                break

                        token.default = default
                        token.enum_default = enum_default

                    token.is_nested = False
                    token.enum_def = enums[token.type]
                    token.enum_name = token.type
                    token.type = 'enum'

                elif imported_enums.get(token.type) is not None:
                    if token.default is not None:
                        for entry in imported_enums[token.type].fields:
                            if token.default == entry.name:
                                default = entry.value
                                enum_default = entry.name
                                break

                        token.default = default
                        token.enum_default = enum_default

                    token.is_nested = False
                    token.enum_def = imported_enums[token.type]
                    token.enum_name = token.type
                    token.type = 'enum'

                elif (token.type not in self.scalars) and (token.type not in ('string', 'bytes')):
                    token.message_name = token.type
                    token.type = 'message'
                    token.is_nested = False

                current.fields.append(token)

            elif token.token_type == 'RBRACE':
                return current

            else:
                raise Exception("unexpected %s token at character %d: '%s'" % (token.typ, token.pos, s[token.pos:token.pos+10]))

        raise Exception("unexpected EOF at character %d: '%s'" % (token.pos, s[token.pos:token.pos+10]))

    def _parse_enum(self, s, current, tokens):
        token = next(tokens)
        try:
            assert token.token_type == 'LBRACE'
        except AssertionError:
            raise Exception("missing opening paren at pos %d: '%s'" % (token.pos, s[token.pos:token.pos+10]))

        for token in tokens:
            if token.token_type == 'ENUM_FIELD':
                current.fields.append(token)

            elif token.token_type == 'RBRACE':
                return current

            else:
                raise Exception("unexpected %s token at character %d: '%s'" % (token.typ, token.pos, s[token.pos:token.pos+10]))

        raise Exception("unexpected EOF at character %d: '%s'" % (token.pos, s[token.pos:token.pos+10]))

    def add_cython_info(self, message):
        for field in message.fields:
            field.list_type = self.list_type_map.get(field.type, 'TypedList')
            field.fixed_width = (field.type in ('float', 'double', 'fixed32', 'sfixed32', 'fixed64', 'sfixed64'))
            field.var_width = (field.type in ('bool', 'enum', 'int32', 'sint32', 'uint32', 'int64', 'sint64', 'uint64'))

            if field.type in self.scalars:
                field.c_type = self.c_type_map[field.type]

            if field.var_width:
                field.getter = self.getter_map[field.type]
                field.setter = self.setter_map[field.type]

        for submessage in message.messages.values():
            self.add_cython_info(submessage)


class ParserOption(object):
    def __init__(self, pos, option):
        self.token_type = 'OPTION'
        self.pos = pos
        self.option = option


class ParserImport(object):
    def __init__(self, pos, value):
        self.token_type = 'IMPORT'
        self.pos = pos
        self.value = value


class ParserMessage(object):
    def __init__(self, pos, name):
        self.token_type = 'MESSAGE'
        self.pos = pos
        self.name = name
        self.messages = {}
        self.enums = {}
        self.fields = []


class ParserField(object):
    def __init__(self, pos, modifier, ftype, name, index, default=None):
        self.token_type = 'FIELD'
        self.pos = pos
        self.modifier = modifier
        self.type = ftype
        self.name = name
        self.index = int(index)
        self.default = process_default(default)
        self.packed = False
        self.deprecated = False


def process_default(default):
    if default == 'true':
        return True
    elif default == 'false':
        return False
    else:
        return default


class ParserFieldPacked(object):
    def __init__(self, pos, modifier, ftype, name, index):
        self.token_type = 'FIELD'
        self.pos = pos
        self.modifier = modifier
        self.type = ftype
        self.name = name
        self.index = int(index)
        self.default = None
        self.packed = True
        self.deprecated = False


class ParserFieldDeprecated(object):
    def __init__(self, pos, modifier, ftype, name, index):
        self.token_type = 'FIELD'
        self.pos = pos
        self.modifier = modifier
        self.type = ftype
        self.name = name
        self.index = int(index)
        self.default = None
        self.packed = False
        self.deprecated = True


class ParserEnum(object):
    def __init__(self, pos, name):
        self.token_type = 'ENUM'
        self.pos = pos
        self.name = name
        self.fields = []


class ParserEnumField(object):
    def __init__(self, pos, name, value=None):
        self.token_type = 'ENUM_FIELD'
        self.pos = pos
        self.name = name
        if value is not None:
            self.value = int(value, 0)
        else:
            self.value = None


class ParserLBrace(object):
    def __init__(self, pos):
        self.token_type = 'LBRACE'
        self.pos = pos


class ParserRBrace(object):
    def __init__(self, pos):
        self.token_type = 'RBRACE'
        self.pos = pos
