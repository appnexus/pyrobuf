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
        ('FIELD', r'([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)'),
        ('MAP_FIELD', r'map<([A-Za-z][0-9A-Za-z_]+),\s*([A-Za-z][0-9A-Za-z_]+)>\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)'),
        ('DEFAULT', r'default\s*='),
        ('PACKED', r'packed\s*=\s*(true|false)'),
        ('DEPRECATED', r'deprecated\s*=\s*(true|false)'),
        ('CUSTOM', r'(\([A-Za-z][0-9A-Za-z_]*\).[A-Za-z][0-9A-Za-z_]*)\s*='),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]\s*;'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}\s*;{0,1}'),
        ('COMMA', r','),
        ('SKIP', r'\s'),
        ('SEMICOLON', r';'),
        ('NUMERIC', r'(-?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)'),
        ('STRING', r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^"\\])*\')'),
        ('BOOLEAN', r'(true|false)'),
        ('ENUM_FIELD_WITH_VALUE', r'([A-Za-z_][0-9A-Za-z_]*)\s*=\s*(0x[0-9A-Fa-f]+|-\d+|\d+)'),
        ('ENUM_FIELD', r'([A-Za-z_][0-9A-Za-z_]*)')
    ]

    parsable_tokens = (
        'OPTION',
        'SYNTAX',
        'IMPORT',
        'MESSAGE',
        'MODIFIER',
        'FIELD',
        'MAP_FIELD',
        'LBRACKET',
        'RBRACKET',
        'DEFAULT',
        'PACKED',
        'DEPRECATED',
        'COMMA',
        'SEMICOLON',
        'ENUM',
        'LBRACE',
        'RBRACE',
        'EXTENSION',
        'ONEOF',
        'EXTEND',
    )

    # These tokens are parsed by the parser but are not supported by the
    # code that build the C extension files and definitions
    unsupported_tokens = ('MAP_FIELD', 'ONEOF',)

    scalars = {
        'double', 'float', 'int32', 'int64', 'uint32', 'uint64', 'sint32', 'sint64',
        'fixed32', 'fixed64', 'sfixed32', 'sfixed64', 'bool', 'enum', 'timestamp'
    }

    floats = {'double', 'float'}

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
        'timestamp': 'uint32_t'
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

    def tokenize(self, disabled_token_types):
        token_type_to_token_class = self.get_token_type_to_token_class_map()

        pos = 0
        line = 0

        m = self.get_token(self.string, pos)
        while m is not None:
            token_type = m.lastgroup
            subm = self.token_getter[token_type](m.group(token_type))
            vals = subm.groups()

            assert token_type not in disabled_token_types, "Disabled token '{}' found on line {}: {}".format(
                token_type, line + 1, self.lines[line])

            # ENUM_FIELD_WITH_VALUE has different regex
            # but same class as ENUM_FIELD
            if token_type == 'ENUM_FIELD_WITH_VALUE':
                token_type = 'ENUM_FIELD'

            if token_type in token_type_to_token_class:
                token_class = token_type_to_token_class[token_type]
                yield token_class(line, *vals)

            line += subm.group().count('\n')
            pos = m.end()
            m = self.get_token(self.string, pos)

        if pos != len(self.string):
            raise Exception("Unexpected character '{}' on line {}: '{}'".format(
                self.string[pos], line + 1, self.lines[line]))

    def parse(self, cython_info=True, fname='', includes=None, disabled_tokens=()):
        self.verify_parsable_tokens()
        tokens = self.tokenize(disabled_tokens)
        rep = {'imports': [], 'messages': [], 'enums': []}
        enums = {}
        imported = {'messages': {}, 'enums': {}}
        messages = {}
        includes = includes or []
        scope = {}

        for token in tokens:
            if token.token_type == 'OPTION':
                continue

            elif token.token_type == 'SYNTAX':
                if 'proto2' == token.value:
                    self.syntax = 2
                elif 'proto3' == token.value:
                    self.syntax = 3
                else:
                    raise Exception("Unexpected syntax value '{}'".format(token.value))

            elif token.token_type == 'IMPORT':
                # Ignore google meta messages
                if token.value.find('google/protobuf') == 0:
                    continue

                rep['imports'].append(token.value)

                # Google's protoc only supports the use of messages and enums
                # from direct imports. So messages and enums from indirect
                # imports are not fetched here.
                imported_rep = self._parse_import(
                    token.value + '.proto',
                    fname,
                    includes,
                    disabled_tokens
                )
                imported['messages'].update(
                    (m.name, m) for m in imported_rep['messages']
                )
                imported['enums'].update(
                    (e.name, e) for e in imported_rep['enums']
                )

            elif token.token_type == 'MESSAGE':
                ret = self._parse_message(
                        token, tokens, messages, enums.copy(),
                        imported['enums']
                )

                assert token.name not in scope, (
                    "'{}' is already defined in global scope".format(
                        token.name))

                scope[token.name] = ret
                rep['messages'].append(ret)

            elif token.token_type == 'ENUM':
                rep['enums'].append(
                    self._parse_enum(token, tokens, scope)
                )
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
    def parse_from_filename(cls, fname, includes, disabled_tokens=unsupported_tokens):
        with open(fname, 'r') as fp:
            s = fp.read()

        try:
            return cls(s).parse(fname=fname, includes=includes, disabled_tokens=disabled_tokens)
        except Exception as e:
            print('Exception while parsing {}'.format(fname))
            raise e

    def _parse_import(self, fname, parent_fname, includes, disabled_tokens):
        actual_fname = fname
        if not os.path.isabs(fname):
            for d in [os.path.dirname(parent_fname)] + includes:
                actual_fname = os.path.join(d, fname)
                if os.path.exists(actual_fname):
                    break

        return self.__class__.parse_from_filename(actual_fname, includes, disabled_tokens)

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
            for value, entry in enums[token.type].fields.items():
                if token.default == entry.name:
                    default = value
                    enum_default = entry.full_name
                    found = True
                    break

            assert found, "Enum type '{}' has no value named '{}' on line {}: {}".format(
                token.type, token.default, token.line + 1, self.lines[token.line])
            token.default = default
            token.enum_default = enum_default

        token.enum_def = enums[token.type]
        token.enum_name = token.enum_def.full_name
        token.type = 'enum'

    def _parse_message(self, current_message, tokens, messages, enums, imported_enums):
        """
        Recursive parsing of messages.
        Args:
            current_message: the current ParserMessage object we are working on.
            tokens: a generator of Parser*.
            messages: a dictionary of all ParserMessage objects
                already known/parsed.
            enums: a dictionary of ParserEnum objects.
            imported_enums: a dictionary of ParserEnum objects.
        Returns:
            a list/hiearchy of ParserMessage objects.
        """
        token = next(tokens)
        previous = self.LBrace(-1)

        assert token.token_type == 'LBRACE', "missing opening brace on line {}: '{}'".format(
            token.line + 1, self.lines[token.line])

        for token in tokens:
            if token.token_type == 'MESSAGE':
                token.full_name = current_message.full_name + token.name
                ret = self._parse_message(token, tokens, messages, enums.copy(), imported_enums)

                assert token.name not in current_message.namespace, "'{}' is already defined in message '{}'".format(
                    token.name, current_message.name)

                current_message.messages[token.name] = ret
                current_message.namespace[token.name] = ret
                # updates the dictionary of known/parsed messages.
                messages[token.name] = current_message.messages[token.name]

            elif token.token_type == 'ENUM':
                token.full_name = current_message.full_name + token.name
                current_message.enums[token.name] = self._parse_enum(
                    token,
                    tokens,
                    current_message.namespace,
                    current_message
                )
                # updates the dictionary of known/parsed enums
                enums[token.name] = current_message.enums[token.name]

            elif token.token_type == 'ONEOF':
                current_message.oneofs[token.name] = token
                self._parse_oneof(token, tokens, current_message, messages, enums, imported_enums)

            elif token.token_type == 'MODIFIER':
                if self.syntax == 3:
                    assert token.value == 'repeated', (
                        "Illegal modifier {} on line {}: {}".format(
                            token.value, token.line + 1,
                            self.lines[token.line]))

            elif token.token_type in ('FIELD', 'MAP_FIELD'):
                self._parse_field_token(token, previous, tokens, current_message, messages, enums, imported_enums)

            elif token.token_type == 'EXTENSION':
                # Just ignore extensions for now, but don't error
                previous = token
                continue

            elif token.token_type == 'OPTION':
                # Just ignore options for now, but don't error
                previous = token
                continue

            else:
                assert token.token_type == 'RBRACE', "unexpected {} token on line {}: '{}'".format(
                    token.token_type, token.line + 1, self.lines[token.line])
                return current_message

            previous = token

        raise Exception("unexpected EOF on line {}: '{}'".format(token.line + 1, self.lines[token.line]))

    def _parse_field_token(self, token, previous, tokens, current_message, messages, enums, imported_enums):
        """Parse FIELD and MAP_FIELD token types"""
        if self.syntax == 2:
            assert previous.token_type == 'MODIFIER', "Need modifier for field on line {}: {}".format(
                token.line + 1, self.lines[token.line])
        if previous.token_type == 'MODIFIER':
            # Map fields does not accept any modifiers
            assert token.token_type == 'FIELD', "Illegal modifier '{}' for map field on line {}: {}".format(
                previous.value, token.line + 1, self.lines[token.line])

            token.modifier = previous.value
        self._parse_field(token, tokens)

        assert token.index > 0, (
            "non-positive field index on line {}: '{}'".format(token.line + 1, self.lines[token.line]))
        assert token.index not in current_message.fields, (
            "Field index {} in '{}' is already used by '{}'".format(
                token.index, current_message.name, current_message.fields[token.index].name))
        assert token.name not in current_message.namespace, (
            "'{}' is already defined in message '{}'".format(token.name, current_message.name))

        if messages.get(token.type) is not None:
            # retrieves the type "full_name"
            token.message_name = messages.get(token.type).full_name
            token.type = 'message'

        elif current_message.enums.get(token.type) is not None:
            self._process_token_enum(token, current_message.enums)

        elif enums.get(token.type) is not None:
            self._process_token_enum(token, enums)

        elif imported_enums.get(token.type) is not None:
            self._process_token_enum(token, imported_enums)

        elif (token.type not in self.scalars) and (token.type not in {'string', 'bytes'}):
            token.message_name = token.type
            token.type = 'message'

        current_message.fields[token.index] = token
        current_message.namespace[token.name] = token

    def _parse_oneof(self, oneof_token, tokens, current_message, messages, enums, imported_enums):
        token = next(tokens)
        assert token.token_type == 'LBRACE', (
            "missing opening paren on line {}: '{}'".format(
                token.line + 1, self.lines[token.line]))

        # setting previous as a place holder for the inner fields parsing
        previous = self.LBrace(-1)
        for token in tokens:
            if token.token_type == 'FIELD':
                # fields will be added to the proper message by the following
                # parser function that takes care of fields generally
                self._parse_field_token(token, previous, tokens, current_message, messages, enums, imported_enums)
                oneof_token.fields.append(token.name)
                previous = token

            else:
                assert token.token_type == 'RBRACE', "unexpected {} token on line {}: '{}'".format(
                    token.token_type, token.line + 1, self.lines[token.line])
                return oneof_token

        raise Exception("unexpected EOF on line {}: '{}'".format(
            token.line + 1, self.lines[token.line]))

    def _parse_field(self, field, tokens):
        """Parse the body of a FIELD token"""
        token = next(tokens)

        if token.token_type == 'LBRACKET':
            for token in tokens:
                if token.token_type == 'DEFAULT':
                    self._parse_default(field, tokens)
                elif token.token_type == 'PACKED':
                    field.packed = token.value
                elif token.token_type == 'DEPRECATED':
                    field.deprecated = token.value
                elif token.token_type == 'CUSTOM':
                    if self._parse_custom(field, tokens):
                        return
                elif token.token_type == 'COMMA':
                    continue
                else:
                    assert token.token_type == 'RBRACKET', "unexpected {} token on line {}: '{}'".format(
                        token.token_type, token.line + 1, self.lines[token.line])
                    return

        else:
            assert token.token_type == 'SEMICOLON', "expected ; or modifier on line {}, got {}: '{}'".format(
                token.line + 1, self.lines[token.line], token.token_type)

    def _parse_default(self, field, tokens):
        """Parse a default option"""
        token = next(tokens)

        if token.token_type == 'ENUM_FIELD':
            # This will get updated later
            field.default = token.full_name
            return
        elif token.token_type == 'NUMERIC':
            assert field.type in self.scalars, \
                "attempting to set numeric as default for non-numeric field on line {}: '{}'".format(
                    token.line + 1, self.lines[token.line])
            if field.type not in self.floats:
                assert int(token.value) == token.value, \
                    "attempting to set integer non-integer default for integer field on line {}: '{}'".format(
                        token.line + 1, self.lines[token.line])
                token.value = int(token.value)
        elif token.token_type == 'STRING':
            assert field.type in {'string', 'bytes'}, "attempting to set string as default on line {}: '{}'".format(
                token.line + 1, self.lines[token.line])
        else:
            assert token.token_type == 'BOOLEAN', "unexpected {} token on line {}: '{}'".format(
                token.token_type, token.line + 1, self.lines[token.line])

        field.default = token.value

    def _parse_custom(self, field, tokens):
        """Parse a custom option and return whether or not we hit the closing RBRACKET"""
        token = next(tokens)

        if token.token_type == 'STRING':
            field.value = token.value
            for token in tokens:
                if token.token_type == 'STRING':
                    field.value += token.value
                    continue
                elif token.token_type == 'COMMA':
                    return False
                else:
                    assert token.token_type == 'RBRACKET'
                    return True
        else:
            assert token.token_type in {'NUMERIC', 'BOOLEAN'}, "unexpected custom option value on line {}: '{}'".format(
                token.line + 1, self.lines[token.line])
            field.value = token.value
            return False

    def _parse_enum(self, current, tokens, scope, current_message=None):
        token = next(tokens)
        assert token.token_type == 'LBRACE', "missing opening brace on line {}: '{}'".format(
            token.line + 1, self.lines[token.line])

        for num, token in enumerate(tokens):
            if token.token_type == 'ENUM_FIELD':
                if num == 0:
                    if self.syntax == 3:
                        assert token.value == 0, "expected zero as first enum element on line {}, got {}: '{}'".format(
                            token.line + 1, token.value, self.lines[token.line])
                    current.default = token

                token.full_name = "{}_{}".format(current.full_name, token.name)

                assert token.name not in scope, "'{}' is already defined in {}".format(
                    token.name, "'{}'".format(current_message.name) if current_message else "global scope")

                # protoc allows value collisions with allow_alias option;
                # revisit once options are implemented
                assert token.value not in current.fields, "Enum value {} in '{}' is already used".format(
                    token.value, current.name)

                current.fields[token.value] = token
                scope[token.name] = token

                self._parse_enum_field(token, tokens)
            else:
                assert token.token_type == 'RBRACE', "unexpected {} token on line {}: '{}'".format(
                    token.token_type, token.line + 1, self.lines[token.line])
                return current

        raise Exception("unexpected EOF on line {}: '{}'".format(
            token.line + 1, self.lines[token.line]))

    def _parse_enum_field(self, field, tokens):
        token = next(tokens)

        if token.token_type == 'LBRACKET':
            for token in tokens:
                if token.token_type == 'CUSTOM':
                    if self._parse_custom(field, tokens):
                        return
                elif token.token_type == 'COMMA':
                    continue
                else:
                    assert token.token_type == 'RBRACKET', "unexpected {} token on line {}: '{}'".format(
                        token.token_type, token.line + 1, self.lines[token.line])
                    return

        else:
            assert token.token_type == 'SEMICOLON', "expected ; or modifier on line {}, got {}: '{}'".format(
                token.line + 1, token.token_type, self.lines[token.line])

    def _parse_extend(self, current, tokens):
        token = next(tokens)
        assert token.token_type == 'LBRACE', "missing opening paren on line {}: '{}'".format(
            token.line + 1, self.lines[token.line])

        # For now, just find the closing brace and return
        for token in tokens:
            if token.token_type == 'RBRACE':
                return current

    def add_cython_info(self, message):
        for field in message.fields.values():
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

    @classmethod
    def get_token_type_to_token_class_map(cls):
        return {
            token_class.token_type: token_class
            for token_class in cls.Token.__subclasses__()
        }

    @classmethod
    def verify_parsable_tokens(cls):
        """Raise error if any of the parsable tokens has no class defined."""
        mapping = cls.get_token_type_to_token_class_map()
        for token_type in cls.parsable_tokens:
            if token_type not in mapping:
                raise NotImplementedError("Parsable token {} has no repr class defined.".format(token_type))

    class Token(object):
        token_type = None
        line = -1
        type = None

    class Option(Token):
        token_type = 'OPTION'

        def __init__(self, line, option):
            self.line = line
            self.option = option

    class Syntax(Token):
        token_type = 'SYNTAX'

        def __init__(self, line, value):
            self.line = line
            self.value = value

    class Import(Token):
        token_type = 'IMPORT'

        def __init__(self, line, value):
            self.line = line
            self.value = value

    class Message(Token):
        token_type = 'MESSAGE'

        def __init__(self, line, name):
            self.line = line
            self.name = name
            # full_name may later be overridden with parent hierarchy
            self.full_name = name
            self.messages = {}
            self.enums = {}
            self.oneofs = {}
            self.fields = {}
            self.namespace = {}

    class Modifier(Token):
        token_type = 'MODIFIER'

        def __init__(self, line, value):
            self.line = line
            self.value = value

    class Field(Token):
        token_type = 'FIELD'

        def __init__(self, line, ftype, name, index):
            self.line = line
            self.modifier = None
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = False
            self.deprecated = False

        def get_key(self):
            if self.modifier == 'repeated' and self.packed:
                return (self.index << 3) | 2
            elif self.type in {'message', 'string', 'bytes'}:
                return (self.index << 3) | 2
            elif self.type in {'fixed64', 'sfixed64', 'double'}:
                return (self.index << 3) | 1
            elif self.type in {'fixed32', 'sfixed32', 'float'}:
                return (self.index << 3) | 5
            else:
                return (self.index << 3) | 0

    class MapField(Token):
        token_type = 'MAP_FIELD'

        def __init__(self, line, key_type, value_type, name, index):
            self.line = line
            # value type is set to self.type if it is processed similarly
            # to the Field token.
            self.type = value_type
            self.key_type = key_type
            self.name = name
            self.index = int(index)

            # currently copied from the Field token so they are processed the
            # same way. Maybe it is not needed if these are not supported for
            # map fields
            self.default = None
            self.packed = False
            self.deprecated = False

            # Map fields does not support modifiers both for syntax 2 and 3
            # self.modifier = None

        def get_key(self):
            raise NotImplementedError(
                "MapField implemented currently only for parsing purposes."
            )

    class LBracket(Token):
        token_type = 'LBRACKET'

        def __init__(self, line):
            self.line = line

    class RBracket(Token):
        token_type = 'RBRACKET'

        def __init__(self, line):
            self.line = line

    class Default(Token):
        token_type = 'DEFAULT'

        def __init__(self, line):
            self.line = line

    class Packed(Token):
        token_type = 'PACKED'

        def __init__(self, line, value):
            self.line = line
            self.value = value == 'true'

    class Deprecated(Token):
        token_type = 'DEPRECATED'

        def __init__(self, line, value):
            self.line = line
            self.value = value == 'true'

    class Custom(Token):
        token_type = 'CUSTOM'

        def __init__(self, line, name):
            self.line = line
            self.name = name
            self.value = None

    class Comma(Token):
        token_type = 'COMMA'

        def __init__(self, line):
            self.line = line

    class Semicolon(Token):
        token_type = 'SEMICOLON'

        def __init__(self, line):
            self.line = line

    class Enum(Token):
        token_type = 'ENUM'

        def __init__(self, line, name):
            self.line = line
            self.name = name
            self.fields = {}
            self.default = None
            # full_name may later be overridden with parent hierarchy
            self.full_name = name

    class EnumField(Token):
        token_type = 'ENUM_FIELD'

        def __init__(self, line, name, value=None):
            self.line = line
            self.name = name
            if value is not None:
                self.value = int(value, 0)
            else:
                self.value = None
            # full_name may later be overridden with parent hierarchy
            self.full_name = name

    class Numeric(Token):
        token_type = 'NUMERIC'

        def __init__(self, line, value):
            self.line = line
            self.value = float(value)

    class String(Token):
        token_type = 'STRING'

        def __init__(self, line, value):
            self.line = line
            self.value = value

    class Boolean(Token):
        token_type = 'BOOLEAN'

        def __init__(self, line, value):
            self.line = line
            self.value = True if value == 'true' else False

    class LBrace(Token):
        token_type = 'LBRACE'

        def __init__(self, line):
            self.line = line

    class RBrace(Token):
        token_type = 'RBRACE'

        def __init__(self, line):
            self.line = line

    class Extension(Token):
        token_type = 'EXTENSION'

        def __init__(self, line, low, hi):
            self.line = line
            self.low = low
            self.hi = hi

    class Oneof(Token):
        token_type = 'ONEOF'

        def __init__(self, line, name):
            self.line = line
            self.name = name
            self.fields = []

    class Extend(Token):
        token_type = 'EXTEND'

        def __init__(self, line, name):
            self.line = line
            self.name = name


class Proto3Parser(Parser):
    syntax = 3
