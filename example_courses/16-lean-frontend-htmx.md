@start name
Lean Frontend with HTMX
@end name

@start description
Break away from the complexity of heavy JavaScript frameworks. Learn how to build modern, interactive user interfaces using the power of hypermedia and server-driven logic.
@end description

@start module
@start title
The Hypermedia Approach
@end title

@start description
Understand the core philosophy of HTMX and why it is more efficient than the SPA model.
@end description

@start content
## Beyond JSON and State Management

Modern web apps typically use a "JSON API $\rightarrow$ Client-side State $\rightarrow$ DOM Render" flow. This creates immense complexity in the frontend.

HTMX returns to the original spirit of the web: **Hypermedia**. Instead of JSON, the server sends HTML fragments that are injected directly into the DOM.

## The HATEOAS Principle

HTMX is based on HATEOAS (Hypermedia as the Engine of Application State). The server controls the state of the application by providing the links and HTML needed for the next action, reducing the need for complex client-side routing.
@end content

@start quiz
@start title
Quiz: Hypermedia Basics
@end title

@start description
Verify your understanding of the HTMX philosophy.
@end description

@start question
@start text
In the HTMX model, what is the primary format of the data sent from the server to the client?
@end text

@start answer
@start text
JSON
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
HTML fragments
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
XML
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
Core HTMX Attributes
@end title

@start description
Learn how to trigger requests and update specific parts of the page without a full reload.
@end description

@start content
## Triggering Requests

- `hx-get`: Sends an HTTP GET request to the specified URL.
- `hx-post`: Sends an HTTP POST request.
- `hx-put` / `hx-patch`: Used for updating data.
- `hx-delete`: Used for removing data.

## Targeting the DOM

The `hx-target` attribute specifies which element should be updated with the response.

```html
<button hx-post="/like" hx-target="#like-count">
    Like
</button>
<span id="like-count">10</span>
```

## Swapping Content

`hx-swap` defines how the new content is inserted.
- `innerHTML`: Replaces the inside of the target.
- `outerHTML`: Replaces the target element itself.
- `afterend`: Appends the content after the target.
@end content

@start quiz
@start title
Quiz: HTMX Attributes
@end title

@start description
Test your knowledge of the core HTMX attributes.
@end description

@start question
@start text
Which attribute is used to specify the element that should be updated with the server's response?
@end text

@start answer
@start text
`hx-swap`
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
`hx-target`
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
`hx-get`
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
Advanced Interactions and Infinite Scroll
@end title

@start description
Implement complex UX patterns like lazy loading and infinite scrolling with minimal code.
@end description

@start content
## Triggering on Event

HTMX can trigger requests based on events like `keyup`, `mouseover`, or `intersect`.

## Infinite Scroll Implementation

To create an infinite scroll, we use the `hx-trigger="revealed"` attribute. When the last item in a list becomes visible on the screen, HTMX automatically requests the next page of results.

```html
<div hx-get="/courses?page=2" hx-trigger="revealed" hx đã-target="this" hx-swap="afterend">
    Load more...
</div>
```

## Client-side Validation with `hx-indicator`

Use `hx-indicator` to show a loading spinner or a disabled state while a request is in flight, providing a responsive feel to the user.
@end content

@start quiz
@start title
Quiz: Advanced HTMX
@end title

@start description
Check your understanding of event-driven interactions.
@end description

@start question
@start text
What is the most efficient way to implement an infinite scroll using HTMX?
@end text

@start answer
@start text
By using a JavaScript timer that polls the server every 5 seconds.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
By using `hx-trigger="revealed"` on the last element of the list.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
By reloading the entire page every time the user reaches the bottom.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
