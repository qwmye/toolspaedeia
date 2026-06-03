@start name
CSS3 Flexbox and Grid
@end name

@start description
Master modern CSS layout techniques. Learn how to build responsive, fluid interfaces without the need for fragile floats or heavy frameworks.
@end description

@start module
@start title
Flexbox: One-Dimensional Layouts
@end title

@start description
Learn how to distribute space and align items along a single axis.
@end description

@start content
## Flex Containers

To start using Flexbox, set `display: flex;` on the parent element.

## Main Axis and Cross Axis

- **`justify-content`**: Aligns items along the main axis (horizontal by default).
  - `center`, `space-between`, `space-around`, `flex-start`, `flex-end`.
- **`align-items`**: Aligns items along the cross axis (vertical by default).
  - `center`, `stretch`, `flex-start`, `flex-end`.

## Flex-Grow and Shrink

You can control how an item expands to fill space using `flex-grow: 1;` or shrinks to fit using `flex-shrink`.
@end content

@start quiz
@start title
Quiz: Flexbox Basics
@end title

@start description
Verify your understanding of flex-direction and alignment.
@end description

@start question
@start text
Which property is used to align items horizontally in a standard row-based flex container?
@end text

@start answer
@start text
`align-items`
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
`justify-content`
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
`flex-direction`
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
CSS Grid: Two-Dimensional Layouts
@end title

@start description
Create complex, grid-based layouts that handle both rows and columns simultaneously.
@end description

@start content
## Defining the Grid

Use `display: grid;` and define your columns and rows using `grid-template-columns` and `grid-template-rows`.

```css
.container {
    display: grid;
    grid-template-columns: 200px 1fr 1fr;
    grid-template-rows: auto 1fr auto;
}
```

## Grid Areas and Naming

You can name areas of your grid to make the layout more intuitive:

```css
.container {
    grid-template-areas:
        "header header"
        "sidebar main"
        "footer footer";
}
.header { grid-area: header; }
```
@end content

@start quiz
@start title
Quiz: CSS Grid
@end title

@start description
Test your knowledge of grid-template properties.
@end description

@start question
@start text
What does the `1fr` unit represent in a CSS Grid definition?
@end text

@start answer
@start text
One fixed pixel.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
One fraction of the available free space.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
One percent of the viewport width.
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
Responsive Design and Media Queries
@end title

@start description
Ensure your layouts work on any screen size, from mobile phones to ultra-wide monitors.
@end description

@start content
## Media Queries

Use `@media` rules to apply different styles based on the screen width.

```css
@media (max-width: 600px) {
    .container {
        grid-template-columns: 1fr;
    }
}
```

## Mobile-First Approach

Design for the smallest screen first, then add complexity for larger screens. This results in faster load times on mobile and a cleaner CSS structure.
@end content

@start quiz
@start title
Quiz: Responsive Layouts
@end title

@start description
Check your understanding of media queries.
@end description

@start question
@start text
Which approach involves styling for the smallest screen first and then expanding for larger displays?
@end text

@start answer
@start text
Desktop-First Design
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Mobile-First Design
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Fluid Design
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
