@start name
C Memory Management & Pointers
@end name

@start description
Mastering the most challenging aspect of C: pointers, memory allocation, and avoiding leaks.
@end description

@start module
@start title
Understanding Pointers
@end title

@start description
What pointers are, how they work, and why they are powerful.
@end description

@start content
# Pointers in C

A pointer is a variable that stores the memory address of another variable.

## The Address-of and Dereference Operators
- `&` (Address-of): Returns the memory address of a variable.
- `*` (Dereference): Accesses the value at the address stored in the pointer.

```c
int x = 10;
int *ptr = &x; // ptr stores the address of x

printf("%p", ptr); // Print the memory address
printf("%d", *ptr); // Print the value at that address (10)
```

## Pointer Arithmetic
Since arrays are stored contiguously, you can navigate them using pointer arithmetic.
`ptr + 1` moves the pointer to the next element of its type.

## The Void Pointer
`void *` is a generic pointer. It can point to any data type, but it must be cast back to a specific type before dereferencing.
@end content

@start quiz
@start title
Pointers Quiz
@end title

@start description
Verify your understanding of memory addresses and dereferencing.
@end description

@start question
@start text
What does the `*` operator do when used with a pointer variable?
@end text
@start answer
@start text
It finds the memory address of the variable.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
It dereferences the pointer to access the value at that address.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is a `void` pointer?
@end text
@start answer
@start text
A pointer that is not allowed to point to any data.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
A generic pointer that can point to any data type.
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
Dynamic Memory Allocation
@end title

@start description
Using `malloc`, `calloc`, `realloc`, and `free` to manage memory at runtime.
@end description

@start content
# Heap vs Stack

- **Stack**: Managed automatically. Fast, but limited size.
- **Heap**: Managed manually by the programmer. Large, but requires care.

## Memory Allocation Functions
These functions are found in `<stdlib.h>`.

- `malloc(size)`: Allocates a block of memory. Returns a `void *`.
- `calloc(num, size)`: Allocates memory for an array and initializes all bits to zero.
- `realloc(ptr, size)`: Changes the size of a previously allocated block.

```c
int *arr = (int *)malloc(5 * sizeof(int));
if (arr == NULL) {
    printf("Memory allocation failed!");
}
```

## Memory Deallocation
Every `malloc` must have a corresponding `free()`. Failure to do so results in a **Memory Leak**.

```c
free(arr);
```
@end content

@start quiz
@start title
Dynamic Memory Quiz
@end title

@start description
Test your knowledge of heap management.
@end description

@start question
@start text
Which function should be used to release memory allocated on the heap?
@end text
@start answer
@start text
`delete()`
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`free()`
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is the main difference between `malloc` and `calloc`?
@end text
@start answer
@start text
`calloc` initializes the allocated memory to zero, while `malloc` does not.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
`malloc` is only for arrays, while `calloc` is for single variables.
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
Common Pitfalls: Dangling Pointers and Buffer Overflows
@end title

@start description
Learning how to identify and prevent critical memory bugs.
@end description

@start content
# Memory Safety in C

C gives you total control, but that means you are responsible for safety.

## Dangling Pointers
A dangling pointer occurs when a pointer still points to a memory location that has already been freed.
**Fix**: Set the pointer to `NULL` immediately after calling `free()`.

## Buffer Overflows
A buffer overflow happens when a program writes more data to a buffer than it can hold, overwriting adjacent memory.

```c
char buffer[10];
strcpy(buffer, "This string is way too long for the buffer!"); // CRASH/VULNERABILITY
```
**Fix**: Use safer functions like `strncpy()` or `fgets()`.

## Segmentation Faults (Segfaults)
A segfault occurs when your program tries to access memory it doesn't own (e.g., dereferencing a `NULL` pointer).
@end content

@start quiz
@start title
Memory Pitfalls Quiz
@end title

@start description
Verify your ability to spot memory errors.
@end description

@start question
@start text
What is a 'dangling pointer'?
@end text
@start answer
@start text
A pointer that has not yet been assigned a value.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
A pointer that points to a memory location that has already been freed.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Which of these is a common cause of a Segmentation Fault?
@end text
@start answer
@start text
Dereferencing a NULL pointer.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Using a `for` loop that runs too many times.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
