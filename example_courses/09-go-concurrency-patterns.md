@start name
Go Concurrency Patterns
@end name

@start description
Mastering Go's concurrency primitives: Goroutines, Channels, and the Select statement.
@end description

@start module
@start title
Goroutines and the Scheduler
@end title

@start description
Understanding how Go achieves lightweight concurrency.
@end description

@start content
# Concurrency in Go

Go is famous for its efficient concurrency model, based on Communicating Sequential Processes (CSP).

## What is a Goroutine?
A goroutine is a lightweight thread managed by the Go runtime. They are much cheaper than OS threads, allowing you to spawn thousands of them.

```go
func sayHello() {
    fmt.Println("Hello from goroutine!")
}

func main() {
    go sayHello() // This starts a goroutine
    time.Sleep(time.Second) // Wait for it to finish
}
```

## The Go Scheduler
The Go runtime uses a "M:N" scheduler, mapping M goroutines to N OS threads. This allows the runtime to handle blocking calls (like I/O) without freezing the whole program.

## Avoiding Race Conditions
When multiple goroutines access the same variable, you get a **Race Condition**. To prevent this, use:
- **Channels**: To communicate and share data.
- **Mutexes**: To lock a piece of data for one goroutine at a time.
@end content

@start quiz
@start title
Goroutines Quiz
@end title

@start description
Verify your understanding of lightweight threads in Go.
@end description

@start question
@start text
How do you start a goroutine in Go?
@end text
@start answer
@start text
By using the `go` keyword before a function call.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
By using the `thread.start()` method.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What is a race condition in Go?
@end text
@start answer
@start text
When a program runs too fast for the CPU to handle.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
When multiple goroutines access the same data simultaneously, leading to unpredictable results.
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
Channels: Communication and Synchronization
@end title

@start description
Using channels to send and receive data between goroutines safely.
@end description

@start content
# Channels in Go

"Do not communicate by sharing memory; instead, share memory by communicating."

## Creating and Using Channels
Channels are pipes that connect goroutines. You create them using `make(chan T)`.

```go
ch := make(chan string)

go func() {
    ch <- "Ping!" // Send data into channel
}()

msg := <-ch // Receive data from channel
fmt.Println(msg)
```

## Unbuffered vs Buffered Channels
- **Unbuffered**: Blocks the sender until the receiver is ready. This provides strong synchronization.
- **Buffered**: Has a capacity. The sender only blocks when the buffer is full.

```go
ch := make(chan int, 2) // Buffered channel with size 2
ch <- 1
ch <- 2 // Does not block yet
```

## Closing Channels
The sender can close a channel using `close(ch)`. Receivers can detect if a channel is closed using a comma-ok idiom: `val, ok := <-ch`.
@end content

@start quiz
@start title
Channels Quiz
@end title

@start description
Check your knowledge of channel-based communication.
@end description

@start question
@start text
What is the difference between a buffered and an unbuffered channel?
@end text
@start answer
@start text
Buffered channels can hold a limited number of values without blocking the sender.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Unbuffered channels are faster than buffered channels.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
How can a receiver tell if a channel has been closed?
@end text
@start answer
@start text
The program will crash automatically.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
By using the comma-ok idiom: `val, ok := <-ch`.
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
The Select Statement and Worker Pools
@end title

@start description
Multiplexing channel operations and building efficient concurrent processing systems.
@end description

@start content
# Advanced Concurrency Patterns

## The `select` Statement
The `select` statement lets a goroutine wait on multiple communication operations. It blocks until one of its cases can run.

```go
select {
case msg1 := <-ch1:
    fmt.Println("Received from ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("Received from ch2:", msg2)
case <-time.After(time.Second):
    fmt.Println("Timeout occurred")
}
```

## Implementing a Worker Pool
A worker pool limits the number of goroutines running at once, preventing system exhaustion.

1. Create a `jobs` channel and a `results` channel.
2. Spawn a fixed number of worker goroutines.
3. Feed jobs into the channel and collect results.

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}
```

## WaitGroups
The `sync.WaitGroup` is used to wait for a collection of goroutines to finish before continuing the main execution.
@end content

@start quiz
@start title
Select and Worker Pools Quiz
@end title

@start description
Verify your ability to implement advanced concurrency patterns.
@end description

@start question
@start text
What is the primary purpose of the `select` statement?
@end text
@start answer
@start text
To pick a random number.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To wait on multiple channel operations simultaneously.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Why would you use a Worker Pool instead of spawning a new goroutine for every single task?
@end text
@start answer
@start text
To avoid overwhelming the system's resources by limiting the number of concurrent tasks.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Because worker pools are slower and therefore safer.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
