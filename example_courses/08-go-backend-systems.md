@start name
Go for Backend Systems
@end name

@start description
Mastering the Go programming language (Golang) for building high-performance backend services.
@end description

@start module
@start title
Go Syntax and Type System
@end title

@start description
Introduction to Go's unique approach to typing, structs, and interfaces.
@end description

@start content
# Getting Started with Go

Go is designed for simplicity and efficiency, making it ideal for cloud services and backend infrastructure.

## Statically Typed and Compiled
Go is statically typed, meaning types are checked at compile time. This leads to safer and faster code.

## Structs: The Basis of Data
Go does not have traditional classes. Instead, it uses **structs** to group data.

```go
type User struct {
    ID    int
    Name  string
    Email string
}

func main() {
    user := User{ID: 1, Name: "Alice", Email: "alice@example.com"}
    fmt.Println(user.Name)
}
```

## Methods and Receivers
You can add behavior to structs by defining methods with a **receiver**.

```go
func (u User) Greet() string {
    return "Hello, " + u.Name
}
```

## Interfaces: Decoupling Logic
Interfaces define a set of method signatures. Any type that implements those methods satisfies the interface.

```go
type Greeter interface {
    Greet() string
}
```
@end content

@start quiz
@start title
Syntax and Types Quiz
@end title

@start description
Verify your understanding of Go's type system.
@end description

@start question
@start text
Does Go use traditional classes for object-oriented programming?
@end text
@start answer
@start text
Yes, it uses class and extends keywords.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
No, it uses structs and methods to achieve similar results.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is a 'receiver' in Go?
@end text
@start answer
@start text
A function that receives a network packet.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
The argument that binds a function to a specific struct, making it a method.
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
Error Handling and Defer
@end title

@start description
Learning Go's explicit error handling philosophy and resource management.
@end description

@start content
# Robustness in Go

Go takes a different approach to error handling than most languages—it avoids exceptions.

## Explicit Error Returns
In Go, errors are values. Functions that can fail return the result and an `error` type as the last return value.

```go
func Divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

res, err := Divide(10, 0)
if err != nil {
    log.Println(err)
}
```

## The `defer` Keyword
`defer` schedules a function call to run immediately before the surrounding function returns. This is perfect for closing files or network connections.

```go
func readFiles() {
    f, _ := os.Open("test.txt")
    defer f.Close() // Runs at the end of readFiles()

    // do something with f
}
```

## Panic and Recover
`panic` is used for unrecoverable errors. `recover` can be used inside a deferred function to stop a panic and regain control.
@end content

@start quiz
@start title
Error Handling Quiz
@end title

@start description
Test your knowledge of Go's error and resource management.
@end description

@start question
@start text
How does Go typically handle errors compared to languages like Java or Python?
@end text
@start answer
@start text
It uses try-catch blocks for all errors.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
It returns errors as explicit values that must be checked.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is the purpose of the `defer` keyword?
@end text
@start answer
@start text
To pause the execution of the program.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To ensure a function call happens right before the surrounding function returns.
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
Building REST APIs with Go
@end title

@start description
Creating a production-ready API using the standard library and popular routers.
@end description

@start content
# Developing Web Services

Go's standard library `net/http` is powerful enough to build full APIs, though routers like `Gorilla Mux` or `Gin` are common.

## The `http.Handler`
Everything in Go's web server is a `Handler`. A handler is essentially a function that takes a `ResponseWriter` and a `Request`.

```go
func homeHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Welcome to the Go API!")
}

func main() {
    http.HandleFunc("/", homeHandler)
    http.ListenAndServe(":8080", nil)
}
```

## JSON Encoding and Decoding
Since most APIs use JSON, Go's `encoding/json` package is essential.

```go
type Response struct {
    Message string `json:"message"`
}

func jsonHandler(w http.ResponseWriter, r *http.Request) {
    res := Response{Message: "Hello World"}
    json.NewEncoder(w).Encode(res)
}
```

## Middleware Concepts
Middleware are functions that wrap handlers to provide functionality like logging, authentication, or CORS.
@end content

@start quiz
@start title
REST API Quiz
@end title

@start description
Verify your ability to create web services in Go.
@end description

@start question
@start text
Which package in the standard library is used for creating basic web servers?
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
`web/server`
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What is the purpose of using struct tags like `` `json:"message"` ``?
@end text
@start answer
@start text
To tell Go how to map the struct field to a JSON key during encoding/decoding.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
To make the code compile faster.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
