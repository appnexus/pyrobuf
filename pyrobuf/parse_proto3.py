from pyrobuf.parse_proto import *


class Proto3Parser(Parser):

    syntax = 3

    tokens = Parser.tokens.copy()
    tokens['FIELD'] = (r'(repeated|)\s+([A-Za-z][0-9A-Za-z_]*)\s+'
                       r'([A-Za-z][0-9A-Za-z_]*)\s*=\s*(\d+);')

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

    class FieldDeprecated(Parser.Token):
        def __init__(self, line, modifier, ftype, name, index):
            self.token_type = 'FIELD'
            self.line = line
            self.modifier = 'repeated' if modifier == 'repeated ' else 'optional'
            self.type = ftype
            self.name = name
            self.index = int(index)
            self.default = None
            self.packed = ftype in Parser.scalars
            self.deprecated = True
