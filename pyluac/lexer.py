'''
PyLUAc tokeniser/lexer
'''
import ply.lex as lex

reserved = {
    'if'   : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while': 'WHILE',
    'for'  : 'FOR',
}

# List of token names.   This is always required
tokens = [
    'ID',
    'STRING',
    'NUMBER',
#    'LPAREN',
#    'RPAREN',
#    'LSBRACK',
#    'RSBRACK',
#    'LCBRACE',
#    'RCBRACE',
] + list(reserved.values())

literals = [ '+','-','*','/','(',')' ]

# Simple tokens
#t_LPAREN     = r'\('
#t_RPAREN     = r'\)'

# Mutating tokens
def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)  # TODO: Should be Decimal
    return t

def t_STRING(t):
    r'("[^\n"]*")'
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

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

