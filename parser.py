import re


def match(pattern, ignore=r'[\n\t\r ]*'):
    def parse(i):
        m = re.match(r'%s(%s)' % (ignore, pattern), i)
        if m:
            return True, i[len(m.group(0)):], m.group(1)
        else:
            return False, i, None
    return parse


def sequence(*es):
    def parser(i):
        p = i
        ns = []
        for e in es:
            s, p, n = e(p)
            ns.append(n)
            if not s:
                return False, i, None
        return True, p, ns
    return parser


def choice(*es):
    def parser(i):
        for e in es:
            s, p, n = e(i)
            if s:
                return True, p, n
        return False, i, None
    return parser


def star(e):
    def parser(i):
        s, p, ns = True, i, []
        while s:
            s, p, n = e(p)
            ns.append(n)
        ns.pop()
        return True, p, ns
    return parser


def plus(e):
    def parser(i):
        s, p, n = sequence(e, star(e))(i)
        if s:
            return True, p, [n[0]] + n[1]
        else:
            return False, i, None
    return parser


def optional(e):
    def parser(i):
        s, p, n = e(i)
        return True, p, n
    return parser


def and_predicate(e):
    def parser(i):
        s, p, n = e(i)
        return s, i, None
    return parser


def not_predicate(e):
    def parser(i):
        s, p, n = e(i)
        return not s, i, None
    return parser
