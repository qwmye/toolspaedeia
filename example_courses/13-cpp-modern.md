@start name
C++ Modern Features
@end name

@start description
Explore the evolution of C++ from C++11 to C++20. Learn about auto, lambda expressions, move semantics, and the STL's powerful algorithms.
@end description

@start module
@start title
Type Inference and Lambdas
@end title

@start description
Write more concise and flexible code using `auto` and anonymous functions.
@end description

@start content
## The `auto` Keyword

Introduced in C++11, `auto` allows the compiler to deduce the type of a variable from its initializer. This is particularly useful for complex iterator types.

```cpp
auto it = my_map.begin(); // Deduct type instead of std::map<K, V>::iterator
```

## Lambda Expressions

Lambdas are anonymous functions that can capture variables from their surrounding scope.

```cpp
auto add = [](int a, int b) { return a + b; };
std::cout << add(10, 5); // 15
```
@end content

@start quiz
@start title
Quiz: Modern Syntax
@end title

@start description
Verify your understanding of type inference and lambdas.
@end description

@start question
@start text
What is the primary purpose of the `auto` keyword in modern C++?
@end text

@start answer
@start text
It makes the variable a constant.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It lets the compiler automatically deduce the variable's type.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It allows the variable to change its type at runtime.
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
Move Semantics and R-value References
@end title

@start description
Optimize performance by transferring ownership of resources instead of copying them.
@end description

@start content
## L-values vs R-values

- **L-value**: An object that occupies a identifiable location in memory (has an address).
- **R-value**: A temporary value that does not persist beyond the expression that creates it.

## Move Semantics (`std::move`)

Move semantics allow you to "steal" resources from a temporary object, preventing expensive deep copies of large arrays or strings.

```cpp
std::vector<int> v1 = {1, 2, 3};
std::vector<int> v2 = std::move(v1); // v1 is now empty, v2 takes the data
```
@end content

@start quiz
@start title
Quiz: Resource Management
@end title

@start description
Check your knowledge of move semantics.
@end description

@start question
@start text
What is the main benefit of using `std::move`?
@end text

@start answer
@start text
It creates a deep copy of the data.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It transfers ownership of resources, avoiding expensive deep copies.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It deletes the object immediately.
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
The STL and Algorithms
@end title

@start description
Leverage the Standard Template Library to implement complex logic with minimal code.
@end description

@start content
## Container Choice

- `std::vector`: The go-to dynamic array.
- `std::unordered_map`: O(1) lookup hash map.
- `std::set`: Unique sorted elements.

## Generic Algorithms

The `<algorithm>` header provides tools for sorting, searching, and transforming.

```cpp
std::vector<int> v = {4, 1, 3, 2};
std::sort(v.begin(), v.end()); // [1, 2, 3, 4]
bool found = std::binary_search(v.begin(), v.end(), 3);
```
@end content

@start quiz
@start title
Quiz: STL
@end title

@start description
Verify your knowledge of STL containers and algorithms.
@end description

@start question
@start text
Which STL container is best for fast lookups using a key?
@end text

@start answer
@start text
std::vector
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
std::unordered_map
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
std::list
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
