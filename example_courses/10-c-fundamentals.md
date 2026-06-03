@start name
C Fundamentals
@end name

@start description
Master the basics of the C programming language, the foundation of modern computing. Learn about types, control flow, and the concept of the memory model.
@end description

@start module
@start title
The C Environment and Syntax
@end title

@start description
Introduction to the C compiler, basic data types, and operator precedence.
@end description

@start content
## The Compilation Process

C is a compiled language. The source code (`.c`) goes through a preprocessor, a compiler, and a linker to produce an executable file.

## Data Types and Variables

C provides a set of fundamental types:
- `int`: Integers.
- `char`: Single characters.
- `float` / `double`: Floating-point numbers.

Unlike Python, C is statically typed, meaning the type of a variable must be known at compile time.

```c
int age = 21;
float price = 19.99;
char grade = 'A';
```
@end content

@start quiz
@start title
Quiz: C Syntax
@end title

@start description
Verify your understanding of C basics.
@end description

@start question
@start text
Which of the following is true about C?
@end text

@start answer
@start text
It is an interpreted language.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It is a statically typed, compiled language.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It does not use a linker.
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
Control Flow and Functions
@end title

@start description
Implement logic using conditionals, loops, and modular functions.
@end description

@start content
## Conditional Branching

C uses `if`, `else if`, and `else` similarly to other C-family languages.

## Loops

- `for` loops: Best for iterating a fixed number of times.
- `while` loops: Best for iterating until a condition is met.
- `do-while` loops: Ensures the block is executed at least once.

## Function Definitions

Functions in C must specify the return type.

```c
int add(int a, int b) {
    return a + b;
}
```
@end content

@start quiz
@start title
Quiz: Control Flow
@end title

@start description
Test your logic implementation skills.
@end description

@start question
@start text
Which loop is guaranteed to execute at least once?
@end text

@start answer
@start text
for
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
do-while
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
Arrays and Strings
@end title

@start description
Store collections of data and handle text using the C-style string approach.
@end description

@start content
## Arrays

An array is a contiguous block of memory containing elements of the same type.

```c
int numbers[5] = {10, 20, 30, 40, 50};
printf("%d", numbers[0]); // 10
```

## Strings in C

C does not have a built-in `string` type. Strings are represented as arrays of `char` ending with a null terminator (`\0`).

```c
char greeting[] = "Hello"; // Automatically adds \0 at the end
```
@end content

@start quiz
@start title
Quiz: Arrays and Strings
@end title

@start description
Verify your understanding of memory layouts for arrays and strings.
@end description

@start question
@start text
What marks the end of a string in C?
@end text

@start answer
@start text
A newline character `\n`
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
A null terminator `\0`
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
A semi-colon `;`
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
