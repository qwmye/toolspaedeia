@start name
Go for Backend Systems
@end name

@start description
Build high-performance, scalable backend services using the Go programming language. Learn about strong typing, efficient compilation, and the standard library for networking.
@end description

@start module
@start title
Introduction to Go Syntax
@end title

@start description
Learn the basics of the Go language: variables, types, and the unique approach to functions.
@end description

@start content
## Go Philosophy

Go was designed by Google for simplicity, efficiency, and scalability. It is a compiled language with a focus on fast build times and a strict type system.

## Variables and Constants

In Go, types are declared after the variable name.

```go
var name string = "Ana"
var age = 21 // Type inference
const Pi = 3.1415
```

## Functions and Multiple Returns

Go allows functions to return multiple values, which is commonly used for error handling.

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}
```
@end content

@start quiz
@start title
Quiz: Go Syntax
@end title

@start description
Check your understanding of Go basics.
@end description

@start question
@start text
Which of the following is a characteristic of the Go programming language?
@end text

@start answer
@start text
It is an interpreted language like Python.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It is a compiled language focused on simplicity and efficiency.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It does not have a strong type system.
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
Structs and Interfaces
@end title

@start description
Organize data using structs and define behavior through interfaces to achieve polymorphism.
@end description

@start content
## Structs

Go does not have traditional classes. Instead, it uses `struct` to define collections of fields.

```go
type User struct {
    ID   int
    Name string
}

func (u User) Greet() string {
    return "Hello, " + u.Name
}
```

## Interfaces

An interface defines a set of method signatures. Any type that implements these methods automatically satisfies the interface.

```go
type Greeter interface {
    Greet() string
}

func SayHello(g Greeter) {
    fmt.Println(g.Greet())
}
```
@end content

@start quiz
@start title
Quiz: Structs and Interfaces
@end title

@start description
Test your knowledge of Go's approach to data and behavior.
@end description

@start question
@start text
How does Go achieve polymorphism without traditional class inheritance?
@end text

@start answer
@start text
Through the use of interfaces.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
By using the `extends` keyword.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Go does not support polymorphism.
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
Standard Library and Networking
@end title

@start description
Build a basic HTTP server using Go's powerful standard library.
@end description

@start content
## The `net/http` Package

Go provides a high-performance HTTP server in its standard library, eliminating the need for external frameworks for simple APIs.

```go
package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Welcome to Toolspaedeia Go Backend!")
}

func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}
```

## JSON Processing

Use the `encoding/json` package to marshal and unmarshal data between Go structs and JSON strings.
@end content

@start quiz
@start title
Quiz: Networking in Go
@end title

@start description
Verify your understanding of Go's networking capabilities.
@end description

@start question
@start text
Which package is used to create an HTTP server in Go?
@end text

@start answer
@start text
`net/http`
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
`webserver`
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
`django-go`
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
