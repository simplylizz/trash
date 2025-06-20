# String Counter Problem

Welcome to the String Counter repo! This is a repo about counting things related to strings.

## Getting Started

String counters are objects which count things relating to strings.
For example, the length counter can be used to count the number of characters in a string.

```python
from BasicCounters import LengthCounter
lc = LengthCounter() 
lc("hello world!") # == 12
```

We can also count other things about strings

```python
from BasicCounters import VowelCounter, ByteCounter

vc = VowelCounter() 
vc("hello world!") # == 3

uc = ByteCounter("utf-8")
uc("hello world!") # == 12
uc("héllo world! 👋") # == 18
```

And, we can combine counters too! 

```python
from BasicCounters import LengthCounter, VowelCounter, ByteCounter
from ComposedCounters import AdditiveCounter

lc = LengthCounter() 
vc = VowelCounter() 
uc = ByteCounter("utf-8")
summed_counter = AdditiveCounter(lc, vc, uc)
summed_counter("hello world!") # == 27
```

Happy counting : ]

## Your Task

In this repo, we'd like you to implement a way of serializing/de-serializing counters

### Serialization and deserialization

We want a way to treat our code as data. 
Namely, we want to be able to have a way of turning any Counter into a representation that could be stored in a file, or a database, and which is human readable and editable.

Build such a system, such that:
1) The way of serializing counters works with new counters that are added
2) The interface for serialization and deserialization makes sense and is easy to use
3) The code for serialization and deserialization is easily maintainable
4) The serialized representation is easy for humans to read and manipulate.

You'll have two hours to complete this task, at the end of which you will present your solution to a panel of interviewers. You will be assessed not just on your solution and whether it works, but also on your thought process, your ability to weigh tradeoffs between solutions, and the clarity of your explanation.

Happy coding : ]

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt # literally just pytest
```
