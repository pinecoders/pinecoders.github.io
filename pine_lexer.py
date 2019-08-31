from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Literal, Punctuation, Generic, Other, Error

# Many examples are here https://bitbucket.org/birkenfeld/pygments-main/src/default/pygments/lexers/
class PinePygmentsLexer(RegexLexer):
    name = 'pine'

    tokens = {
        'root': [
            (r'\#([0-9a-fA-F]{8})|\#([0-9a-fA-F]{6})', Literal), # Color literal
            (r'[0-9]+', Number.Integer),
            (r'(\.\d+|[0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?', Number.Float),
            (r'\s+', Text.Whitespace),
            (r'//.*?$', Comment), 
            (r'(for|if|else|var)\b', Keyword),
            (r'(open|high|low|close|volume|time|hl2|hlc3|ohlc4)\b', Name.Constant), # Built-in series 'open', 'high', ...
            (r'(study|strategy|plot|plotshape|plotchar|plotarrow|fill|hline|input)\b', Name.Entity), # Annotation function
            (r'[\w\.]+', Name.Other),
            (r'\+|\-|\*|\/|\%|\=|\[|\]|and|or|not|\?|\:|\<|\>|\!', Operator),
            (r'\(|\)|\,', Punctuation),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
        ]
    }