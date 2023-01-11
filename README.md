# truth_tables
A module to build truth tables for logical statements.

# Installing

You can install directly from the repo with:

```
pip install git+https://github.com/agoryuno/truth_tables
```

# Usage

The module defines basic logical operators:

```_and(), _or(), _xor(), _nand(), _nor(), not()```

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

