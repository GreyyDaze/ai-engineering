# Python for AI Engineering

---

Revisited the following Python topics from the perspective of AI engineering:

→ Python and why it dominates AI
→ Variables, data types, and mutability
→ Data structures (list, tuple, dict, set)
→ Control flow (if/elif/else, for, while, break, continue)
→ Functions
→ Scope
→ Modules and imports
→ File I/O
→ Error handling
→ String manipulation

---

## Subtopic 1 — Python and Why It Dominates AI

**What it is →** An interpreted language. Executes code line by line. If a line contains an error, everything after it stops until resolved.

**Compiled vs Interpreted →** A compiled language compiles the whole code into bytecode first, then converts to machine code. Errors thrown at compile time. Python skips this — you write it, you run it.

**Dynamic Typing →** You don't declare a type. Python infers it from the value.

```python
name = "Aminah"
print(type(name))    # <class 'str'>
```

**Indentation →** Python doesn't use brackets. Indentation defines code blocks.

**Why Python Dominates AI →** Every AI library is written in Python — LangChain, FastAPI, Qdrant, Langfuse, DSPy. The real reason is ecosystem lock-in. NumPy (2005), Pandas (2008), PyTorch (2016) — all built in Python before LLMs arrived. New tools were built in Python because the users were already there. Python also calls C/C++ underneath for heavy computation — NumPy, PyTorch, TensorFlow run C code under the hood. Python is just the instruction layer. No other language can catch up now.

**Summary →** Interpreted so runs line by line → dynamic typing so write faster → C/C++ underneath for performance → ecosystem lock-in makes it permanent.

---

## Subtopic 2 — Variables, Data Types, and Mutability

**Variable →** A name that points to a value in memory. Python creates the value in memory, creates a label, and points the label to that location.

**Data Types →**

```python
name   = "Aminah"    # string
age    = 25          # integer
salary = 100.3       # float
active = True        # boolean
result = None        # None
```

**Why None is Special →** Not an empty string, not zero, not False. Means nothing is here. It is its own object. When an LLM API call fails silently, the variable holds None. If you don't catch it, the code crashes downstream with a confusing error.

```python
response = None

if response is None:    # correct — checks same object in memory
    print("call failed")

if response == "":      # wrong — misses None entirely
    print("call failed")
```

`is` checks if it is the exact same object in memory. `==` checks if values are equal.

**Mutability →** Mutability means a value can be changed in memory directly. Immutability means any operation creates a new value and the previous one gets garbage collected.

```
Mutable   → list, dictionary, set
Immutable → string, integer, float, boolean, tuple, None
```

**Immutable example →**

```python
name = "  Aminah  "
name.strip()           # creates new value, no label points to it
print(name)            # "  Aminah  " — unchanged

name = name.strip()    # now label points to new value
print(name)            # "Aminah"
```

In document cleaning this haunts you if you DON'T reassign.

**Mutable example →**

```python
l = [1, 2]
l.append(3)
print(l)    # [1, 2, 3] — changed directly in memory
```

**Check memory location →**

```python
name = "  Aminah  "
print(id(name))         # memory location A

name = name.strip()
print(id(name))         # memory location B — new value, new location

l = [1, 2]
print(id(l))            # memory location C

l.append(3)
print(id(l))            # memory location C — same, changed in place
```

**Mutable default argument →** Default arguments are stored on the function object itself, not in the local namespace. This is why even though the local namespace is destroyed after the function ends, a mutable default persists across calls. Each call points `items` to the same list attached to the function object.

```python
# Wrong — data leaks across calls
def collect(items=[]):
    items.append("new")
    return items

collect()
collect()
print(collect.__defaults__)    # (['new', 'new', 'new'],)

# Right
def collect(items=None):
    if items is None:
        items = []
    items.append("new")
    return items
```

**Summary →** Variable is a name pointing to value in memory → 5 types: string, integer, float, boolean, None → None means nothing is here, check with `is None` → immutable types create new values on every operation, must reassign → mutable types change in place → never use mutable types as default arguments or data leaks across calls.

