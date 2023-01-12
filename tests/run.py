import unittest
from truth_table import _and, _or, _not, _xor, _symd, _diff, _if, Value, build_table, test_equiv


def set_var(var, val):
	if val:
		var.true
		return
	var.false


class MyTests(unittest.TestCase):
    def setUp(self):
        a = Value("A")
        b = Value("B")
        c = Value("C")

    def test_if(self):
        stmt1 = _if(a, b)
        stmt2 = _or(_not(a), b)

        vals = [[True, True], [True, False], [False, True],
        		[False, False]]
        for av, bv in vals:
        	set_var(a, av)
        	set_var(b, bv)
        	self.assertEqual(stmt1 == stmt2)

    def test_method2(self):
        # test method 2 code and assertions

    def tearDown(self):
        # code to be executed after each test method

if __name__ == '__main__':
    unittest.main()


