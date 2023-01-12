from typing import List
from itertools import combinations


def _to_symbol(val):
	return "T" if val else "F"


class Statement:

	def stmt(self, *args):
		return self.__class__(*args)

	def deconstruct(self):
		return self

	def __eq__(self, other):
		if isinstance(other, Value):
			assert other() is not None, ("You are trying to test equivalence against "
				"an unitialized Value(). Initialize it by using val.true/val.false" )

		return test_equiv([self, other])


class Value(Statement):

	def __init__(self, name):
		self.name = name
		self.__value = None

	def __hash__(self):
		return hash(self.name)

	def __call__(self):
		return self.__value

	def __eq__(self, other):
		assert self.__value is not None, ("You are trying to test equivalence of "
			"an unitialized Value(). Initialize it by using val.true/val.false" )
		return super().__eq__(other)

	@property
	def true(self):
		self.__value = True

	@property
	def false(self):
		self.__value = False

	@property
	def values(self):
		return (self, )

	def __str__(self):
		return _to_symbol(self.__value)

	def __repr__(self):
		return self.name


class Operation(Statement):

	def __repr__(self):
		name = self.__class__.__name__
		if hasattr(self.__class__, "name"):
			name = self.name
		return name


class BinaryOperation(Operation):

	def __init__(self, left: Statement, right: Statement) -> None:
		self.left = left
		self.right = right

	def __call__(self) -> bool:
		assert self.left() is not None and self.right() is not None, \
			("The statement's operands haven't been set to either True or False. "
				"Set them with val.true/val.false")

	def __repr__(self):
		name = super().__repr__()
		return f"({repr(self.left)}{name}{repr(self.right)})"


	@property
	def values(self):
		return tuple(set([val for val in self.left.values] + 
			[val for val in self.right.values]))
	

class UnaryOperation(Operation):
	def __init__(self, operand: Statement):
		self.operand = operand

	def __call__(self) -> bool:
		assert self.operand() is not None, \
		("The statement's operand had't been set to either True or False. "
				"Set it with val.true/val.false")

	def __repr__(self):
		name = super().__repr__()
		return f"{self.name}{repr(self.operand)}"

	@property
	def values(self):
		return tuple({val for val in self.operand.values})


class _not(UnaryOperation):
	name = "\u00ac"

	def __call__(self):
		super().__call__()
		return not self.operand()


class _if(BinaryOperation):
	"""
	Logical IF(A, B) is false if A is True and B is False.
	True everywhere else.
	"""

	name = r" \u21d2 "

	def __call__(self):
		super().__call__()
		return (not self.left()) or self.right()

	def deconstruct(self):
		return _or(_not(self.left.deconstruct()), self.right.deconstruct() )


class _nand(BinaryOperation):
	name = r" \u007c "

	def __call__(self):
		super().__call__()
		return not (not self.left()  and not self.right())

	def deconstruct(self):
		return _not(_and(_not(self.left.deconstruct())), _not(self.right.deconstruct()))


class _nor(BinaryOperation):
	name = " \u2193 "

	def __call__(self):
		super().__call__()
		return not self.left() and not self.right()

	def deconstruct(self):
		return _and(_not(self.left.deconstruct()), _not(self.right.deconstruct()))


class _and(BinaryOperation):
	name = " \u2227 "

	def __call__(self):
		super().__call__()
		return self.left() and self.right()


class _or(BinaryOperation):
	name = " \u2228 "

	def __call__(self):
		super().__call__()
		return self.left() or self.right()


class _xor(BinaryOperation):
	name = " + "

	def __call__(self):
		super().__call__()
		return (self.left() or self.right()) and not (self.left() 
				and self.right())

	def deconstruct(self):
		return _and(_or(self.left.deconstruct(), self.right.deconstruct()), _not(self.left.deconstruct()))


class _diff(BinaryOperation):
	name = " \\ "

	def __call__(self):
		super().__call__()
		return self.left() and (not self.right())

	def deconstruct(self):
		return _and(self.left.deconstruct(), _not(self.right.deconstruct()))


class _symd(BinaryOperation):
	name = " \u2296 "

	def __call__(self):
		super().__call__()
		return (self.left() and not self.right()) or (self.right() and not self.left)

	def deconstruct(self):
		return _or(_and(self.left.deconstruct(), _not(self.right.deconstruct())), 
			_and(self.right.deconstruct(), _not(self.left.deconstruct())))


def build_table(stmts: List):
	vals = list({val for stmt in stmts for val in stmt.values})

	a = list({val for val in combinations([True, False]*len(vals), len(vals))})
	rows = [{t[0].name : t[1] for t in tuple(zip(row[0], row[1]))} for row in zip([vals]*len(a), a)]
	
	header = [repr(val) for val in vals] + [repr(stmt) for stmt in stmts]

	header_s = " | ".join(header)

	header_sep = "|".join([":" + "-"*len(name) + ":" for name in header])
	table = ["| " + header_s + " |", "| " + header_sep + " |"]

	for row in rows:
		row_s = []
		for val in vals:
			if row[val.name]:
				val.true
			else:
				val.false
			row_s.append(str(val))
		for stmt in stmts:
			row_s.append(_to_symbol(stmt()))


		row_s = " | ".join(row_s)
		table.append("| " + row_s + " |")
	
	return "\n".join(table)	


def test_equiv(stmts: List):
	assert all([isinstance(stmt, Operation) for stmt in stmts])

	vals = list({val for stmt in stmts for val in stmt.values})
	a = list({val for val in combinations([True, False]*len(vals), len(vals))})
	rows = [{t[0].name : t[1] for t in tuple(zip(row[0], row[1]))} for row in zip([vals]*len(a), a)]

	results = []

	for row in rows:
		for val in vals:
			if row[val.name]:
				val.true
			else:
				val.false
		result = {stmt() for stmt in stmts}
		results.append(len(result) == 1)

	return all(results)


if __name__ == "__main__":
	a = Value("A")
	b = Value("B")
	c = Value("C")

	print (test_equiv([_and(a,c), _and(a,c)]))
	print (test_equiv([_and(a,c), _or(a,c)]))
