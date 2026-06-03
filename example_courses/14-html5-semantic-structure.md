@start name
HTML5 Semantic Structure
@end name

@start description
Moving beyond `div` and `span` to create meaningful, accessible, and SEO-friendly web pages.
@end description

@start module
@start title
The Importance of Semantic HTML
@end title

@start description
Understanding why semantic tags matter for accessibility and search engines.
@end description

@start content
# Why Semantic HTML?

Semantic HTML refers to using HTML tags that convey the *meaning* of the content they contain, rather than just how it should *look*.

## Accessibility (A11y)
Screen readers for visually impaired users rely on semantic tags to navigate a page. For example, a `<nav>` tag tells the screen reader, "This is the navigation section," allowing the user to jump straight to the links.

## SEO (Search Engine Optimization)
Search engines like Google prioritize semantic content. A `<h1>` tag indicates the primary topic of the page, while `<article>` suggests a self-contained piece of content, helping the engine index the page correctly.

## Maintainability
For developers, `<header>` and `<footer>` are much easier to identify in a large codebase than `<div class="top-section">` and `<div class="bottom-section">`.
@end content

@start quiz
@start title
Semantic HTML Quiz
@end title

@start description
Test your knowledge of the benefits of semantic HTML.
@end description

@start question
@start text
What is the primary benefit of using semantic tags for visually impaired users?
@end text
@start answer
@start text
It changes the color of the text.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
It allows screen readers to understand the structure and purpose of different page sections.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
How does semantic HTML affect SEO?
@end text
@start answer
@start text
It tells search engines which parts of the page are the most important (e.g., using `<h1>`).
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
It has no effect on how search engines index a page.
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
Core Semantic Elements
@end title

@start description
Deep dive into the most commonly used semantic tags and their correct application.
@end description

@start content
# Essential Semantic Tags

## Layout Tags
- `<header>`: The introductory content of a page or a section.
- `<nav>`: Contains navigation links.
- `<main>`: The dominant content of the `<body>`. There should only be one `<main>` per page.
- `<footer>`: The bottom section containing copyright, contact info, etc.
- `<section>`: A thematic grouping of content.
- `<article>`: A self-contained composition (e.g., a blog post, a news story).
- `<aside>`: Content indirectly related to the main content (e.g., a sidebar).

## Content-Specific Tags
- `<figure>` and `<figcaption>`: Used for images, diagrams, or code snippets with a caption.
- `<time>`: Represents a specific period in time or a date.
- `<mark>`: Highlights text for reference.

## Example Layout
```html
<body>
  <header>
    <h1>My Blog</h1>
    <nav>
      <ul><li><a href="/">Home</a></li></ul>
    </nav>
  </header>
  <main>
    <article>
      <h2>How to Learn HTML</h2>
      <p>Content goes here...</p>
    </article>
    <aside>
      <p>Related links...</p>
    </aside>
  </main>
  <footer>
    <p>&copy; 2026 Toolspaedeia</p>
  </footer>
</body>
```
@end content

@start quiz
@start title
Core Elements Quiz
@end title

@start description
Check your ability to choose the correct semantic tag.
@end description

@start question
@start text
Which tag should be used for a self-contained blog post?
@end text
@start answer
@start text
`<section>`
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`<article>`
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
How many `<main>` tags are allowed per page?
@end text
@start answer
@start text
Only one.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
As many as needed for different sections.
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
Accessibility and ARIA Roles
@end title

@start description
Using ARIA attributes when semantic HTML isn't enough.
@end description

@start content
# Extending HTML with ARIA

While semantic HTML is the goal, some complex UI components (like tabs or accordions) cannot be described by HTML tags alone. This is where **ARIA (Accessible Rich Internet Applications)** comes in.

## What is ARIA?
ARIA is a set of attributes you add to HTML elements to provide extra information to assistive technologies.

## Common ARIA Attributes
- `role="button"`: Tells the screen reader that a `div` or `span` is acting as a button.
- `aria-label="Close"`: Provides a text label for an element that only has an icon.
- `aria-expanded="false"`: Indicates whether a collapsible section is open or closed.
- `aria-hidden="true"`: Tells the screen reader to ignore this element entirely (e.g., decorative icons).

## The First Rule of ARIA
**If you can use a native HTML element instead of an ARIA role, do it.**
- Use `<button>` instead of `<div role="button">`.
- Use `<nav>` instead of `<div role="navigation">`.
@end content

@start quiz
@start title
ARIA Quiz
@end title

@start description
Verify your understanding of web accessibility extensions.
@end description

@start question
@start text
What is the "First Rule of ARIA"?
@end text
@start answer
@start text
Always use ARIA roles on every single tag.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
Use native HTML semantic elements whenever possible before resorting to ARIA.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Which ARIA attribute is used to provide a text description for an element that has no visible text?
@end text
@start answer
@start text
`aria-label`
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
`aria-hidden`
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
