'''
PyLUAc Test suite
'''
import unittest

from pyluac.lexer import lexer

class PyLUAcLexerTest(unittest.TestCase):
    '''
    PyLUAc Lexer test class
    '''

    def test_basic(self):
        data = 'print("It\'s Never Lupus!")'
        lexer.input(data)

        tokens = list(lexer)
        assert [tok.type for tok in tokens] == ['ID', '(', 'STRING', ')']

    #def test_for_1(self):
        
    

if __name__ == '__main__':
    unittest.main()

