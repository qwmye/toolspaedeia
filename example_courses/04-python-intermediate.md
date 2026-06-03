@start name
Python Intermediate: OOP and Modules
@end name

@start description
Advance your Python skills by mastering Object-Oriented Programming (OOP), decorators, and effective module organization.
@end description

@start module
@start title
Object-Oriented Programming Basics
@end title

@start description
Learn how to organize code using classes and objects to model real-world entities.
@end description

@start content
## Classes and Objects

A class is a blueprint for creating objects. An object is an instance of a class.

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def get_info(self):
        return f"Course: {self.title}, Price: {self.price}"

my_course = Course("Python OOP", 49.99)
print(my_course.get_info())
```

## The `self` Keyword

`self` represents the instance of the class. It allows the method to access attributes and other methods of the same object.
@end content

@start quiz
@start title
Quiz: OOP Basics
@end title

@start description
Verify your understanding of classes and objects.
@end description

@start question
@start text
What is the purpose of the `__init__` method in a Python class?
@end text

@start answer
@start text
To define a private method.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
To initialize an object's attributes when it is created.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
To delete an object from memory.
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
Inheritance and Polymorphism
@end title

@start description
Reduce code redundancy by inheriting attributes and behaviors from parent classes.
@end description

@start content
## Inheritance

Inheritance allows a class (child) to derive attributes and methods from another class (parent).

```python
class User:
    def login(self):
        print("User logged in")

class Publisher(User):
    def publish(self):
        print("Course published!")

pub = Publisher()
pub.login()   # Inherited from User
pub.publish() # Specific to Publisher
```

## Polymorphism

Polymorphism allows different classes to be treated as instances of the same general class through a shared interface.
@end content

@start quiz
@start title
Quiz: Inheritance
@end title

@start description
Test your knowledge of class hierarchies.
@end description

@start question
@start text
In the example above, what is the relationship between User and Publisher?
@end text

@start answer
@start text
Publisher is the parent class.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Publisher is the child class.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
They are unrelated classes.
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
Decorators and Generators
@end title

@start description
Master advanced Python features for modifying function behavior and handling large data streams efficiently.
@end description

@start content
## Decorators

A decorator is a function that takes another function and extends its behavior without explicitly modifying it.

```python
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@debug
def add(a, b):
    return a + b
```

## Generators

Generators use the `yield` keyword to produce a sequence of values lazily, which is memory efficient for large datasets.

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)
```
@end content

@start quiz
@start title
Quiz: Advanced Features
@end title

@start description
Check your understanding of decorators and generators.
@end description

@start question
@start text
What is the main advantage of using a generator over a list?
@end text

@start answer
@start text
Generators are faster to access by index.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Generators use less memory as they produce values one at a time.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Generators can be modified after creation.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
