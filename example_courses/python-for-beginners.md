@start name
Python for Beginners
@end name

@start description
A practical beginner course focused on writing real Python code.
You will learn syntax, control flow, and reusable functions.
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

Python variables are created when assigned.

Examples:
- name = "Ana"
- age = 21
- price = 19.99
- is_active = True

## User Input

Use input() to read text from the user.
Convert values using int(), float(), or bool-like checks.
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

Use if / elif / else to branch logic based on conditions.

## Loops

Use for loops to iterate collections and range().
Use while loops when repeating until a condition changes.
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

Use def to define a function:
def greet(name):
    return "Hello " + name

## Return Values

Functions can return computed results for reuse in other parts of the program.
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
