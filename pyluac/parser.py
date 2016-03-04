'''
PyLUAc parser
'''

import ply.yacc as yacc


# Get the token map from the lexer.  This is required.
from pyluac.lexer import tokens

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('left', '('),
    ('left', 'BRACKET'),
    ('right', 'UMINUS'),
)

def p_block(p):
    '''
    block : statement block
          | statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]]
        p[0].extend(p[2])


def p_statement(p):
    '''
    statement : assignment
              | expression
              | return
    '''
    p[0] = p[1]

def p_return(p):
    '''
    return : RETURN expression
    '''
    p[0] = ('return', p[2])

def p_assignment(p):
    '''
    assignment : IDASSIGN expression
    '''
    p[0] = ('assign', p[1], p[2])

def p_function(p):
    '''
    function : ID '(' expressionlist assignmentlist ')'
    '''
    p[0] = ('func', p[1], p[3], p[4])

def p_tuple(p):
    '''
    tuple : '(' expressionlist ')'
    '''
    p[0] = ('tuple', p[2])

def p_expressionlist(p):
    '''
    expressionlist : expressionlist ',' expression
                   | expressionlist ','
                   | expression
                   |
    '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_assignmentlist(p):
    '''
    assignmentlist : assignmentlist ',' assignment
                   | assignmentlist ','
                   | assignment
                   |
    '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_expression(p):
    '''
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | expression '%' expression
               | '-' expression %prec UMINUS
               | '(' expression ')' %prec BRACKET
               | object
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('neg', p[2])
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = (p[2], p[1], p[3])


def p_object(p):
    '''
    object : NUMBER
           | STRING
           | ID
           | NONE
           | TRUE
           | FALSE
           | function
           | tuple
    '''
    p[0] = p[1]


# Error rule for syntax errors
def p_error(p):  # pragma: no cover
    print(p)
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
