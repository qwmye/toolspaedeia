@start name
C++ Object-Oriented Programming
@end name

@start description
Transition from C to C++ by mastering classes, encapsulation, and the concept of RAII. Learn how to build complex systems with strong type safety.
@end description

@start module
@start title
Classes and Encapsulation
@end title

@start description
Introduction to C++ classes, access modifiers, and the concept of data hiding.
@end description

@start content
## Classes in C++

C++ introduces classes, which combine data (attributes) and behavior (methods).

```cpp
class Course {
private:
    std::string title;
    double price;

public:
    Course(std::string t, double p) : title(t), price(p) {}

    std::string getTitle() { return title; }
};
```

## Access Modifiers

- `public`: Accessible from anywhere.
- `private`: Accessible only within the class.
- `protected`: Accessible within the class and its derived classes.

This encapsulation ensures that internal state cannot be corrupted by external code.
@end content

@start quiz
@start title
Quiz: Encapsulation
@end title

@start description
Verify your understanding of C++ class structure.
@end description

@start question
@start text
Which access modifier prevents a variable from being accessed outside of the class?
@end text

@start answer
@start text
public
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
private
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
protected
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
Polymorphism and Virtual Functions
@end title

@start description
Learn how to use abstract base classes and virtual functions to implement runtime polymorphism.
@end description

@start content
## Virtual Functions

A `virtual` function in a base class can be overridden by a derived class. This allows a pointer to a base class to call the version of the function that corresponds to the actual object type.

```cpp
class Shape {
public:
    virtual void draw() { std::cout << "Drawing shape"; }
};

class Circle : public Shape {
public:
    void draw() override { std::cout << "Drawing circle"; }
};
```

## Pure Virtual Functions

A function is "pure virtual" if it is declared as `= 0`. This makes the class **abstract**, meaning you cannot instantiate it. All derived classes must implement this function.
@end content

@start quiz
@start title
Quiz: Polymorphism
@end title

@start description
Check your knowledge of virtual functions.
@end description

@start question
@start text
What is the effect of declaring a function as a pure virtual function (`= 0`)?
@end text

@start answer
@start text
The function can never be called.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
The class becomes abstract and cannot be instantiated.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
The function is automatically optimized by the compiler.
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
RAII and Smart Pointers
@end title

@start description
Eliminate memory leaks using Resource Acquisition Is Initialization (RAII) and smart pointers.
@end description

@start content
## RAII Concept

RAII ensures that resources are acquired during object construction and released during destruction. This prevents memory leaks in the event of exceptions.

## Smart Pointers

Modern C++ avoids manual `new` and `delete` in favor of:
- `std::unique_ptr`: Sole ownership of a resource.
- `std::shared_ptr`: Shared ownership using reference counting.
- `std::weak_ptr`: A non-owning reference to an object managed by a `shared_ptr`.

```cpp
#include <memory>
std::unique_ptr<Course> myCourse = std::make_unique<Course>("Modern C++", 29.99);
// Memory is freed automatically when myCourse goes out of scope.
```
@end content

@start quiz
@start title
Quiz: Memory Management
@end title

@start description
Verify your understanding of smart pointers.
@end description

@start question
@start text
Which smart pointer should be used when only one object is allowed to own the resource?
@end text

@start answer
@start text
std::shared_ptr
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
std::unique_ptr
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
std::weak_ptr
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
