'''
PyLUAc Test suite
'''
import unittest

from ply import lex
from pyluac.lexer import lexer

class PyLUAcLexerTest(unittest.TestCase):
    '''
    PyLUAc Lexer test class
    '''

    def test_basic(self):
        data = 'print("It\'s Never Lupus!")'
        lexer.input(data)

        tokens = list(lexer)
        self.assertEqual([tok.type for tok in tokens],
            ['ID', '(', 'STRING', ')'])

    def test_indentation(self):
        data = 'one\n  \n    two\n    three\n        four\n          five\n\n    six'
        lexer.input(data)

        tokens = list(lexer)
        self.assertEqual([tok.type for tok in tokens],
            ['ID', 'INDENT', 'ID', 'ID', 'INDENT', 'ID', 'INDENT', 'ID', 'DEDENT', 'DEDENT', 'ID', 'DEDENT'])

    def test_bad_indentation(self):
        data = 'one\n    two\n  three'
        lexer.input(data)

        with self.assertRaisesRegex(lex.LexError, 'Invalid indentation'):
             tokens = list(lexer) 
    

if __name__ == '__main__':
    unittest.main()

