# PyScrabbler

A Python package for retrieving a list of valid words and their values in Scrabble™ given a set of letters [seven to fifteen].

## Description

### Methods

```py
getScrabbleWords(letters)
```

**Parameter**: _String_; provided letters.<br>
**Returns**: _2D-List_; words and their base values.<br>

**Exceptions**:<br>
&emsp;`Error: Letter count must be between seven and fifteen.`: occurs when provided _String_ is less than seven characters OR longer than fifteen characters.<br>
&emsp;`Error: No argument provided.`: occurs when not provided with an argument.


**Example Use In Code**:

```py
storedWords = getScrabbleWords('JUHSINE')
for word in storedWords:
  print(word)
```

**Example Use In Terminal**:

```bash
python pyscrabbler.py a,r,t,w,t,x,y,z
```

**Example Output**:

```
['EH', 5]
['EHS', 6]
['EISH', 7]
['EN', 2]
['ENS', 3]
['ES', 2]
['HE', 5]
['HEN', 6]
['HENS', 7]
...
```

## Installation

Coming soon!

## Legal

This project was developed for educational purposes. I do not own, nor claim to own, anything involving Scrabble™. Scrabble™ is a trademark owned by Hasbro Inc. and all rights are reserved to its respective owner.
