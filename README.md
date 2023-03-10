# truth_tables
A module to build truth tables for logical statements and more!

<a name="toc" />

##### Contents
- [Installing](#installing)
- [Creating statements](#creating-statements)
- [Evaluating statements](#evaluating-statements)
- [Elementary operations](#elementary-operations)
- [Printing truth tables](#printing-truth-tables)
- [Testing equivalence](#testing-equivalence)
- [Analyze equivalence](#analyze-equivalence)



## Installing
[↑to top](#toc)

You can install directly from the repo with:

```
pip install git+https://github.com/agoryuno/truth_tables
```

## Creating statements 
[↑to top](#toc)


The module defines basic logical connectives:

```_and(), _or(), _xor(), _nand(), _nor(), _not(), _if(), _iff()```

and two operations on sets: `_symd()` - symmetric difference and 
`_diff()` - difference between two sets.

Unions and intersections can be represented with `_or()` and `_and()`
respectively.

Values are created using class `Value()` that takes the
value's name as its only argument:

```a = Value("A")```

A value can be set True or False:

```
a.true
a.false
```
A statement `A and B` can be created with:

```
a = Value("A")
b = Value("B")
_and(a, b)
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

## Evaluating statements
[↑to top](#toc)

Once a statement is created it can be evaluated for the given values. Consider a statement
with three values: `((A ∨ C) ⊖ (B \ C))`

```
a, b, c = Value("A"), Value("B"), Value("C")

stmt = _symd(_or(a, c), _diff(b, c))
```

The `stmt` object can be evaluated by setting the values and calling it as a function, like so:

```
a.true
b.true
c.false
stmt()
```

Output:

```False```

Trying to evaluate a statement without properly initializing it's operand values will result
in an AssertionError.

## Elementary operations
[↑to top](#toc)

All statements, except for values and elementary operations: `_and()`, `_or()`, and `_not()`,
can be represented in terms of elementary operations and values by using their `deconstruct()` method.

For instance, "deconstructing" the statement `(A ⊖ (B + C))`

```
_symd(a, _xor(b, c)).deconstruct()
```

yields:

```
((A ∧ ¬((B ∨ C) ∧ ¬B)) ∨ (((B ∨ C) ∧ ¬B) ∧ ¬A))
```

This can be useful both as a means of reminding yourself what exactly a particular operation
does, and as the first step to analyzing statements by way of using truth tables.

Using the `deconstruct()` method on a `Value()` object or an elementary statement is perfectly safe - 
it will simply return the value or the statement itself.

## Printing truth tables
[↑to top](#toc)

Function `build_table()` is used to construct a Markdown representation of a truth table.
`build_table()` takes an iterable with logical statements and returns a table with a column
for each `Value()` used in all of the statements, and a column for each individual statement. 

Following is a complete example of creating the truth table for expression: `((A ∧ B) ∨ C)`.
Note the extra steps needed to print the table in a notebook.

```
from IPython.display import display, Markdown
from truth_table import _and, _or, _not, _xor, Value, build_table

a = Value("A")
b = Value("B")
c = Value("C")

stmt = _or(_and(a, b), c)
display(Markdown(build_table([stmt])))
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

And you can certainly use statements to construct other statements:

```
a,b,c = Value("A"), Value("B"), Value("C")

stmt1 = _or(a, b)
stmt2 = _symd(stmt1, c)
stmt3 = _symd(a, c)
stmt4 = _diff(b, a)
stmt5 = _symd(stmt3, stmt4)

display(Markdown(build_table([stmt1, stmt3, stmt4, stmt5, stmt2])))
```

Output:

| B | A | C | (A ∨ B) | (A ⊖ C) | (B \ A) | ((A ⊖ C) ⊖ (B \ A)) | ((A ∨ B) ⊖ C) |
| :-:|:-:|:-:|:-------:|:-------:|:-------:|:-------------------:|:-------------: |
| T | F | T | T | F | T | F | F |
| T | T | F | T | T | F | T | T |
| F | T | F | T | T | F | T | T |
| F | F | F | F | F | F | F | F |
| T | F | F | T | F | T | F | T |
| F | F | T | F | F | F | F | F |
| T | T | T | T | F | F | F | F |
| F | T | T | T | F | F | F | F |

## Testing equivalence
[↑to top](#toc)

Function `test_equiv()` can be used to test the logical equivalence of multiple statements.
It takes a list of statements as its only argument and returns True if all statements are
equivalent for all combinations of their boolean values, and False otherwise.

Taking inspiration from exercise 14 from section 1.4 of the "How To Prove It: A Structured Approach. Second Edition" book by
Daniel Velleman: 

a) are `((A ∨ B) ⊖ C)` and `((A ⊖ C) ⊖ (B \ A))` equivalent:

```
a, b, c = Value("A"), Value("B"), Value("C")

stmt1 = _symd(_or(a, b), c)

stmt2 = _symd(a, c)
stmt3 = _diff(b, a)
stmt4 = _symd(stmt2, stmt3)

test_equiv([stmt1, stmt4])
```

Output:

`False`

b) `((A ∧ B) ⊖ C)` and `((A ⊖ C) ⊖ (A \ B))`:

```
stmt1 = _symd(_or(a, b), c)

stmt2 = _symd(a, c)
stmt3 = _diff(b, a)
stmt4 = _symd(stmt2, stmt3)

test_equiv([stmt1, stmt4])
```

Output:

`True`

c) `((A \ B) ⊖ C)` and `((A ⊖ C) ⊖ (A ∧ B))`:

```
stmt1 = _symd(_diff(a, b), c)
stmt2 = _symd(a, c)
stmt3 = _and(a, b)
stmt4 = _symd(stmt2, stmt3)

test_equiv([stmt1, stmt4])
```

Output:

`True`

Equivalence of two statements can be tested with the standard "==" operation. For example:

```
_symd(a, _xor(b, c)) == _and(_xor(b,c), a)
```

Output:

```
False
```

You can test values and operations for equivalence, but values need to be set for that. An unitialized value in
an equivalence test will raise an AssertionError. This is to enforce the difference between a logically valid 
false equivalence test result and a false result due to an unitialized value.

## Analyze equivalence
[↑to top](#toc)

We can use truth tables to confirm the `test_equiv()` result of a) in the previous section.
Namely, `((A ∨ B) ⊖ C)` and `((A ⊖ C) ⊖ (B \ A))` not being equivalent.

```
a, b, c = Value("A"), Value("B"), Value("C")

stmt1 = _symd(_or(a, b), c)

stmt2 = _symd(a, c)
stmt3 = _diff(b, a)
stmt4 = _symd(stmt2, stmt3)

display(Markdown(build_table([stmt2, stmt3, stmt4, stmt1])))
```
Output:

| B | A | C | (A ⊖ C) | (B \ A) | ((A ⊖ C) ⊖ (B \ A)) | ((A ∨ B) ⊖ C) |
| :-:|:-:|:-:|:-------:|:-------:|:-------------------:|:-------------: |
| T | F | T | F | T | F | F |
| T | T | F | T | F | T | T |
| F | T | F | T | F | T | T |
| F | F | F | F | F | F | F |
| T | F | F | F | T | F | T |
| F | F | T | F | F | F | F |
| T | T | T | F | F | F | F |
| F | T | T | F | F | F | F |

The only difference between the two statements is in the 5th row where `B=True`, `A=False` and `C=False`.

[↑Back to top](#toc)
