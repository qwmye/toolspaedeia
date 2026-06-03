@start name
HTML5 Semantic Structure
@end name

@start description
Learn how to build accessible and SEO-friendly websites using HTML5 semantic elements and modern standards.
@end description

@start module
@start title
The Power of Semantics
@end title

@start description
Understand the difference between generic containers and semantic tags.
@end description

@start content
## Why Semantics?

Using `<div>` for everything makes a site "invisible" to screen readers and search engines. Semantic tags tell the browser what the content *is*, not just how it looks.

## Key Semantic Elements

- `<header>`: Introduction or navigation section.
- `<main>`: The primary content of the document.
- `<article>`: An independent, self-contained composition.
- `<section>`: A generic thematic grouping.
- `<aside>`: Content indirectly related to the main content.
- `<footer>`: Footer for the page or section.
@end content

@start quiz
@start title
Quiz: Semantics
@end title

@start description
Verify your understanding of HTML5 tags.
@end description

@start question
@start text
Which tag should be used for a self-contained piece of content that could be distributed independently, like a blog post?
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

@start answer
@start text
`<div>`
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
Forms and Input Validation
@end title

@start description
Build interactive forms with built-in browser validation and modern input types.
@end description

@start content
## Modern Input Types

HTML5 introduced specific types to improve user experience and data quality:
- `type="email"`: Ensures a valid email format.
- `type="number"`: Restricts input to digits.
- `type="date"`: Opens a native date picker.
- `type="range"`: Provides a slider.

## Validation Attributes

- `required`: The field must be filled.
- `pattern="[A-Z]{3}"`: Uses regular expressions to validate content.
- `min`/`max`: Define numeric boundaries.
@end content

@start quiz
@start title
Quiz: Forms
@end title

@start description
Test your knowledge of form validation.
@end description

@start question
@start text
Which attribute is used to ensure a form field is not left empty?
@end text

@start answer
@start text
`validate`
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
`required`
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
`essential`
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
Accessibility (a11y) and SEO
@end title

@start description
Optimize your HTML for screen readers and search engine crawlers.
@end description

@start content
## ARIA Roles

When semantic tags aren't enough, use `aria-` attributes (Accessible Rich Internet Applications) to provide context.
Example: `aria-label="Close Menu"` on an icon-only button.

## SEO Best Practices

- Use only one `<h1>` per page.
- Use `alt` text for all images to describe the content.
- Implement `meta` tags for descriptions and keywords.
@end content

@start quiz
@start title
Quiz: Accessibility
@end title

@start description
Verify your knowledge of a11y and SEO.
@end description

@start question
@start text
What is the purpose of the `alt` attribute in an `<img>` tag?
@end text

@start answer
@start text
To specify the image's URL.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
To provide a text description for screen readers and broken images.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
To change the image's transparency.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
