# QWorder
QWorder simplifies strings representing sequences of quantum gates.

# Installation

`pip install qworder`

# Sample usage
Define a word "HXTTXZXH" with positive sign, and cascade reduce it with `cascade_word()`

```   
w = Word("HXYYXZXH", True)
c = Cascader()
print(w)
print(c.cascade_word(w))
```

The output will be:

```
['HXYYXZXH', True]
['Y', True]
```