---

## Subtopic 3 — Data Structures

Data structures are containers that hold multiple values.

---

### List

**Definition →** Ordered and mutable collection. Ordered means items placed by position. Mutable means can add, update, or delete items.

**How it works →** Creates a memory block in sequence and stores item references there.

**Syntax:**

```python
list1 = ["1.txt", "2.txt"]
list1[0]                          # access by index
list1[-1]                         # reverse order
list1.append("3.txt")             # add to end
list1.insert(0, "0.txt")          # insert at position
del list1[0]                      # remove by index
list1.remove("1.txt")             # remove by value
list1.pop()                       # remove and return last
len(list1)                        # length
"1.txt" in list1                  # check existence
list1[0:2]                        # slice [start:end:step]
```

**Quirk →** `b = a` saves the memory reference — does not copy. Use `.copy()` for an independent copy.

**In AI systems →** List of filenames, list of processed chunks, list of search results from vector DB.

---

### Tuples

**Definition →** Ordered and immutable collection. Like a list but marked as read-only.

**Why it exists →** When you don't want the collection modified accidentally. Python also returns multiple values from a function as a tuple automatically.

**Syntax:**

```python
t = ("gpt-4o", 0.7)
t[0]                              # access by index
t1, t2 = ("gpt-4o", 0.7)         # unpack
```

**Quirk →** Single item tuple needs trailing comma — `t = ("gpt-4o",)`. Without it Python treats it as a string in parentheses.

**In AI systems →** Model configuration (fixed values) and function return values.

---

### Dictionaries

**Definition →** Unordered collection of key-value pairs. Access by key, no index needed.

**How it works →** Keys stored in a hash table. Key is hashed by a hash function that returns a number determining the value's location in memory. Same hash function used when searching. Because of this, search is fast regardless of dictionary size. Keys must be immutable.

**Syntax:**

```python
person = {"name": "Aminah", "age": 25}
person["name"]                        # access by key — throws KeyError if missing
person.get("name")                    # safe access — returns None if missing
person.get("name", "unknown")         # safe access with default
person["city"] = "Islamabad"          # add or update
del person["age"]                     # delete by key
person.pop("age")                     # delete and return value
for key, value in person.items():     # loop
person.keys()                         # all keys
person.values()                       # all values
```

**Quirk →** Don't use `[]` to access a key — throws KeyError if not found. Use `.get()` — no error, can set a default.

**In AI systems →** LLM API responses and model configurations.

---

### Set

**Definition →** Unordered collection of unique values.

**How it works →** Hash value before storing. When adding a new value, uses hash to check if it already exists — if it does, it's a duplicate and not added.

**Syntax:**

```python
s = {"doc.txt", "doc2.txt"}
s.add("doc3.txt")                     # add
s.discard("doc.txt")                  # safe remove
s.remove("doc.txt")                   # unsafe remove — error if missing
"doc.txt" in s                        # check membership
s1 | s2                               # union
s1 & s2                               # intersection
s1 - s2                               # difference
```

**Quirk →** `{}` is an empty dictionary not an empty set. Use `set()` for an empty set.

**In AI systems →** Tracking processed files and removing duplicates.

---

### When to Use Each

```
List       → ordered, will modify → chunks, results, file lists
Tuple      → ordered, must not change → configs, return values
Dictionary → key-value lookups → API responses, metadata
Set        → unique items, fast checks → tracking, deduplication
```

---

## Subtopic 4 — Control Flow

Runs code based on a condition, runs code repeatedly until a sequence ends or condition is met, or skips an action based on a condition.

---

### if/elif/else

**Definition →** Runs a code block when the first True condition is found.

**How it works →** Checks expression after `if`/`elif`. Runs the block or moves on. `else` runs when nothing above is True.

**Syntax:**

```python
score = 10

if score > 10:
    print("score greater than 10")
elif score == 10:
    print("score equals 10")
else:
    print("score less than 10")
```

