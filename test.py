import unittest
import parser
from types import FunctionType


class TestPegFunctions(unittest.TestCase):
    def test_match(self):
        m = parser.match('ab')

        # Testing basic behaviour
        self.assertEqual(type(m), FunctionType)
        self.assertEqual(m('ab'), (True, '', 'ab'))
        self.assertEqual(m('abc'), (True, 'c', 'ab'))
        self.assertEqual(m('_'), (False, '_', None))

        # Testing with regexp
        self.assertEqual(parser.match(r'a*')('aaab'), (True, 'b', 'aaa'))

        # Testing the ignore parameter
        self.assertEqual(parser.match('ab', ignore=r' *')('  ab'),
                         (True, '', 'ab'))
        self.assertEqual(parser.match('ab', ignore=r' *')('\tab'),
                         (False, '\tab', None))

        # Testing the default value for the ignore
        self.assertEqual(m('\n\t  ab '), (True, ' ', 'ab'))

    def test_sequence(self):
        m = parser.match
        s = parser.sequence(m('ab'), m('ab'))

        self.assertEqual(type(s), FunctionType)
        self.assertEqual(s('abab'), (True, '', ['ab', 'ab']))
        self.assertEqual(parser.sequence(m('a'), m('bb'), m('a'))('abba'),
                         (True, '', ['a', 'bb', 'a']))
        self.assertEqual(s('ab_'), (False, 'ab_', None))
        self.assertEqual(s('_'), (False, '_', None))
        self.assertEqual(s('_abab'), (False, '_abab', None))

    def test_choice(self):
        c = parser.choice
        m = parser.match

        self.assertEqual(type(c(m('foo'))), FunctionType)
        self.assertEqual(c(m('a'), m('b'), m('c'))('abc'), (True, 'bc', 'a'))
        self.assertEqual(c(m('a'), m('b'), m('c'))('b'), (True, '', 'b'))
        self.assertEqual(c(m('a'), m('b'), m('c'))('c'), (True, '', 'c'))
        self.assertEqual(c(m('a'), m('b'), m('c'))('_'), (False, '_', None))

    def test_star(self):
        s = parser.star
        m = parser.match

        self.assertEqual(type(s(m('foo'))), FunctionType)
        self.assertEqual(s(m('a'))(''), (True, '', []))
        self.assertEqual(s(m('a'))('_'), (True, '_', []))
        self.assertEqual(s(m('a'))('a'), (True, '', ['a']))
        self.assertEqual(s(m('a'))('aa'), (True, '', ['a', 'a']))
        self.assertEqual(s(m('a'))('aa_'), (True, '_', ['a', 'a']))

    def test_plus(self):
        p = parser.plus
        m = parser.match('a')

        self.assertEqual(type(p(m('foo'))), FunctionType)
        self.assertEqual(p(m)(''), (False, '', None))
        self.assertEqual(p(m)('_'), (False, '_', None))
        self.assertEqual(p(m)('a'), (True, '', ['a']))
        self.assertEqual(p(m)('aa'), (True, '', ['a', 'a']))
        self.assertEqual(p(m)('aa_'), (True, '_', ['a', 'a']))

    def test_optional(self):
        o = parser.optional
        m = parser.match

        self.assertEqual(type(o(m('foo'))), FunctionType)
        self.assertEqual(o(m('a'))('a'), (True, '', 'a'))
        self.assertEqual(o(m('a'))('b'), (True, 'b', None))

    def test_and_predicate(self):
        a = parser.and_predicate
        m = parser.match('a')

        self.assertEqual(type(a(m)), FunctionType)
        self.assertEqual(a(m)('a'), (True, 'a', None))
        self.assertEqual(a(m)('b'), (False, 'b', None))

    def test_not_predicate(self):
        n = parser.not_predicate
        m = parser.match('a')

        self.assertEqual(type(n(m)), FunctionType)
        self.assertEqual(n(m)('a'), (False, 'a', None))
        self.assertEqual(n(m)('b'), (True, 'b', None))

if __name__ == '__main__':
    unittest.main()
