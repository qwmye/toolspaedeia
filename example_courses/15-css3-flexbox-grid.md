@start name
CSS3 Flexbox and Grid
@end name

@start description
Mastering modern layout techniques to create responsive and flexible web designs.
@end description

@start module
@start title
Flexbox: One-Dimensional Layouts
@end title

@start description
Learning to align elements efficiently along a single axis.
@end description

@start content
# Understanding Flexbox

Flexbox (The Flexible Box Layout Module) is designed for laying out items in a single dimension—either as a row or a column.

## The Flex Container
To start using Flexbox, apply `display: flex;` to a parent element.

```css
.container {
    display: flex;
    flex-direction: row; /* Default: items stay in a line */
}
```

## Key Alignment Properties
- **`justify-content`**: Aligns items along the **main axis** (e.g., `center`, `space-between`, `space-around`).
- **`align-items`**: Aligns items along the **cross axis** (e.g., `center`, `stretch`, `flex-start`).
- **`flex-wrap`**: Determines if items should wrap to a new line if they exceed the container width.

## Flexible Items
Items inside a flex container can be told how to grow or shrink:
- `flex-grow`: Ability for an item to grow if there is extra space.
- `flex-shrink`: Ability for an item to shrink if there is not enough space.
- `flex-basis`: The initial size of an item before growing or shrinking.
@end content

@start quiz
@start title
Flexbox Basics Quiz
@end title

@start description
Test your knowledge of Flexbox alignment.
@end description

@start question
@start text
Which property is used to align items along the main axis of a flex container?
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
@end question

@start question
@start text
What does `flex-wrap: wrap;` do?
@end text
@start answer
@start text
It forces all items to stay on one line, regardless of width.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
It allows flex items to move to the next line if they exceed the container's width.
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
CSS Grid: Two-Dimensional Layouts
@end title

@start description
Creating complex, grid-based layouts with rows and columns.
@end description

@start content
# The Power of CSS Grid

While Flexbox is for 1D layouts, CSS Grid is for 2D layouts (rows AND columns simultaneously).

## Defining the Grid
Apply `display: grid;` to the parent.

```css
.grid-container {
    display: grid;
    grid-template-columns: 200px 1fr 1fr; /* Fixed width, then two flexible fractions */
    grid-template-rows: auto 100px;
    gap: 10px; /* Space between cells */
}
```

## Placing Items
You can tell an item exactly where to start and end in the grid.

```css
.sidebar {
    grid-column: 1 / 2; /* Starts at line 1, ends at line 2 */
    grid-row: 1 / 3;    /* Spans two rows */
}
```

## Grid Areas
For a more intuitive approach, use `grid-template-areas`.

```css
.container {
    display: grid;
    grid-template-areas:
        "header header"
        "sidebar main"
        "footer footer";
}
.header { grid-area: header; }
.main { grid-area: main; }
```
@end content

@start quiz
@start title
CSS Grid Quiz
@end title

@start description
Verify your ability to build a 2D grid.
@end description

@start question
@start text
What is the main difference between Flexbox and CSS Grid?
@end text
@start answer
@start text
Flexbox is for 1D layouts, whereas Grid is for 2D layouts.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Grid is only used for mobile phones, while Flexbox is for desktops.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What does the unit `1fr` represent in a grid definition?
@end text
@start answer
@start text
1 fixed pixel.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
One "fraction" of the available free space.
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
Combining Flex and Grid for Responsive Design
@end title

@start description
Using the right tool for the right job to build a complete, modern webpage.
@end description

@start content
# Responsive Strategy

A professional layout typically uses **Grid for the overall page structure** and **Flexbox for the elements inside** those structures.

## Example: The Modern Page Layout
1. **Grid (Outer)**:
   - Header (Full width)
   - Main Area (Left) + Sidebar (Right)
   - Footer (Full width)
2. **Flexbox (Inner)**:
   - Navigation links inside the Header (Space-between).
   - Centering a button inside a Grid cell.

## Media Queries
To change layouts for different screens, use `@media` queries.

```css
@media (max-width: 768px) {
    .grid-container {
        grid-template-columns: 1fr; /* Stack everything in one column on mobile */
    }
}
```

## Choosing the Right Tool
- Use **Flexbox** when you want to align a group of items in a row/column and don't care about the exact size of the grid.
- Use **Grid** when you need a strict layout of rows and columns that must align across the page.
@end content

@start quiz
@start title
Responsive Strategy Quiz
@end title

@start description
Verify your knowledge of layout selection.
@end description

@start question
@start text
In a typical modern layout, which tool is best for the overall page structure (Header, Main, Sidebar, Footer)?
@end text
@start answer
@start text
CSS Grid
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Flexbox
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
Which CSS feature is used to change the layout based on the screen width (e.g., from 3 columns to 1 column)?
@end text
@start answer
@start text
Media Queries
@end la
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
Flex-wrap
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
