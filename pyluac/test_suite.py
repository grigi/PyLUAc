'''
PyLUAc Test suite
'''
import unittest

from ply import lex
from pyluac.lexer import lexer
from pyluac.parser import parser


class PyLUAcLexerTest(unittest.TestCase):
    '''
    PyLUAc Lexer test class
    '''

    def test_basic(self):
        'Basic lexing test'
        data = 'print("It\'s Never Lupus!")'
        lexer.input(data)

        tokens = list(lexer)
        self.assertEqual(
            [tok.type for tok in tokens],
            ['ID', '(', 'STRING', ')'])

    def test_indentation(self):
        'Test lexing indentation handling'
        data = 'one\n  \n    two\n    three\n        four\n          five\n\n    six'
        lexer.input(data)

        tokens = list(lexer)
        self.assertEqual(
            [tok.type for tok in tokens],
            ['ID', 'INDENT', 'ID', 'ID', 'INDENT', 'ID', 'INDENT', 'ID', 'DEDENT', 'DEDENT', 'ID', 'DEDENT'])

    def test_strings(self):
        'Test lexing string/multiline-string handling'
        data = '"str1" id1\n  \'str2\'\n  id2\n  """str3\nstr4"""\nid3\n\'\'\'\n\nstr5\n\'\'\'\nid4'
        lexer.input(data)

        tokens = list(lexer)
        self.assertEqual(
            [tok.type for tok in tokens],
            ['STRING', 'ID', 'INDENT', 'STRING', 'ID', 'STRING', 'DEDENT', 'ID', 'STRING', 'ID'])
        self.assertEqual(
            [tok.value for tok in tokens],
            ['str1', 'id1', '', 'str2', 'id2', 'str3\nstr4', '', 'id3', '\n\nstr5\n', 'id4'])
        self.assertEqual(
            [tok.lineno for tok in tokens],
            [1, 1, 2, 2, 3, 4, 6, 6, 7, 11])

    def test_bad_indentation(self):
        'Test lexer failing on bad dedentation'
        data = 'one\n    two\n  three'
        lexer.input(data)

        with self.assertRaisesRegex(lex.LexError, 'Invalid indentation at line 3 col 2'):
            list(lexer)

    def test_whitespace(self):
        'Test that lexer ignores in/trailing whitespace, but not leading whitespace'
        data = 'if a>0: \n    print(a + 10) \n    return a'
        lexer.input(data)

        tokens = list(lexer)
        self.assertEqual(
            [tok.type for tok in tokens],
            ['IF', 'ID', 'LCOMP', 'NUMBER', ':', 'INDENT', 'ID', '(', 'ID', '+', 'NUMBER', ')', 'RETURN', 'ID', 'DEDENT'])

    def test_multiline_not_closed(self):
        '''Test that lexer fails when a multiline string isn't closed'''
        data = '\n"""one\n\n\n\ntwo'
        lexer.input(data)

        with self.assertRaisesRegex(lex.LexError, 'Multiline string not closed at line 2 col 1'):
            list(lexer)


class PyLUAcParserTest(unittest.TestCase):
    '''
    PyLUAc Parser test class
    '''

    def test_basic(self):
        'Basic lexing test'
        data = '1 + (2 + 3) * -4 + f(5)'
        result = parser.parse(data)

        print(result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