**Quirk →** Python doesn't only check for explicit `True` — `None`, `0`, `""`, `{}`, `[]` all evaluate as False. An LLM response could be `0` or `""` which are valid responses. Using just the variable runs the wrong code. Always check for explicit `None` using `is not None`.

---

### for Loop

**Definition →** Takes a sequence of items and runs code continuously until the last item is reached.

**How it works →** An iterator tracks the current position. On the last item the iterator signals `StopIteration` which ends the loop.

**Syntax:**

```python
list1 = [1, 2, 3]
for i in list1:
    print(i)

for key, value in dict1.items():    # dictionary
for index, i in enumerate(list1):   # with index
for i in range(5):                  # specific range
clean = [f for f in files if f.endswith(".txt")]    # list comprehension
```

**Quirk →** Don't modify the list in a for loop — results in missing items because the sequence shifts but the iterator doesn't know.

---

### while Loop

**Definition →** Runs until the condition becomes False. A for loop runs on a fixed sequence. A while loop runs indefinitely until the condition becomes False.

**How it works →** Checks condition and runs, then checks again and runs. Repeats until False.

**Syntax:**

```python
score = 0

while score < 10:
    print("score hasn't reached 10")
    score += 1
```

**Quirk →** If the condition never becomes False the loop runs infinitely. Always have an exit condition or a `break` statement.

**In AI systems →** Agent calling tools with a max steps limit.

---

### break and continue

**Definition →** `break` stops the loop entirely. `continue` skips the current iteration. Use `break` to stop when a critical operation fails and `continue` to skip a bad step.

**Syntax:**

```python
score = 0

while score <= 10:
    score += 1
    if score == 5:
        continue    # skips print for this iteration
    if score == 10:
        break       # stops the loop at 10
    print("score hasn't reached 10")
```

---

## Subtopic 5 — Functions

**What it is →** A named block of code that can be reused. Instead of writing logic 10 times, write it once and call it every time needed.

**Definition →** Takes parameters (input), runs some logic, and optionally returns the output.

**How it works →** On the `def` keyword, a function object is created in memory. When called, a local namespace is created — a temporary dictionary that holds all variables inside that call. Parameters are assigned, code runs, output is returned, and the local namespace is destroyed.

**Syntax:**

```python
def hello(name):
    print("Hello " + name)

hello("Guest")

def func(a, b, c):                        # multiple parameters
    return a, b, c                         # multiple return values as tuple

a, b, c = func(1, 2, 3)                   # unpack return values

def call_llm(prompt, temperature=0.7):    # default parameter
    pass

call_llm("question", temperature=0)       # keyword argument
```

Keyword arguments — when parameters become 5+ it becomes difficult to know what value belongs to what without looking at the function definition. Keywords make the function self-documenting. For keyword arguments order does not matter but for positional arguments it does.

**Quirks →**

No return means `None` is returned — causes issues in the pipeline with a vague error downstream.

Mutable default argument — default arguments are stored on the function object, not in the local namespace. Even though the local namespace is destroyed after the function ends, a mutable default persists across calls.

```python
# Wrong
def collect(items=[]):
    items.append("new")
    return items

# Right
def collect(items=None):
    if items is None:
        items = []
    items.append("new")
    return items
```

**In AI systems →** Functions make an AI system modular. Swap, replace, or delete a step without causing issues for other parts.

---

## Subtopic 6 — Scope

**Definition →** Scope tells you where a variable is visible. A variable defined inside a function is only visible inside that function. A variable defined globally can be seen by all.

