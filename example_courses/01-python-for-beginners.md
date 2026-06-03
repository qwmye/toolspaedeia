@start name
Python for Beginners
@end name

@start description
A practical beginner course focused on writing real Python code. You will learn syntax, control flow, functions, data structures, and how to handle common programming tasks in Python.
@end description

@start module
@start title
Variables, Types, and Input
@end title

@start description
Learn how Python stores data and how to read user input.
@end description

@start content
## Variables and Types

Python variables are created when assigned. Unlike statically typed languages, you do not need to declare the type of a variable in advance.

Examples:
- name = "Ana"
- age = 21
- price = 19.99
- is_active = True

Python has several built-in types: `str` for text, `int` for whole numbers, `float` for decimals, and `bool` for True/False.

## User Input

Use `input()` to read text from the user. The result is always a string, so you must convert it when working with numbers.

```python
age_text = input("Enter your age: ")
age = int(age_text)
print("Next year you will be", age + 1)
```

You can convert values using `int()`, `float()`, or `str()`. Boolean conversion uses `bool()`, where any non-empty string or non-zero number is `True`.
@end content

@start quiz
@start title
Quiz: Variables and Types
@end title

@start description
Check your understanding of basic data types and input conversion.
@end description

@start question
@start text
Which of the following is an integer value?
@end text

@start answer
@start text
42
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
"42"
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
3.14
@end text

@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What does input() return by default?
@end text

@start answer
@start text
An int
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
A string
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
A float
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module

@start module
@start title
Conditionals and Loops
@end title

@start description
Control program flow using if statements and loops.
@end description

@start content
## Conditionals

Use `if` / `elif` / `else` to branch logic based on conditions. Python uses indentation (typically 4 spaces) to define blocks.

```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

## Loops

Use `for` loops to iterate over collections and `range()`. Use `while` loops when repeating until a condition changes.

```python
for i in range(3):
    print(i)

count = 0
while count < 3:
    print(count)
    count += 1
```

`break` exits the loop early; `continue` skips the rest of the current iteration.
@end content

@start quiz
@start title
Quiz: Conditionals and Loops
@end title

@start description
Verify control flow fundamentals.
@end description

@start question
@start text
Which keyword is used for an alternative condition in an if chain?
@end text

@start answer
@start text
elseif
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
elif
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
altif
@end text

@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
Which loop is best when you know exactly how many times to iterate?
@end text

@start answer
@start text
for
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
while
@end text

@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What does the break statement do inside a loop?
@end text

@start answer
@start text
Skips the rest of the current iteration
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Exits the loop entirely
@end text

@start is_correct
true
@end is_correct
@end answer
@end question
@end quiz
@end module

@start module
@start title
Functions and Reuse
@end title

@start description
Write reusable logic with function definitions and return values.
@end description

@start content
## Defining Functions

Use `def` to define a function. Functions can accept parameters and return values.

```python
def greet(name):
    return "Hello " + name

print(greet("Ana"))
```

## Return Values

Functions can return computed results for reuse. If no return is specified, the function returns `None`.

```python
def add(a, b):
    return a + b

result = add(3, 5)  # result is 8
```

## Default Parameters

You can assign default values to parameters:

```python
def power(base, exponent=2):
    return base ** exponent

print(power(3))     # 9
print(power(2, 3))  # 8
```
@end content

@start quiz
@start title
Quiz: Functions
@end title

@start description
Test your understanding of function definitions and returns.
@end description

@start question
@start text
Which keyword defines a function in Python?
@end text

@start answer
@start text
func
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
def
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
function
@end text

@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What does return do inside a function?
@end text

@start answer
@start text
Stops the function and sends a value back
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Prints text to the console
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module

@start module
@start title
Lists, Dictionaries, and Tuples
@end title

@start description
Work with Python's core data structures for storing collections of data.
@end description

@start content
## Lists

Lists are ordered, mutable collections. They are defined with square brackets.

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(fruits[0])  # apple
```

## Dictionaries

Dictionaries store key-value pairs and provide fast lookup.

```python
user = {"name": "Ana", "age": 21}
print(user["name"])
user["city"] = "Bucharest"
```

## Tuples

Tuples are ordered, immutable collections. They are defined with parentheses and cannot be changed after creation.

```python
point = (10, 20)
x, y = point
```
@end content

@start quiz
@start title
Quiz: Data Structures
@end title

@start description
Verify your understanding of Python's core data structures.
@end description

@start question
@start text
Which data structure uses key-value pairs?
@end text

@start answer
@start text
List
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Dictionary
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Tuple
@end text

@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
Can a tuple be modified after creation?
@end text

@start answer
@start text
Yes
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
No
@end text

@start is_correct
true
@end is_correct
@end answer
@end question
@end quiz
@end module

@start module
@start title
File Handling and Modules
@end title

@start description
Read and write files and organize code into reusable modules.
@end description

@start content
## Reading and Writing Files

Use the `open()` function to read or write files. Always close the file when done, or use a `with` statement.

```python
with open("notes.txt", "w") as f:
    f.write("Hello, world!")

with open("notes.txt", "r") as f:
    content = f.read()
    print(content)
```

## Modules and Imports

A module is a file containing Python code. Use `import` to use code from another module.

```python
import math
print(math.sqrt(16))  # 4.0
```

You can also import specific functions: `from math import sqrt`.
@end content

@start quiz
@start title
Quiz: Files and Modules
@end title

@start description
Test your knowledge of file operations and module imports.
@end description

@start question
@start text
Which statement is recommended for safely handling files in Python?
@end text

@start answer
@start text
open() without closing
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
with open() as f:
@end text

@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Which keyword is used to bring external code into the current file?
@end text

@start answer
@start text
include
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
import
@end text

@start is_correct
true
@end is_correct
@end answer
@end question
@end quiz
@end module
