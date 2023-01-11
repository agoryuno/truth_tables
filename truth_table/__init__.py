from typing import overload, List
from itertools import combinations, product, permutations


def _to_symbol(val):
	return "T" if val else "F"


class Statement:

	def stmt(self, *args):
		return self.__class__(*args)


class Value(Statement):

	def __init__(self, name):
		self.name = name
		self.__value = None

	def __call__(self):
		return self.__value

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
		assert self.left() is not None and self.right() is not None

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
		assert self.operand() is not None

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


class _nand(BinaryOperation):
	name = r" \| "

	def __call__(self):
		super().__call__()
		return not (not self.left()  and not self.right()) 


class _nor(BinaryOperation):
	name = " \u2193 "

	def __call__(self):
		super().__call__()
		return not self.left() and not self.right()


class _and(BinaryOperation):
	name = " \u0245 "

	def __call__(self):
		super().__call__()
		return self.left() and self.right()


class _or(BinaryOperation):
	name = " V "

	def __call__(self):
		super().__call__()
		return self.left() or self.right()


class _xor(BinaryOperation):
	name = " + "

	def __call__(self):
		super().__call__()
		return (self.left() or self.right()) and not (self.left() 
				and self.right())



def build_table(stmts: List):
	all_vals = {val for stmt in stmts for val in stmt.values}
	#each_vals = [{val for val in stmt.values} for stmt in stmts]
	#assert all([vals == all_vals for vals in each_vals])

	vals = list(all_vals)

	val_combos = [i for val in vals for i in [(True, val), (False, val)] ]
	rows = [val for val in combinations(val_combos, len(all_vals))]

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


if __name__ == "__main__":
	a = Value("A")
	b = Value("B")
	c = Value("C")

	print (build_table([_and(_or(a,c), _not(b))]))