**How it works →** Variable is found using the LEGB rule — Local (current function), Enclosing (outer function), Global (top level of file), Built-in (Python's built-in names like `print`, `len`). Python searches in this order and uses the first match.

**Syntax:**

```python
# Local — NameError outside function
def x_call():
    x = 2
    print(x)

x_call()
print(x)    # NameError

# Global — visible inside functions
x = 3

def x_call():
    print(x)

# Cannot modify global — UnboundLocalError
x = 3

def x_call():
    x += 1    # UnboundLocalError
    print(x)

# global keyword — allows modification
x = 3

def x_call():
    global x
    x += 1
    print(x)
```

**Quirk →** Don't use `global` in production code. If 10 functions use a global variable and there's an error, you can't know which function modified it. Pass in and return out for a traceable pipeline.

**In AI systems →** Every step has its own local scope — easier to debug and nothing leaks between steps.

---

## Subtopic 7 — Modules and Imports

**Definition →** A module is a `.py` file that contains functions, classes, and variables that other files can import. Divide code into modules instead of writing everything in one file.

**How it works →** On import, Python first checks `sys.modules` (cache). If not found, searches current directory, `sys.path` (virtual environment `/lib`), or built-in modules. Executes file top to bottom and caches the module. First import runs the file. Second import reuses from cache.

**Syntax:**

```python
import os                              # full module — use module name to access
from os.path import exists, join       # specific items — use directly
import numpy as np                     # alias — use community conventions
from file_reader import read_file      # your own module
```

**Three types of packages:**

- Standard library — available on Python install, no separate install needed
- Third-party — installed using `pip` which downloads from PyPI
- Your own modules — imported from current directory or project subdirectory

**Quirks →**

Top-level code runs on import — any code NOT inside a function or class sits at the root of the file and runs when imported. Guard it:

```python
if __name__ == "__main__":
    # only runs when: python utils.py
    # does NOT run when imported
    helper()
```

`__name__` is `"__main__"` when run directly. When imported, `__name__` is the module name.

Circular dependency — file A imports from file B and file B imports from file A. Python throws an error. Fix by creating a separate file with shared code and importing from there.

**In AI systems →** Code divided into modules gives each file one responsibility. Issue in a step — only check files related to that step.

---

## Subtopic 8 — File I/O

**Why we learn this →** Ingesting data into an AI system requires reading and writing files.

**What it is →** File I/O allows reading data from a file and writing data to disk.

**How it works →** Opening a file communicates with the OS to create a handle — a connection between the program and the file on disk. Data flows through it. Not closing causes three problems: file stays locked so other programs can't access it, data fails to save because it's still in memory and not flushed to disk, or the program crashes because too many files are open. The `with` statement closes the file after the block completes, even on error.

**Syntax:**

```python
# Dangerous — file stays open on error
f = open("file.txt", "r")
content = f.read()
f.close()

# Safe — closes even on error
with open("file.txt", "r") as f:
    content = f.read()              # entire file as string — small files
    lines = f.readlines()           # list of lines
    for line in f:                  # line by line — large files
        print(line)

with open("file.txt", "w") as f:    # write — creates or overwrites
    f.write("text")

with open("file.txt", "a") as f:    # append — preserves existing content
    f.write("text")
```

JSON:

```python
import json

with open("config.json", "r") as f:
    data = json.load(f)                 # JSON file → Python dict

with open("results.json", "w") as f:
    json.dump(data, f, indent=2)        # Python dict → JSON file

data = json.loads('{"model": "gpt-4o"}')   # JSON string → Python dict
json_string = json.dumps(data)              # Python dict → JSON string
```

`load`/`dump` for files. `loads`/`dumps` for strings. `indent=2` makes JSON human-readable.

**Quirks →**

Always specify `encoding="utf-8"`. Without it Python uses system default which differs across machines — works locally, crashes in production.

After `readlines()` always strip newline characters:

```python
lines = [line.strip() for line in lines]
```

**In AI systems →** First and most important step in RAG and Agentic RAG — every document enters the pipeline through file I/O.

---

## Subtopic 9 — Error Handling

**What it is →** Handling errors before letting things go wrong. Instead of crashing, catch the error, do something about it, and continue.

**How it works →** When an error occurs, Python creates an exception object with the error type, message, and exact line (traceback). Python walks up the call stack — from current function to whoever called it — to find a `try/except` block that catches that error type. If found, runs the `except` block. If not found, crashes and prints the traceback.

**Syntax:**

```python
# Basic
try:
    n = 10 / 0
except ZeroDivisionError:
    print("cannot divide by zero")

# Multiple errors — Python runs first matching block
try:
    with open("data.txt", "r") as f:
        content = f.read()
    number = int(content)
except FileNotFoundError:
    print("file not found")
except ValueError:
    print("content is not a valid number")

# finally — always runs regardless of error
try:
    result = call_llm(prompt)
except Exception as e:
    result = None
finally:
    print("always runs")

# Capture error message
except FileNotFoundError as e:
    print(f"Error: {e}")
```

**Common errors:**

- `FileNotFoundError` — file doesn't exist
- `ValueError` — wrong value type
- `TypeError` — wrong type in operation
- `KeyError` — key not found in dictionary
- `UnicodeDecodeError` — wrong encoding type
- `ConnectionError` — can't reach the API
- `TimeoutError` — API took too long to respond

**Quirks →**

Don't catch everything blindly:

- bare `except` — hides all errors and catches keyboard interrupts making the program unkillable
- `except Exception` — catches all errors but with no details
- always catch specific errors and log the error type and message

Bare `except` hides bugs — in an AI system a hidden error means something went wrong with no traceback of why or where.

**In AI systems →** Always write defensive code. Catch everything that could go wrong, log what happened, and continue processing the rest.

---

## Subtopic 10 — String Manipulation

**What it is →** Cleaning, formatting, splitting, and transforming text. Every document in an AI system is a string. Quality of cleaning determines quality of LLM answers.

**How it works →** A string is an immutable sequence of characters. Every operation produces a new string in memory. Reassigning is important — the original never changes.

**Syntax:**

```python
text = "  hello world  \n"
text = text.strip()                   # remove both sides whitespace
text = text.lstrip()                  # left side only
text = text.rstrip()                  # right side only

text.split()                          # split on whitespace — smart
text.split(",")                       # split on comma
text.split("\n")                      # split on newline
len(text.split())                     # word count

text = text.replace("\n\n", " ")      # replace
text = text.replace("  ", " ")

" ".join(["hello", "world"])          # list to string
"\n\n".join(chunks)                   # join with separator

query = query.lower()                 # lowercase
query = query.upper()                 # uppercase

message = f"Model: {model}, Cost: ${cost:.4f}"    # f-string

system_prompt = """You are a helpful assistant.
Answer based only on the provided context."""      # multi-line string

text = raw.strip().lower().replace("\n", " ")      # chaining
```

**Quirks →**

`split()` vs `split(" ")` — `split()` treats any amount of whitespace as one separator and removes empty strings. `split(" ")` splits on every single space so multiple spaces produce empty strings.

`strip()` — only removes leading and trailing whitespace, not middle spaces.

**In AI systems →** Every document must go through string cleaning before entering the pipeline. Use f-strings and `.join()` to build prompts. Quality of string cleaning directly determines quality of LLM answers.

---

## Extra Knowledge — Quick Reference

**How a Python Project Works Behind the Scene →** Install Python (installs the interpreter) → create a folder → run `python -m venv venv` to create an isolated Python copy so projects don't conflict → write `.py` files → run with `python filename.py` → interpreter reads text, parser breaks into tokens, compiler converts to bytecode (stored in `__pycache__/`), PVM executes bytecode line by line → install libraries with `pip install` which downloads from PyPI into virtual environment `/lib` folder → track libraries with `pip freeze > requirements.txt`.

**How Variables Work Behind the Scene →** Write `name = "Aminah"` → Python creates string in memory with type tag and reference count → creates label in namespace pointing to that location → reassignment creates new value and re-points the label → old value with zero references gets garbage collected → multiple labels can point to same value (`b = a` does not copy) → with mutable types, changing through one label affects all labels pointing to that value → with immutable types this never happens because operations create new values.

**How Python Calls C/C++ →** Write `np.sum(a)` → NumPy receives the call → does NOT run addition in Python → passes data to a pre-compiled C function → C function runs at C speed → result comes back to Python. Python is the instruction layer. Heavy work runs in compiled C underneath. That's why Python being "slow" doesn't matter.
