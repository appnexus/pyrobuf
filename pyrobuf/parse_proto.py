import os
import re


class Parser(object):

    syntax = 2

    tokens = {
        'COMMENT_OL': r'\/\/.*?\n',
        'COMMENT_ML': r'\/\*(?:.|[\r\n])*?\*\/',
        'OPTION': r'option\s+(.*?);',
        'IMPORT': r'import\s+"(.+?).proto"[ ]*;',
        'MESSAGE': r'message\s+([A-Za_z_][0-9A-Za-z_]*)',
        'FIELD': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+);',
        'FIELD_WITH_DEFAULT': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[\s*default\s*=\s*([0-9A-Za-z][0-9A-Za-z_]*|-?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')\s*\];',
        'FIELD_PACKED': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[\s*packed\s*=\s*true\s*\];',
        'FIELD_DEPRECATED': r'(optional|required|repeated)\s+([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[\s*deprecated\s*=\s*true\s*\];',
        'ENUM': r'enum\s+([A-Za-z_][0-9A-Za-z_]*)',
        'ENUM_FIELD': r'([A-Za-z_][0-9A-Za-z_]*);',
        'ENUM_FIELD_WITH_VALUE': r'([A-Za-z_][0-9A-Za-z_]*)\s*=\s*(-\d+|\d+|0x[0-9A-Fa-f]+);',
        'LBRACE': r'\{',
        'RBRACE': r'\};{0,1}',
        'SKIP': r'[ \t]',
        'NEWLINE': r'[\r\n]',
        'PACKAGE': r'package\s.*;',
        'SYNTAX': r'(syntax\s+.*?);',
        'EXTENSION': r'extensions\s+(\d+)\s+to\s+(\d+|max);',
        'ONEOF': r'oneof\s+([A-Za-z_][0-9A-Za-z_]*)',
        'ONEOF_FIELD': r'([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+);'
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
        line = 0
        lines = s.split('\n')

        m = self.get_token(s, pos)
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

            elif token_type in ('FIELD', 'FIELD_WITH_DEFAULT'):
                yield self.Field(line, *vals)

            elif token_type == 'FIELD_PACKED':
                yield self.FieldPacked(line, *vals)

            elif token_type == 'FIELD_DEPRECATED':
                yield self.FieldDeprecated(line, *vals)

            elif token_type == 'ENUM':
                yield self.Enum(line, *vals)

            elif token_type in ('ENUM_FIELD', 'ENUM_FIELD_WITH_VALUE'):
                yield self.EnumField(line, *vals)

            elif token_type == 'LBRACE':
                yield self.LBrace(line)

            elif token_type == 'RBRACE':
                yield self.RBrace(line)

            elif token_type == 'EXTENSION':
                yield self.Extension(line, *vals)

            elif token_type == 'ONEOF':
                yield self.Oneof(line, *vals)

            elif token_type == 'ONEOF_FIELD':
                yield self.OneofField(line, *vals)

            elif token_type == 'NEWLINE':
                line += 1

            pos = m.end()
            m = self.get_token(s, pos)

        if pos != len(s):
            raise Exception("Unexpected character '%s' on line %d: '%s'" % (s[pos], line, lines[line]))

    def parse(self, s, cython_info=True, fname=''):
        tokens = self.tokenize(s)
        rep = {'imports': [], 'messages': [], 'enums': []}
        enums = {}
        imported = {'messages': {}, 'enums': {}}
        messages = {}
        lines = s.split('\n')

        for token in tokens:
            if token.token_type == 'OPTION':
                continue

            elif token.token_type == 'SYNTAX':
                if 'proto3' in token.value:
                    assert(self.syntax == 3)
                continue

            elif token.token_type == 'IMPORT':
                rep['imports'].append(token.value)

                # Google's protoc only supports the use of messages and enums from direct imports.
                # So messages and enums from indirect imports are not fetched here.
                imported_rep = self._parse_import(token.value + '.proto', fname)
                imported['messages'].update((m.name, m) for m in imported_rep['messages'])
                imported['enums'].update((e.name, e) for e in imported_rep['enums'])

            elif token.token_type == 'MESSAGE':
                rep['messages'].append(self._parse_message(s, token, tokens, messages, enums.copy(), imported['enums']))

            elif token.token_type == 'ENUM':
                ret = self._parse_enum(s, token, tokens)
                rep['enums'].append(ret)
                enums[token.name] = token

            else:
                raise Exception("unexpected %s token on line %d: '%s'" % (token.type, token.line, lines[token.line]))

        if cython_info:
            for message in rep['messages']:
                self.add_cython_info(message)

        return rep

    def parse_from_filename(self, fname):
        with open(fname, 'r') as fp:
            s = fp.read()

        return self.parse(s, fname=fname)

    def _parse_import(self, fname, parent_fname):
        i_parser = self.__class__()
        actual_fname = fname if os.path.isabs(fname) else os.path.join(os.path.dirname(parent_fname), fname)
        rep = i_parser.parse_from_filename(actual_fname)
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
            found = False
            for entry in enums[token.type].fields:
                if token.default == entry.name:
                    default = entry.value
                    enum_default = entry.full_name
                    found = True
                    break

            if found:
                token.default = default
                token.enum_default = enum_default
            else:
                raise Exception('Enum type "%s" has no value named "%s".' % (token.type, token.default))

        token.enum_def = enums[token.type]
        token.enum_name = token.enum_def.full_name
        token.type = 'enum'

    def _parse_message(self, s, current, tokens, messages, enums, imported_enums):
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
        lines = s.split('\n')
        try:
            assert token.token_type == 'LBRACE'
        except AssertionError:
            raise Exception("missing opening brace on line %d: '%s'" % (token.line, lines[token.line]))

        for token in tokens:
            if token.token_type == 'MESSAGE':
                token.full_name = current.full_name + token.name
                current.messages[token.name] = self._parse_message(s, token, tokens, messages, enums.copy(), imported_enums)
                # updates the dictionary of known/parsed messages.
                messages[token.name] = current.messages[token.name]

            elif token.token_type == 'ENUM':
                token.full_name = current.full_name + token.name
                current.enums[token.name] = self._parse_enum(s, token, tokens)
                # updates the dictionary of known/parsed enums
                enums[token.name] = current.enums[token.name]

            elif token.token_type == 'FIELD':
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

                elif (token.type not in self.scalars) and (token.type not in ('string', 'bytes')):
                    token.message_name = token.type
                    token.type = 'message'

                current.fields.append(token)

            elif token.token_type == 'EXTENSION':
                # Just ignore extensions for now, but don't error
                continue

            elif token.token_type == 'RBRACE':
                return current

            else:
                raise Exception("unexpected %s token on line %d: '%s'" % (token.token_type, token.line, lines[token.line]))

        raise Exception("unexpected EOF on line %d: '%s'" % (token.line, lines[token.line]))

    def _parse_enum(self, s, current, tokens):
        token = next(tokens)
        lines = s.split('\n')
        try:
            assert token.token_type == 'LBRACE'
        except AssertionError:
            raise Exception("missing opening paren on line %d: '%s'" % (token.line, lines[token.line]))

        for token in tokens:
            if token.token_type == 'ENUM_FIELD':
                token.full_name = "%s_%s" % (current.full_name, token.name)
                current.fields.append(token)

            elif token.token_type == 'RBRACE':
                return current

            else:
                raise Exception("unexpected %s token on line %d: '%s'" % (token.token_type, token.line, lines[token.line]))

        raise Exception("unexpected EOF on line %d: '%s'" % (token.line, lines[token.line]))

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
            # full_name may later be overriden with parent hierarchy when relevant
            self.full_name = name
            self.messages = {}
            self.enums = {}
            self.fields = []

    class Field(Token):
        def __init__(self, line, modifier, ftype, name, index, default=None):
            self.token_type = 'FIELD'
            self.line = line
            self.modifier = modifier
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = process_default(default)
            self.packed = False
            self.deprecated = False

    class FieldPacked(Token):
        def __init__(self, line, modifier, ftype, name, index):
            self.token_type = 'FIELD'
            self.line = line
            self.modifier = modifier
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = True
            self.deprecated = False

    class FieldDeprecated(Token):
        def __init__(self, line, modifier, ftype, name, index):
            self.token_type = 'FIELD'
            self.line = line
            self.modifier = modifier
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = False
            self.deprecated = True

    class Enum(Token):
        def __init__(self, line, name):
            self.token_type = 'ENUM'
            self.line = line
            self.name = name
            self.fields = []
            # full_name may later be overriden with parent hierarchy when relevant
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
            # full_name may later be overriden with parent hierarchy when relevant
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

    class OneofField(Token):
        def __init__(self, line, ftype, name, index):
            self.token_type = 'ONEOF_FIELD'
            self.line = line
            self.modifier = 'optional'
            self.type = ftype
            self.name = name
            self.index = int(index)


def process_default(default):
    if default == 'true':
        return True
    elif default == 'false':
        return False
    else:
        return default
