import unittest
from truth_table import _and, _or, _not, _xor, _symd, _diff, _if, Value, build_table, test_equiv


def set_var(var, val):
    if val:
        var.true
        return
    var.false


class MyTests(unittest.TestCase):
    def setUp(self):
        self.a = Value("A")
        self.b = Value("B")
        self.c = Value("C")

    def test_if(self):
        stmt1 = _if(self.a, self.b)
        stmt2 = _or(_not(self.a), self.b)

        vals = [[True, True], [True, False], [False, True],
                [False, False]]
        for av, bv in vals:
            set_var(self.a, av)
            set_var(self.b, bv)
            self.assertEqual(stmt1, stmt2)

    def test_method2(self):
        ...


if __name__ == '__main__':
    unittest.main()


