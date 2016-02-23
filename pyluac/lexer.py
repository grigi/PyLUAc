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
    'INDENT',
    'DEDENT',
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


# Define a rule so we can track line numbers and indents and dedents
def t_newline(t):
    r'(\n[ ]*)+'
    t.lexer.lineno += len([i for i in t.value if i == '\n'])
    new_indent = len(t.value) - t.value.rfind('\n') - 1
    old_indent = t.lexer.indent[-1]

    # New Indentation
    if new_indent > old_indent:
        t.lexer.indent.append(new_indent)
        t.type = 'INDENT'
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

old_input = lexer.input

# Override input function to do some setup
def new_input(text):
    lexer.lineno = 1
    lexer.indent = [0]
    return old_input(text + '\n')

lexer.input = new_input

