# Definition

A Definition is like a combination of [Enums](https://docs.python.org/3/library/enum.html) and
[bidicts](https://github.com/jab/bidict). They all do similar things, but, have some small differences.

## Comparison

### How to construct

```python
# Functional interface also available
class MyEnum(Enum):
    A = 1
    B = 2

my_bidict = bidict({"A": 1, "B": 2})

class MyDefinition(Definition):
    A = 1
    B = 2
```

### Value Access

```python
>>> print(MyEnum.A)
<MyEnum.A: 1>
>>> print(MyEnum["A"])
<MyEnum.A: 1>
>>> print(MyEnum.A.value)
1
>>> print(my_bidict["A"])
1
>>> print(MyDefinition.A)
1
>>> print(MyDefinition["A"])
1
```

### Key access

```python
>>> print(MyEnum(1))
<MyEnum.A: 1>
>>> print(MyEnum(1).value)
"A"
>>> print(my_bidict.inverse[1])
"A"
>>> print(MyDefinition(1))
"A"
```

### Equality

```python
>>> MyEnum.A == 1
False
>>> MyEnum.A.value == 1
True
>>> my_bidict["A"] == 1
True
>>> MyDefinition.A == 1
True
```


### Uniqueness

Enum:

- Duplicate values allowed by default, they are considered
  [aliases](https://docs.python.org/3/library/enum.html#duplicating-enum-members-and-values),
  so reverse access will return the first key that defined the value.
- Can make value uniqueness requirement with [@unique](https://docs.python.org/3/library/enum.html#enum.unique)
  decorator

bidict:

- Keys and values must be unique and hashable.


Definition:

- Keys and values must be unique and hashable by default.
- Uniqueness can be turned off with `class A(Definition, unique=False)`, but in this mode reverse access
  is not allowed, since definitions are not considered each other's aliases. However, values can now be
  non-hashable, since reverse key map is not required.


### Benchmarks:

① Creating 100 000 instances with 3 members (A=1, B=2, C=3):

- Enum: 5.1 s.
- bidict: 0.66 s.
- Definition: 1.1 s.
