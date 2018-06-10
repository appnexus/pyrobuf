from pyrobuf.parse_proto import *


class Proto3Parser(Parser):

    syntax = 3

    # Tokens ordered roughly by priority
    tokens = [
        ('COMMENT_OL', r'\/\/.*?\n'),
        ('COMMENT_ML', r'\/\*(?:.|[\r\n])*?\*\/'),
        ('OPTION', r'option\s+((?:.|[\n\r])*?);'),
        ('IMPORT', r'import\s+"(.+?).proto"\s*;'),
        ('MESSAGE', r'message\s+([A-Za-z_][0-9A-Za-z_]*)'),
        ('ENUM', r'enum\s+([A-Za-z_][0-9A-Za-z_]*)'),
        ('PACKAGE', r'package\s+.*\s*;'),
        ('SYNTAX', r'(syntax\s+.*?)\s*;'),
        ('EXTEND', r'extend\s+([A-Za-z_][0-9A-Za-z_\.]*)'),
        ('EXTENSION', r'extensions\s+(\d+)\s+to\s+(\d+|max)\s*;'),
        ('ONEOF', r'oneof\s+([A-Za-z_][0-9A-Za-z_]*)'),
        ('FIELD', r'(repeated|)\s+([A-Za-z][0-9A-Za-z_]*)'
                  r'\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)'),
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
        ('ENUM_FIELD', r'([A-Za-z_][0-9A-Za-z_]*)\s*'),
        ('ONEOF_FIELD', r'([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*='
                        r'\s*(\d+)\s*;')
    ]

    class Field(Parser.Token):
        def __init__(self, line, modifier, ftype, name, index):
            self.token_type = 'FIELD'
            self.line = line
            self.modifier = 'repeated' if modifier == 'repeated ' else 'optional'
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = ftype in Parser.scalars
            self.deprecated = False
