'''
PyLUAc tokeniser/lexer
'''
# pylint: disable=C0103
import re
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
    'Skip any unparsed text inside multiline string'
    t.lexer.skip(1)


def t_multilined_multilines_eof(t):
    'Only happens when a multiline is not closed'
    t.lexpos = t.lexer.begin_lexpos - 2
    raise lex.LexError("Multiline string not closed at line %d col %d" % (t.lexer.begin_lineno, find_column(t.lexer.lexdata, t)), t.lexer.lexdata[t.lexer.begin_lexpos:])


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
    'IDASSIGN',
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

literals = ['+', '-', '*', '/', '%', '(', ')', ':', ',']


# Simple tokens
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
    r'[_a-zA-Z][_a-zA-Z0-9]*([ ]*=[^=])?'
    if '=' in t.value:
        t.type = 'IDASSIGN'
        m = re.match(r'[_a-zA-Z][_a-zA-Z0-9]*', t.value)
        t.value = m.group(0)
        t.lexer.lexpos -= 1
    else:
        t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)  # TODO: Should be Decimal
    else:
        t.value = int(t.value)
    return t

def t_STRING(t):
    r'("[^\n"]*"|\'[^\n\']*\')'
    t.value = t.value[1:-1]
    return t

def t_TRUE(t):
    r'True'
    t.value = True
    return t

def t_FALSE(t):
    r'False'
    t.value = False
    return t

def t_NONE(t):
    r'None'
    t.value = None
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
            t.lexpos = t.lexer.lexpos
            raise lex.LexError("Invalid indentation at line %d col %d" % (t.lexer.lineno, find_column(t.lexer.lexdata, t)), t.lexer.lexdata[t.lexer.lexpos:])

        t.lexer.indent = t.lexer.indent[:-1]
        t.type = 'DEDENT'
        t.value = ''
        t.lineno = t.lexer.lineno
        return t


def find_column(lexdata, token):
    '''
    Compute column.
        lexdata is the input text string
        token is a token instance
    '''
    last_cr = lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:  # pragma: no cover
        last_cr = 0  # This should never happen -> first character is always a newline
    column = token.lexpos - last_cr - 1
    return column


# Error handling rule
def t_error(t):  # pragma: no cover
    'Unexpected error - should fail hard'
    print("Illegal character %s" % repr(t.value[0]))
    raise lex.LexError("Scanning error. Illegal character %s at line %d col %d" % (repr(t.lexer.lexdata[t.lexer.lexpos]), t.lexer.lineno, find_column(t.lexer.lexdata, t)), t.lexer.lexdata[t.lexer.lexpos:])


# Build the lexer
lexer = lex.lex()
lexer.lineno = 1
lexer.indent = [0]


old_input = lexer.input
def new_input(text):
    '''
    Override input function to do some setup.
    I probably shouldn't do this monkeypatching
    '''
    # Reset state before each run
    lexer.begin('INITIAL')
    lexer.lineno = 0
    lexer.indent = [0]
    return old_input('\n' + text + '\n')
lexer.input = new_input

