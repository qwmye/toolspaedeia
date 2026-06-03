@start name
Advanced Authoring & Import/Export
@end name

@start description
An advanced guide for course creators on how to structure high-quality academic content, use the tag-based formatting system, and manage content migration.
@end description

@start module
@start title
The Tag-Based Formatting System
@end title

@start description
Understanding the syntax and logic behind the @start and @end tags used in Toolspaedeia.
@end description

@start content
# Understanding the Authoring Syntax

Toolspaedeia uses a unique tag-based system instead of traditional Markdown headers for its primary structural elements. This ensures that the content can be parsed deterministically for different display modes (web, mobile, print).

## The Core Tag Pair
Every structural element must be wrapped in a `@start [element]` and `@end [element]` pair.

### High-Level Elements:
- `@start name` / `@end name`: The official title of the course.
- `@start description` / `@end description`: A brief overview of the course objectives.

### Module Elements:
- `@start module` / `@end module`: Wraps an entire learning module.
- `@start title` / `@end title`: The name of the specific module.
- `@start content` / `@end content`: The actual instructional material.

## Why Not Use Standard Headers for Structure?
While standard Markdown (`#`, `##`, `###`) is used *inside* the `@start content` block for visual formatting, the structural tags provide metadata that the platform uses to generate:
1. Table of Contents automatically.
2. Progress tracking indices.
3. Searchable knowledge graph nodes.
@end content

@start quiz
@start title
Formatting Fundamentals Quiz
@end title

@start description
Test your knowledge of the structural tags.
@end description

@start question
@start text
Which tag is used to define the start of a learning module?
@end text
@start answer
@start text
@start module
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
# module
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
Where should standard Markdown headers (e.g., # Header) be used?
@end text
@start answer
@start text
To replace @start name tags.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
Inside the @start content and @end content block.
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
Creating Effective Quizzes
@end title

@start description
Best practices for designing assessments that accurately measure student understanding.
@end description

@start content
# Assessment Design

A course is only as good as its verification process. The `@start quiz` block is where students prove their mastery.

## Quiz Anatomy
A quiz consists of:
1. **Title**: A clear name for the assessment.
2. **Description**: Context for the student.
3. **Questions**: The core unit of the quiz.

## Crafting High-Quality Questions
Avoid "trick" questions. Instead, focus on conceptual understanding and application.

- **Avoid**: "Which of these is NOT a feature of X?" (Too easy to guess).
- **Prefer**: "Given the following scenario, which feature of X is most appropriate?" (Requires application).

## The Answer Structure
Each question must have multiple `@start answer` blocks. Only one should be marked `@start is_correct` as `true`.

### Example:
@start answer
@start text
Correct Option
@end text
@start is_correct
true
@end is_correct
@end answer
@end content

@start quiz
@start title
Quiz Design Quiz
@end title

@start description
Verify your ability to create effective assessments.
@end description

@start question
@start text
What is the recommended approach for crafting high-quality questions?
@end text
@start answer
@start text
Use as many trick questions as possible.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
Focus on conceptual understanding and application of knowledge.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
In the Toolspaedeia system, how many answers can be marked as 'true' for a single question?
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
As many as the author desires.
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
Import, Export, and Content Migration
@end title

@start description
Managing course data across different environments and versioning your content.
@end description

@start content
# Content Lifecycle Management

As your courses evolve, you will need to move them between development and production environments.

## Exporting Courses
Courses are exported as individual `.md` files. Because they use a standardized tag system, they can be imported into any Toolspaedeia instance without losing their structural integrity.

## Bulk Importing
To import multiple courses, place them in a single directory and use the `Bulk Import` tool in the Authoring Dashboard. The system will automatically scan for files following the `XX-course-name.md` naming convention.

## Versioning Your Content
It is highly recommended to keep your `.md` files in a version control system like Git. This allows you to:
- Roll back to previous versions of a module.
- Track changes made by different contributors.
- Branch your course for "Experimental" vs "Stable" releases.
@end content

@start quiz
@start title
Migration Quiz
@end title

@start description
Testing knowledge on import/export and versioning.
@end description

@start question
@start text
What is the recommended naming convention for bulk importing courses?
@end text
@start answer
@start text
Random names with dates.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`XX-course-name.md`
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Why is using Git recommended for course authoring?
@end text
@start answer
@start text
To automatically generate the content.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To track changes and manage different versions of the content.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question
@end quiz
@end module
