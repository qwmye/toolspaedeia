@start name
C Memory Management and Pointers
@end name

@start description
Dive deep into how C handles memory. Learn about pointers, the stack, the heap, and how to avoid the most common memory-related bugs.
@end description

@start module
@start title
Introduction to Pointers
@end title

@start description
Understand what a pointer is and how to use it to access memory addresses.
@end description

@start content
## What is a Pointer?

A pointer is a variable that stores the memory address of another variable. This is a core feature of C that allows for efficient data handling and dynamic memory.

```c
int x = 10;
int *ptr = &x; // ptr now holds the address of x

printf("Address: %p", ptr);
printf("Value: %d", *ptr); // Dereferencing: access value at address
```

## Pointer Arithmetic

Pointers can be incremented or decremented. When you add 1 to an `int` pointer, it moves forward by the size of one integer (usually 4 bytes).
@end content

@start quiz
@start title
Quiz: Pointer Basics
@end title

@start description
Verify your understanding of pointers and dereferencing.
@end description

@start question
@start text
What does the `*` operator do when used with a pointer variable (outside of a declaration)?
@end text

@start answer
@start text
It returns the memory address.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It dereferences the pointer to get the value stored at that address.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It declares a new pointer variable.
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
Stack vs Heap
@end title

@start description
Compare automatic memory (stack) and dynamic memory (heap) allocation.
@end description

@start content
## The Stack

The stack is used for static memory allocation. It stores local variables and function call frames. It is managed automatically by the CPU.

## The Heap

The heap is used for dynamic memory allocation. It allows you to allocate memory of any size during runtime, but you must manage it manually.

```c
int *arr = (int *)malloc(5 * sizeof(int)); // Allocate space for 5 ints on the heap
```
@end content

@start quiz
@start title
Quiz: Memory Areas
@end title

@start description
Verify the difference between stack and heap.
@end description

@start question
@start text
Which memory area must be manually freed by the programmer using `free()`?
@end text

@start answer
@start text
The Stack
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
The Heap
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
The Data Segment
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
Dynamic Memory and Common Pitfalls
@end title

@start description
Learn how to allocate memory and avoid critical errors like memory leaks and segmentation faults.
@end description

@start content
## Manual Memory Management

Using `malloc`, `calloc`, `realloc`, and `free`.

```c
int *ptr = malloc(sizeof(int));
*ptr = 100;
free(ptr); // Prevent memory leaks
ptr = NULL; // Prevent dangling pointers
```

## Common Bugs

- **Memory Leak:** Forgetting to call `free()` on heap-allocated memory.
- **Dangling Pointer:** Using a pointer after the memory it points to has been freed.
- **Segmentation Fault:** Attempting to access a memory address that your program doesn't own.
@end content

@start quiz
@start title
Quiz: Memory Bugs
@end title

@start description
Check your knowledge of C memory errors.
@end description

@start question
@start text
What occurs when a program continues to allocate memory on the heap without ever freeing it?
@end text

@start answer
@start text
A Segmentation Fault
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
A Memory Leak
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
A Stack Overflow
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
