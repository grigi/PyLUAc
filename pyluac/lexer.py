'''
PyLUAc tokeniser/lexer
'''
import ply.lex as lex


# List of token names.   This is always required
tokens = (
    'IDENTIFIER',
    'STRING',
    'NUMBER',
    'LPAREN',
    'RPAREN',
#    'LSBRACK',
#    'RSBRACK',
#    'LCBRACE',
#    'RCBRACE',
)


# Simple tokens
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_IDENTIFIER = r'[_a-zA-Z][_a-zA-Z0-9]*'


# Mutating tokens
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)  # TODO: Should be Decimal
    return t

def t_STRING(t):
    r'("[^\n"]*")'
    t.value = t.value[1:-1]
    return t



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

