from pyrobuf.parse_proto import *


class Proto3Parser(Parser):

    syntax = 3

    tokens = {
        'COMMENT_OL': Parser.tokens['COMMENT_OL'],
        'COMMENT_ML': Parser.tokens['COMMENT_ML'],
        'OPTION': Parser.tokens['OPTION'],
        'IMPORT': Parser.tokens['IMPORT'],
        'MESSAGE': Parser.tokens['MESSAGE'],
        'FIELD': r'(repeated |)\s*([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+);',
        'FIELD_DEPRECATED': r'(repeated |)\s*([A-Za-z][0-9A-Za-z_]*)\s+([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+)\s+\[deprecated\s*=\s*true\];',
        'ENUM': Parser.tokens['ENUM'],
        'ENUM_FIELD': Parser.tokens['ENUM_FIELD'],
        'ENUM_FIELD_WITH_VALUE': Parser.tokens['ENUM_FIELD_WITH_VALUE'],
        'LBRACE': Parser.tokens['LBRACE'],
        'RBRACE': Parser.tokens['RBRACE'],
        'SKIP': Parser.tokens['SKIP'],
        'NEWLINE': Parser.tokens['NEWLINE'],
        'PACKAGE': Parser.tokens['PACKAGE'],
        'SYNTAX': Parser.tokens['SYNTAX']
    }

    class ParserField(object):
        def __init__(self, pos, modifier, ftype, name, index):
            self.token_type = 'FIELD'
            self.pos = pos
            self.modifier = 'repeated' if modifier == 'repeated ' else 'optional'
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = ftype in Parser.scalars
            self.deprecated = False

    class ParserFieldDeprecated(object):
        def __init__(self, pos, modifier, ftype, name, index):
            self.token_type = 'FIELD'
            self.pos = pos
            self.modifier = 'repeated' if modifier == 'repeated ' else 'optional'
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = ftype in Parser.scalars
            self.deprecated = True
