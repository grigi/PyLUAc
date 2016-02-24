'''
PyLUAc tokeniser/lexer
'''
from ply import lex

states = (
    ('multilined', 'exclusive'),
    ('multilines', 'exclusive'),
)

# multiline(s|d) state
def t_multistringd(t):
    r'"""'
    t.lexer.begin('multilined')
    t.lexer.begin_lexpos = t.lexer.lexpos
    t.lexer.begin_lineno = t.lexer.lineno

def t_multistrings(t):
    r"'''"
    t.lexer.begin('multilines')
    t.lexer.begin_lexpos = t.lexer.lexpos
    t.lexer.begin_lineno = t.lexer.lineno

def t_multilined_multilines_newline(t):
    r'\n'
    t.lexer.lineno += 1
    
def t_multilined_multilines_error(t):
    t.lexer.skip(1)

def t_multilined_STRING(t):
    r'"""'
    t.lexer.begin('INITIAL')
    t.type = 'STRING'
    t.value = t.lexer.lexdata[t.lexer.begin_lexpos: t.lexer.lexpos-3]
    t.lineno = t.lexer.begin_lineno
    return t

def t_multilines_STRING(t):
    r"'''"
    t.lexer.begin('INITIAL')
    t.type = 'STRING'
    t.value = t.lexer.lexdata[t.lexer.begin_lexpos: t.lexer.lexpos-3]
    t.lineno = t.lexer.begin_lineno
    return t

# Normal state - INITIAL
reserved = {
    'if'    : 'IF',
    'then'  : 'THEN',
    'else'  : 'ELSE',
    'while' : 'WHILE',
    'for'   : 'FOR',
    'def'   : 'DEF',
    'class' : 'CLASS',
    'return': 'RETURN',
}

# List of token names.   This is always required
tokens = [
    'ID',
    'STRING',
    'NUMBER',
    'INDENT',
    'DEDENT',
    'EQUALS',
    'NEQUALS',
    'GECOMP',
    'LECOMP',
    'GCOMP',
    'LCOMP',
    'TRUE',
    'FALSE',
    'NONE',
] + list(reserved.values())

literals = ['+', '-', '*', '/', '%', '(', ')', '=', ':']

# Simple tokens
t_TRUE = r'True'
t_FALSE = r'False'
t_NONE = r'None'
t_EQUALS = r'=='
t_NEQUALS = r'!='
t_GECOMP = r'<='
t_LECOMP = r'>='
t_GCOMP = r'<'
t_LCOMP = r'>'

t_ignore_COMMENT = r'\#.*'
t_ignore_WHITESPACE = r'[ ]'

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
    r'("[^\n"]*"|\'[^\n\']*\')'
    t.value = t.value[1:-1]
    return t

# Define a rule so we can track line numbers and indents and dedents
# TODO: Make handle tabs
def t_newline(t):
    r'(\n[ ]*)+'
    t.lexer.lineno += len([i for i in t.value if i == '\n'])
    new_indent = len(t.value) - t.value.rfind('\n') - 1
    old_indent = t.lexer.indent[-1]

    # New Indentation
    if new_indent > old_indent:
        t.lexer.indent.append(new_indent)
        t.type = 'INDENT'
        t.value = ''
        t.lineno = t.lexer.lineno
        return t

    # Dedentation required
    if new_indent < old_indent:
        # Reset token if more dedents are required
        try:
            if (len(t.lexer.indent) - t.lexer.indent.index(new_indent) - 1) > 1:
                t.lexer.lexpos -= len(t.value)
        except ValueError:
                raise lex.LexError("Invalid indentation at line %d col %d" % (t.lexer.lineno, find_column(t.lexer.lexdata, t)), t.lexer.lexdata[t.lexer.lexpos:])

        t.lexer.indent = t.lexer.indent[:-1]
        t.type = 'DEDENT'
        t.value = ''
        t.lineno = t.lexer.lineno
        return t


# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


# Error handling rule
def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    raise lex.LexError("Scanning error. Illegal character %s at line %d col %d" % (repr(t.lexer.lexdata[t.lexer.lexpos]), t.lexer.lineno, find_column(t.lexer.lexdata, t)), t.lexer.lexdata[t.lexer.lexpos:])
    return t
#    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
lexer.lineno = 1
lexer.indent = [0]

# Override input function to do some setup
# I probably shouldn't do this monkeypatching
old_input = lexer.input
def new_input(text):
    lexer.lineno = 1
    lexer.indent = [0]
    return old_input(text + '\n')
lexer.input = new_input

