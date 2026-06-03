@start name
Python Intermediate: OOP & Modules
@end name

@start description
Moving beyond basic syntax to master Object-Oriented Programming and modular architecture in Python.
@end description

@start module
@start title
Classes and Objects
@end title

@start description
Understanding the fundamentals of OOP: attributes, methods, and instance creation.
@end description

@start content
# Object-Oriented Programming (OOP) Basics

OOP is a paradigm based on the concept of "objects", which can contain data (attributes) and code (methods).

## Defining a Class
A class is a blueprint for creating objects.

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name  # Attribute
        self.breed = breed # Attribute

    def bark(self):       # Method
        return f"{self.name} says Woof!"

my_dog = Dog("Buddy", "Golden Retriever")
print(my_dog.bark())
```

## The `__init__` Method
The `__init__` method is the constructor. It initializes the object's state when it is created.

## The `self` Parameter
`self` represents the instance of the object itself, allowing methods to access attributes and other methods of the same object.
@end content

@start quiz
@start title
Classes and Objects Quiz
@end title

@start description
Check your understanding of classes and instances.
@end description

@start question
@start text
What is the purpose of the `__init__` method in a Python class?
@end text
@start answer
@start text
To define the main entry point of the program.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To initialize the object's attributes when the object is created.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What does the `self` parameter represent in a class method?
@end text
@start answer
@start text
The class definition itself.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
The specific instance of the object being operated on.
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
Inheritance and Polymorphism
@end title

@start description
Leveraging class hierarchies to reuse code and implement flexible interfaces.
@end description

@start content
# Advanced OOP Concepts

## Inheritance
Inheritance allows a class (child) to derive attributes and methods from another class (parent).

```python
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Cat(Animal):
    def speak(self):
        print("Meow")

my_cat = Cat()
my_cat.speak() # Outputs: Meow
```

## Polymorphism
Polymorphism allows different classes to be treated as instances of the same general class through a common interface.

## Method Overriding
When a child class provides a specific implementation of a method that is already provided by its parent class, it is called overriding.

## Super() Function
The `super()` function allows you to call methods from the parent class, which is especially useful in `__init__` to avoid duplicating initialization logic.
@end content

@start quiz
@start title
Inheritance and Polymorphism Quiz
@end title

@start description
Verify your knowledge of class hierarchies.
@end description

@start question
@start text
What is 'method overriding'?
@end text
@start answer
@start text
Deleting a method from a parent class.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
Providing a specific implementation in a child class for a method already defined in the parent class.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Which function is used to call a method from the parent class?
@end text
@start answer
@start text
`super()`
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
`parent()`
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
Modules and Packages
@end title

@start description
Organizing code into reusable files and directories for better maintainability.
@end description

@start content
# Code Organization

As projects grow, keeping all code in one file becomes unmanageable. Python uses modules and packages to structure code.

## Modules
A module is simply a file containing Python definitions and statements. To use a module in another file, use the `import` statement.

```python
# my_math.py
def add(a, b):
    return a + b

# main.py
import my_math
print(my_math.add(5, 10))
```

## Packages
A package is a directory containing a special `__init__.py` file and one or more modules.

## Absolute vs Relative Imports
- **Absolute**: `import my_project.utils.helpers`
- **Relative**: `from .utils import helpers` (used within the same package).

## The `__name__ == "__main__"` Block
This block ensures that certain code only runs when the script is executed directly, not when it is imported as a module.
@end content

@start quiz
@start title
Modules and Packages Quiz
@end title

@start description
Test your ability to organize Python code.
@end description

@start question
@start text
What is a Python 'package'?
@end text
@start answer
@start text
A single `.py` file.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
A directory containing modules and an `__init__.py` file.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Why use `if __name__ == "__main__":`?
@end text
@start answer
@start text
To prevent code from executing when the file is imported as a module.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
To speed up the execution of the code.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
