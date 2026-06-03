@start name
Go Concurrency Patterns
@end name

@start description
Master Go's most powerful feature: concurrency. Learn about Goroutines, Channels, and the Select statement to build highly parallel systems.
@end description

@start module
@start title
Goroutines and the Scheduler
@end title

@start description
Learn how to launch thousands of lightweight threads and how Go manages them.
@end description

@start content
## What are Goroutines?

A goroutine is a lightweight thread managed by the Go runtime. They are much cheaper than OS threads, allowing a single program to run millions of them simultaneously.

```go
func sayHello() {
    fmt.Println("Hello from a goroutine!")
}

func main() {
    go sayHello() // Launch as a goroutine
    fmt.Println("Main function continues")
    time.Sleep(time.Second)
}
```

## The Go Scheduler

The Go runtime uses an M:N scheduler, mapping M goroutines onto N OS threads. This ensures that if one goroutine blocks (e.g., waiting for I/O), the scheduler can move other goroutines to a different thread to keep the CPU busy.
@end content

@start quiz
@start title
Quiz: Goroutine Basics
@end title

@start description
Verify your understanding of Go's concurrency model.
@end description

@start question
@start text
How do you start a function as a goroutine?
@end text

@start answer
@start text
Using the `thread` keyword.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Adding the `go` keyword before the function call.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Calling `runtime.launch()`.
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
Channels and Communication
@end title

@start description
Coordinate goroutines using channels to avoid race conditions and shared memory bugs.
@end description

@start content
## Channel Basics

Channels are the pipes that connect concurrent goroutines. You can send values into channels and receive them.

```go
ch := make(chan string)

go func() {
    ch <- "Ping!" // Send value
}()

msg := <-ch // Receive value
fmt.Println(msg)
```

## Buffered vs Unbuffered Channels

- **Unbuffered:** Block the sender until the receiver is ready. This provides strong synchronization.
- **Buffered:** Have a capacity. The sender only blocks when the buffer is full.

```go
buffered := make(chan int, 3) // Can hold 3 values before blocking
```
@end content

@start quiz
@start title
Quiz: Channels
@end title

@start description
Test your knowledge of channel communication.
@end description

@start question
@start text
What happens when you try to receive from an empty unbuffered channel?
@end text

@start answer
@start text
The program crashes immediately.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
The goroutine blocks until a value is sent.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It returns a `nil` value.
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
Select and Complex Patterns
@end title

@start description
Implement timeouts, non-blocking communication, and the fan-in/fan-out patterns.
@end description

@start content
## The `select` Statement

`select` lets a goroutine wait on multiple communication operations.

```go
select {
case msg1 := <-ch1:
    fmt.Println("Received from ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("Received from ch2:", msg2)
case <-time.After(time.Second):
    fmt.Println("Timed out!")
}
```

## Common Patterns

- **Fan-out:** Multiple goroutines reading from the same channel to process data in parallel.
- **Fan-in:** Multiplexing multiple channels into a single result channel.
- **Worker Pools:** A fixed number of goroutines processing a queue of tasks.
@end content

@start quiz
@start title
Quiz: Advanced Concurrency
@end title

@start description
Verify your understanding of the `select` statement.
@end description

@start question
@start text
Which statement is used to handle multiple channel operations simultaneously in Go?
@end text

@start answer
@start text
`switch`
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
`select`
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
`wait`
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
