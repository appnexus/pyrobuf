import os
import re


class Parser(object):

    syntax = 2

    # Tokens ordered roughly by priority
    tokens = [
        ('COMMENT_OL', r'\/\/.*?\n'),
        ('COMMENT_ML', r'\/\*(?:.|[\r\n])*?\*\/'),
        ('OPTION', r'option\s+((?:.|[\n\r])*?);'),
        ('IMPORT', r'import\s+"(.+?).proto"\s*;'),
        ('MESSAGE', r'message\s+([A-Za-z_][0-9A-Za-z_]*)'),
        ('ENUM', r'enum\s+([A-Za-z_][0-9A-Za-z_]*)'),
        ('PACKAGE', r'package\s+[A-Za-z_][0-9A-Za-z_\.]*\s*;'),
        ('SYNTAX', r'syntax\s*=\s*"(.*?)"\s*;'),
        ('EXTEND', r'extend\s+([A-Za-z_][0-9A-Za-z_\.]*)'),
        ('EXTENSION', r'extensions\s+(\d+)\s+to\s+(\d+|max)\s*;'),
        ('ONEOF', r'oneof\s+([A-Za-z_][0-9A-Za-z_]*)'),
        ('MODIFIER', r'(optional|required|repeated)'),
        ('FIELD', r'([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*='
                  r'\s*(\d+)'),
        ('DEFAULT', r'default\s*=\s*([A-Za-z][0-9A-Za-z_]*|-?[0-9]*\.?[0-9]+'
                    r'(?:[eE][-+]?[0-9]+)?|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*'
                    r'\')'),
        ('PACKED', r'packed\s*=\s*(true|false)'),
        ('DEPRECATED', r'deprecated\s*=\s*(true|false)'),
        ('GENERIC', r'(\([A-Za-z][0-9A-Za-z_]*\).[A-Za-z][0-9A-Za-z_]*)\s*='
                    r'\s*([^\]]+)'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]\s*;'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}\s*;{0,1}'),
        ('COMMA', r','),
        ('SKIP', r'\s'),
        ('SEMICOLON', r';'),
        ('ENUM_FIELD_WITH_VALUE', r'([A-Za-z_][0-9A-Za-z_]*)\s*='
                                  r'\s*(0x[0-9A-Fa-f]+|-\d+|\d+)'),
        ('ENUM_FIELD', r'([A-Za-z_][0-9A-Za-z_]*)')
    ]

    scalars = {
        'double', 'float', 'int32', 'int64', 'uint32', 'uint64', 'sint32',
        'sint64', 'fixed32', 'fixed64', 'sfixed32', 'sfixed64', 'bool', 'enum',
        'timestamp'
    }

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

    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in tokens)
    get_token = re.compile(token_regex).match
    token_getter = {key: re.compile(val).match for key, val in tokens}

    def __init__(self, string):
        self.string = string
        self.lines = string.split('\n')

    def tokenize(self):
        pos = 0
        line = 0

        m = self.get_token(self.string, pos)
        while m is not None:
            token_type = m.lastgroup
            subm = self.token_getter[token_type](m.group(token_type))
            vals = subm.groups()

            if token_type == 'OPTION':
                yield self.Option(line, *vals)

            elif token_type == 'SYNTAX':
                yield self.Syntax(line, *vals)

            elif token_type == 'IMPORT':
                yield self.Import(line, *vals)

            elif token_type == 'MESSAGE':
                yield self.Message(line, *vals)

            elif token_type == 'MODIFIER':
                yield self.Modifier(line, *vals)

            elif token_type == 'FIELD':
                yield self.Field(line, *vals)

            elif token_type == 'LBRACKET':
                yield self.LBracket(line)

            elif token_type == 'RBRACKET':
                yield self.RBracket(line)

            elif token_type == 'DEFAULT':
                yield self.Default(line, *vals)

            elif token_type == 'PACKED':
                yield self.Packed(line, *vals)

            elif token_type == 'DEPRECATED':
                yield self.Deprecated(line, *vals)

            elif token_type == 'CUSTOM':
                yield self.Custom(line, *vals)

            elif token_type == 'COMMA':
                yield self.Comma(line)

            elif token_type == 'SEMICOLON':
                yield self.Semicolon(line)

            elif token_type == 'ENUM':
                yield self.Enum(line, *vals)

            elif token_type in {'ENUM_FIELD', 'ENUM_FIELD_WITH_VALUE'}:
                yield self.EnumField(line, *vals)

            elif token_type == 'LBRACE':
                yield self.LBrace(line)

            elif token_type == 'RBRACE':
                yield self.RBrace(line)

            elif token_type == 'EXTENSION':
                yield self.Extension(line, *vals)

            elif token_type == 'ONEOF':
                yield self.Oneof(line, *vals)

            elif token_type == 'EXTEND':
                yield self.Extend(line, *vals)

            line += subm.group().count('\n')
            pos = m.end()
            m = self.get_token(self.string, pos)

        if pos != len(self.string):
            raise Exception("Unexpected character '{}' on line {}: '{}'".format(
                self.string[pos], line + 1, self.lines[line]))

    def parse(self, cython_info=True, fname=''):
        tokens = self.tokenize()
        rep = {'imports': [], 'messages': [], 'enums': []}
        enums = {}
        imported = {'messages': {}, 'enums': {}}
        messages = {}

        for token in tokens:
            if token.token_type == 'OPTION':
                continue

            elif token.token_type == 'SYNTAX':
                if 'proto3' == token.value:
                    assert self.syntax == 3, "Syntax and parser do not match"
                continue

            elif token.token_type == 'IMPORT':
                # Ignore google meta messages
                if token.value.find('google/protobuf') == 0:
                    continue

                rep['imports'].append(token.value)

                # Google's protoc only supports the use of messages and enums
                # from direct imports. So messages and enums from indirect
                # imports are not fetched here.
                imported_rep = self._parse_import(token.value + '.proto', fname)
                imported['messages'].update((m.name, m) for m in imported_rep['messages'])
                imported['enums'].update((e.name, e) for e in imported_rep['enums'])

            elif token.token_type == 'MESSAGE':
                rep['messages'].append(self._parse_message(token, tokens, messages, enums.copy(), imported['enums']))

            elif token.token_type == 'ENUM':
                ret = self._parse_enum(token, tokens)
                rep['enums'].append(ret)
                enums[token.name] = token

            elif token.token_type == 'EXTEND':
                self._parse_extend(token, tokens)

            else:
                raise Exception("unexpected %s token on line %d: '%s'" % (
                    token.type, token.line + 1, self.lines[token.line]))

        if cython_info:
            for message in rep['messages']:
                self.add_cython_info(message)

        return rep

    @classmethod
    def parse_from_filename(cls, fname):
        with open(fname, 'r') as fp:
            s = fp.read()

        try:
            return cls(s).parse(fname=fname)
        except Exception as e:
            print('Exception while parsing {}'.format(fname))
            raise e

    def _parse_import(self, fname, parent_fname):
        actual_fname = fname if os.path.isabs(fname) else os.path.join(os.path.dirname(parent_fname), fname)
        rep = self.__class__.parse_from_filename(actual_fname)
        return rep

    def _process_token_enum(self, token, enums):
        """
        Helper method for processing a token using known enums.
            * replaces token.default enum string value
              by its equivalent enum int value
            * sets token.enum_default attribute to enum default string value
            * sets few other token attributes
        Args:
            token: a ParserField.
            enums: {string: ParserEnum} dictionary.
        """
        if token.default is not None:
            default = None
            enum_default = None
            found = False
            for entry in enums[token.type].fields:
                if token.default == entry.name:
                    default = entry.value
                    enum_default = entry.full_name
                    found = True
                    break

            assert found, ('Enum type "{}" has no value named "{}" on line {}: '
                           '{}'.format(token.type, token.default,
                                       token.line + 1, self.lines[token.line]))
            token.default = default
            token.enum_default = enum_default

        token.enum_def = enums[token.type]
        token.enum_name = token.enum_def.full_name
        token.type = 'enum'

    def _parse_message(self, current, tokens, messages, enums, imported_enums):
        """
        Recursive parsing of messages.
        Args:
            s: the proto content string.
            current: the current ParserMessage object we are working on.
            tokens: a generator of Parser*.
            messages: a dictionary of all ParserMessage objects already known/parsed.
            enums: a dictionary of ParserEnum objects.
            imported_enums: a dictionary of ParserEnum objects.
        Returns:
            a list/hiearchy of ParserMessage objects.
        """
        token = next(tokens)
        previous = self.LBrace(-1)

        assert token.token_type == 'LBRACE', (
            "missing opening brace on line {}: '{}'".format(
                token.line + 1, self.lines[token.line]))

        for token in tokens:
            if token.token_type == 'MESSAGE':
                token.full_name = current.full_name + token.name
                current.messages[token.name] = self._parse_message(token, tokens, messages, enums.copy(), imported_enums)
                # updates the dictionary of known/parsed messages.
                messages[token.name] = current.messages[token.name]

            elif token.token_type == 'ENUM':
                token.full_name = current.full_name + token.name
                current.enums[token.name] = self._parse_enum(token, tokens)
                # updates the dictionary of known/parsed enums
                enums[token.name] = current.enums[token.name]

            elif token.token_type == 'MODIFIER':
                if self.syntax == 3:
                    assert token.value == 'repeated', (
                        "Illegal modifier {} on line {}: {}".format(
                            token.value, token.line + 1,
                            self.lines[token.line]))

            elif token.token_type == 'FIELD':
                if self.syntax == 2:
                    assert previous.token_type == 'MODIFIER', (
                        "Need modifier for field on line {}: {}".format(
                            token.line + 1, self.lines[token.line]))

                if previous.token_type == 'MODIFIER':
                    token.modifier = previous.value

                self._parse_field(token, tokens)

                if messages.get(token.type) is not None:
                    # retrieves the type "full_name"
                    token.message_name = messages.get(token.type).full_name
                    token.type = 'message'

                elif current.enums.get(token.type) is not None:
                    self._process_token_enum(token, current.enums)

                elif enums.get(token.type) is not None:
                    self._process_token_enum(token, enums)

                elif imported_enums.get(token.type) is not None:
                    self._process_token_enum(token, imported_enums)

                elif (token.type not in self.scalars) and (
                            token.type not in {'string', 'bytes'}):
                    token.message_name = token.type
                    token.type = 'message'

                current.fields.append(token)

            elif token.token_type == 'EXTENSION':
                # Just ignore extensions for now, but don't error
                previous = token
                continue

            elif token.token_type == 'OPTION':
                # Just ignore options for now, but don't error
                previous = token
                continue

            else:
                assert token.token_type == 'RBRACE', (
                    "unexpected {} token on line {}: '{}'".format(
                        token.token_type, token.line + 1,
                        self.lines[token.line]))
                return current

            previous = token

        raise Exception("unexpected EOF on line {}: '{}'".format(
            token.line + 1, self.lines[token.line]))

    def _parse_field(self, field, tokens):
        token = next(tokens)

        if token.token_type == 'LBRACKET':
            for token in tokens:
                if token.token_type == 'DEFAULT':
                    field.default = token.value
                elif token.token_type == 'PACKED':
                    field.packed = token.value
                elif token.token_type == 'DEPRECATED':
                    field.deprecated = token.value
                elif token.token_type == 'CUSTOM':
                    # Ignore custom modifiers for now
                    continue
                elif token.token_type == 'COMMA':
                    continue
                else:
                    assert token.token_type == 'RBRACKET', (
                        "unexpected {} token on line {}: '{}'".format(
                            token.token_type, token.line + 1,
                            self.lines[token.line]))
                    return

        else:
            assert token.token_type == 'SEMICOLON', (
                "expected ; or modifier on line {}, got {}: '{}'".format(
                    token.line + 1, self.lines[token.line],
                    token.token_type))

    def _parse_enum(self, current, tokens):
        token = next(tokens)
        assert token.token_type == 'LBRACE', (
            "missing opening paren on line {}: '{}'".format(
                token.line + 1, self.lines[token.line]))

        for token in tokens:
            if token.token_type == 'ENUM_FIELD':
                token.full_name = "%s_%s" % (current.full_name, token.name)
                self._parse_enum_field(token, tokens)
                current.fields.append(token)

            else:
                assert token.token_type == 'RBRACE', (
                    "unexpected %s token on line {}: '{}'".format(
                        token.token_type, token.line + 1,
                        self.lines[token.line]))
                return current

        raise Exception("unexpected EOF on line {}: '{}'".format(
            token.line + 1, self.lines[token.line]))

    def _parse_enum_field(self, field, tokens):
        token = next(tokens)

        if token.token_type == 'LBRACKET':
            for token in tokens:
                if token.token_type == 'CUSTOM':
                    # Ignore custom modifiers for now
                    continue
                elif token.token_type == 'COMMA':
                    continue
                else:
                    assert token.token_type == 'RBRACKET', (
                        "unexpected {} token on line {}: '{}'".format(
                            token.token_type, token.line + 1,
                            self.lines[token.line]))
                    return

        else:
            assert token.token_type == 'SEMICOLON', (
                "expected ; or modifier on line {}, got {}: '{}'".format(
                    token.line + 1, token.token_type,
                    self.lines[token.line]))

    def _parse_extend(self, current, tokens):
        token = next(tokens)
        assert token.token_type == 'LBRACE', (
            "missing opening paren on line {}: '{}'".format(
                token.line + 1, self.lines[token.line]))

        # For now, just find the closing brace and return
        for token in tokens:
            if token.token_type == 'RBRACE':
                return current

    def add_cython_info(self, message):
        for field in message.fields:
            field.list_type = self.list_type_map.get(field.type, 'TypedList')
            field.fixed_width = (field.type in {
                'float', 'double', 'fixed32', 'sfixed32', 'fixed64', 'sfixed64'
            })
            field.var_width = (field.type in {
                'bool', 'enum', 'int32', 'sint32', 'uint32', 'int64', 'sint64',
                'uint64'
            })

            if field.type in self.scalars:
                field.c_type = self.c_type_map[field.type]

            if field.var_width:
                field.getter = self.getter_map[field.type]
                field.setter = self.setter_map[field.type]

        for submessage in message.messages.values():
            self.add_cython_info(submessage)

    class Token(object):
        token_type = None
        line = -1
        type = None

    class Option(Token):
        def __init__(self, line, option):
            self.token_type = 'OPTION'
            self.line = line
            self.option = option

    class Syntax(Token):
        def __init__(self, line, value):
            self.token_type = 'SYNTAX'
            self.line = line
            self.value = value

    class Import(Token):
        def __init__(self, line, value):
            self.token_type = 'IMPORT'
            self.line = line
            self.value = value

    class Message(Token):
        def __init__(self, line, name):
            self.token_type = 'MESSAGE'
            self.line = line
            self.name = name
            # full_name may later be overridden with parent hierarchy
            self.full_name = name
            self.messages = {}
            self.enums = {}
            self.fields = []

    class Modifier(Token):
        def __init__(self, line, value):
            self.token_type = 'MODIFIER'
            self.line = line
            self.value = value

    class Field(Token):
        def __init__(self, line, ftype, name, index):
            self.token_type = 'FIELD'
            self.line = line
            self.modifier = None
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = False
            self.deprecated = False

    class LBracket(Token):
        def __init__(self, line):
            self.token_type = 'LBRACKET'
            self.line = line

    class RBracket(Token):
        def __init__(self, line):
            self.token_type = 'RBRACKET'
            self.line = line

    class Default(Token):
        def __init__(self, line, value):
            self.token_type = 'DEFAULT'
            self.line = line
            self.value = process_default(value)

    class Packed(Token):
        def __init__(self, line, value):
            self.token_type = 'PACKED'
            self.line = line
            self.value = value == 'true'

    class Deprecated(Token):
        def __init__(self, line, value):
            self.token_type = 'DEPRECATED'
            self.line = line
            self.value = value == 'true'

    class Custom(Token):
        def __init__(self, line, value):
            self.token_type = 'CUSTOM'
            self.line = line
            self.value = value

    class Comma(Token):
        def __init__(self, line):
            self.token_type = 'COMMA'
            self.line = line

    class Semicolon(Token):
        def __init__(self, line):
            self.token_type = 'SEMICOLON'
            self.line = line

    class Enum(Token):
        def __init__(self, line, name):
            self.token_type = 'ENUM'
            self.line = line
            self.name = name
            self.fields = []
            # full_name may later be overridden with parent hierarchy
            self.full_name = name

    class EnumField(Token):
        def __init__(self, line, name, value=None):
            self.token_type = 'ENUM_FIELD'
            self.line = line
            self.name = name
            if value is not None:
                self.value = int(value, 0)
            else:
                self.value = None
            # full_name may later be overridden with parent hierarchy
            self.full_name = name

    class LBrace(Token):
        def __init__(self, line):
            self.token_type = 'LBRACE'
            self.line = line

    class RBrace(Token):
        def __init__(self, line):
            self.token_type = 'RBRACE'
            self.line = line

    class Extension(Token):
        def __init__(self, line, low, hi):
            self.token_type = 'EXTENSION'
            self.line = line
            self.low = low
            self.hi = hi

    class Oneof(Token):
        def __init__(self, line, name):
            self.token_type = 'ONEOF'
            self.line = line
            self.name = name

    class Extend(Token):
        def __init__(self, line, name):
            self.token_type = 'EXTEND'
            self.line = line
            self.name = name


class Proto3Parser(Parser):

    syntax = 3


def process_default(default):
    if default == 'true':
        return True
    elif default == 'false':
        return False
    else:
        return default
