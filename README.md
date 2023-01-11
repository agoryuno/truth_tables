# truth_tables
A module to build truth tables for logical statements.

# Installing

You can install directly from the repo with:

```
pip install git+https://github.com/agoryuno/truth_tables
```

# Creating statements

The module defines basic logical operators:

```_and(), _or(), _xor(), _nand(), _nor(), _not()```

Values are created using class `Value()` that takes the
value's name as its only argument:

```a = Value("A")```

An expression `A not B` can be created with:

```
a = Value("A")
b = Value("B")
_not(a, b)
```

Two more examples:

```
p,q,r = Value("P"), Value("Q"), Value("R")
_and(p, _or(q, r))
_xor(q, _and(_not(p), r))
```

Any logical statement can be printed out using standard notation:

```
repr(_xor(q, _and(_not(p), r)))
```

Outputs: `(Q + (¬P Ʌ R))`

# Printing truth tables

Function `build_table()` is used to construct a Markdown representation of a truth table.
`build_table()` takes an iterable with logical statements and returns a table with a column
for each `Value()` used in all of the statements, and a column for each individual statement. 

Following is a complete example of creating the truth table for expression: `(A and B) or C`.
Note the extra steps needed to print the table in a notebook.

```
from IPython.display import display, Markdown, Latex
from truth_table import _and, _or, _not, _xor, Value, build_table

a = Value("A")
b = Value("B")
c = Value("C")

stmt = _or(_and(a, b), c)
display(Markdown(build_table([stmt]))
```

Outputs:

| B | A | C | ((A Ʌ B) V C) |
| :-:|:-:|:-:|:-------------: |
| T | F | T | T |
| T | T | F | T |
| F | T | F | F |
| F | F | F | F |
| T | F | F | F |
| F | F | T | T |
| T | T | T | T |
| F | T | T | T |


Or you could separate the full statement into two component statements to make it easier to analyze:

```
stmt1 = _and(a,b)
stmt2 = _or(_and(a,b), c)
display(Markdown(build_table([stmt1, stmt2])))
```

Output:

| C | A | B | (A Ʌ B) | ((A Ʌ B) V C) |
| :-:|:-:|:-:|:-------:|:-------------: |
| T | F | T | F | T |
| T | T | F | F | T |
| F | T | F | F | F |
| F | F | F | F | F |
| T | F | F | F | T |
| F | F | T | F | F |
| T | T | T | T | T |
| F | T | T | T | T |
