'''
PyLUAc parser
'''
# pylint: disable=C0103,C0301
import ply.yacc as yacc


# Get the token map from the lexer.  This is required.
from pyluac.lexer import tokens  # pylint: disable=W0611

precedence = (
    ('left', 'EQUALS', 'NEQUALS', 'LECOMP', 'GECOMP', 'LCOMP', 'GCOMP'),
    ('left', 'ID'),
    ('right', ','),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('left', '(', ')'),
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
    statement : if
              | while
              | vested
    '''
    p[0] = p[1]


def p_if(p):
    '''
    if : IF comparison ':' INDENT block DEDENT ifcont
    '''
    p[0] = ('if', p[2], p[5], p[7])


def p_ifcont(p):
    '''
    ifcont : ELIF comparison ':' INDENT block DEDENT ifcont
           | ELSE ':' INDENT block DEDENT
           |
    '''
    if len(p) == 1:
        p[0] = []
    elif p[1] == 'elif':
        p[0] = [('if', p[2], p[5], p[7])]
    else:
        p[0] = p[4]



def p_while(p):
    '''
    while : WHILE comparison ':' INDENT block DEDENT
    '''
    p[0] = ('while', p[2], p[5])


def p_vested(p):
    '''
    vested : assignment
           | comparison
           | return
    '''
    p[0] = p[1]


def p_return(p):
    '''
    return : RETURN comparison
    '''
    p[0] = ('return', p[2])


def p_assignment(p):
    '''
    assignment : IDASSIGN comparison
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
    expressionlist : expressionlist ',' comparison
                   | expressionlist ','
                   | comparison
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


def p_comparison(p):
    '''
    comparison : expression EQUALS comparison
               | expression NEQUALS comparison
               | expression LECOMP comparison
               | expression GECOMP comparison
               | expression LCOMP comparison
               | expression GCOMP comparison
               | expression %prec ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('comparison', [p[2]], [p[1], p[3]])
        try:
            if p[3][0] == 'comparison':
                p[0] = ('comparison', [p[2]], [p[1]])
                p[0][1].extend(p[3][1])
                p[0][2].extend(p[3][2])
        except TypeError:
            pass
    #p[0] = p[1:]


def p_expression(p):
    '''
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | expression '%' expression
               | '-' expression %prec UMINUS
               | '(' comparison ')' %prec BRACKET
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
    'Unexpected error - should fail hard'
    print(p)
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
