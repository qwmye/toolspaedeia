@start name
C++ Modern Features (C++17/20)
@end name

@start description
Exploring the evolution of C++ from C++11 to C++20: smart pointers, lambdas, and concepts.
@end description

@start module
@start title
Smart Pointers and Memory Management
@end title

@start description
Moving away from `malloc` and `free` to safer, automated memory management.
@end description

@start content
# Modern Memory Management

Manual memory management with `new` and `delete` is error-prone. C++11 introduced Smart Pointers to automate this.

## `std::unique_ptr`
A unique pointer owns an object exclusively. It cannot be copied, only moved. When the `unique_ptr` goes out of scope, the memory is automatically deleted.

```cpp
#include <memory>
auto ptr = std::make_unique<Player>(100);
```

## `std::shared_ptr`
A shared pointer allows multiple pointers to own the same object. It uses **Reference Counting**. When the last shared pointer is destroyed, the memory is freed.

```cpp
auto sharedPtr1 = std::make_shared<Player>(100);
auto sharedPtr2 = sharedPtr1; // Reference count increases
```

## `std::weak_ptr`
Used to break circular references between `shared_ptr`s. It doesn't contribute to the reference count.
@end content

@start quiz
@start title
Smart Pointers Quiz
@end title

@start description
Verify your knowledge of automated memory management.
@end description

@start question
@start text
Which smart pointer should be used when only one owner is allowed for a resource?
@end text
@start answer
@start text
`std::shared_ptr`
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`std::unique_ptr`
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
How does `std::shared_ptr` determine when to delete the managed object?
@end text
@start answer
@start text
It uses a reference counter and deletes the object when the count reaches zero.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
It deletes the object as soon as the first pointer is created.
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
Lambda Expressions and Functional Style
@end title

@start description
Writing anonymous functions for cleaner and more concise code.
@end description

@start content
# Lambdas in C++

Lambdas allow you to define a function inline, which is especially useful for algorithms and callbacks.

## Lambda Syntax
A lambda consists of a capture clause, parameters, and a body.

```cpp
auto add = [](int a, int b) { return a + b; };
cout << add(5, 3); // 8
```

## Capturing Variables
Lambdas can "capture" variables from the surrounding scope:
- `[=]`: Capture all by value.
- `[&]`: Capture all by reference.
- `[x, &y]`: Capture `x` by value and `y` by reference.

## Using Lambdas with STL Algorithms
Lambdas are most powerful when used with `std::sort` or `std::find_if`.

```cpp
std::sort(vec.begin(), vec.end(), [](int a, int b) {
    return a > b; // Sort descending
});
```
@end content

@start quiz
@start title
Lambdas Quiz
@end title

@start description
Test your ability to write anonymous functions.
@end description

@start question
@start text
What does the capture clause `[&]` do in a C++ lambda?
@end text
@start answer
@start text
It captures all local variables by reference.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
It captures all local variables by value.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
Where are lambdas most commonly used in modern C++?
@end text
@start answer
@start text
As arguments for STL algorithms like `std::sort`.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
To replace the `main()` function.
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
C++20 Concepts and Ranges
@end title

@start description
Exploring the latest advancements in template constraints and sequence manipulation.
@end description

@start content
# The C++20 Revolution

C++20 introduces features that make templates safer and data manipulation more intuitive.

## Concepts
Concepts are predicates used to constrain template arguments. Instead of getting a 100-line error message, you get a clear "Constraint not satisfied" error.

```cpp
template <typename T>
concept Numeric = std::is_arithmetic_v<T>;

template <Numeric T>
T add(T a, T b) { return a + b; }
```

## The Ranges Library
The Ranges library allows you to perform operations on sequences without needing to specify `.begin()` and `.end()` every time.

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};
auto result = v | std::views::filter([](int n){ return n % 2 == 0; })
               | std::views::transform([](int n){ return n * n; });
```

## Coroutines
C++20 introduces coroutines, allowing functions to be suspended and resumed, which is essential for high-performance asynchronous I/O.
@end content

@start quiz
@start title
Modern C++ Quiz
@end title

@start description
Verify your understanding of C++20 features.
@end description

@start question
@start text
What is the purpose of 'Concepts' in C++20?
@end text
@start answer
@start text
To replace classes entirely.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To provide constraints on template arguments, improving error messages and type safety.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What does the Ranges library allow developers to do?
@end text
@start answer
@start text
Operate on sequences using a pipe-like syntax without explicit iterators.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Create arrays that can grow in size automatically.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
