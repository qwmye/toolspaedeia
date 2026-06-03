@start name
Toolspaedeia Advanced Authoring & Import/Export
@end name

@start description
Master the professional tools for content creation on Toolspaedeia. Learn how to leverage extended Markdown, manage bulk imports, and handle data portability.
@end description

@start module
@start title
Advanced Markdown Features
@end title

@start description
Go beyond basic text with professional formatting tools for scientific and technical content.
@end description

@start content
## Mathematical Equations

Toolspaedeia supports LaTeX-style math. Use single dollar signs for inline math: $E = mc^2$. Use double dollar signs for block equations:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## Definition Lists and Task Lists

Create structured glossaries and checklists to improve the learning experience:

Term
: A short definition of the term.

- [x] Concept learned
- [ ] Practical exercise completed
@end content

@start quiz
@start title
Quiz: Advanced Formatting
@end title

@start description
Verify your knowledge of advanced markdown syntax.
@end description

@start question
@start text
Which symbol is used to start a block-level mathematical equation?
@end text

@start answer
@start text
A single dollar sign ($)
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Double dollar signs ($$)
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
A hash tag (#)
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
Data Portability and Bulk Import
@end title

@start description
Manage your content efficiently by importing and exporting in open formats.
@end description

@start content
## The Philosophy of Plain Text

Toolspaedeia avoids "vendor lock-in" by using Markdown as its primary storage format. This ensures that your courses can be read by any standard text editor, independent of the platform.

## Bulk Import Workflow

Instead of creating modules one by one through the UI, publishers can import a single `.md` file containing the entire course structure.

The import engine parses the `@start` and `@end` tags to automatically create:
1. The Course metadata.
2. Multiple Modules with titles and descriptions.
3. Nested Quizzes and Questions.
@end content

@start quiz
@start title
Quiz: Data Management
@end title

@start description
Test your understanding of content portability.
@end description

@start question
@start text
Why does Toolspaedeia use Markdown instead of a proprietary binary format?
@end text

@start answer
@start text
Because Markdown is harder to read.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
To ensure data portability and avoid vendor lock-in.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Because it is impossible to render Markdown in a browser.
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
Course Structuring Strategies
@end title

@start description
Design your courses for maximum cognitive retention and learner engagement.
@end description

@start content
## The "Micro-Learning" Approach

Break complex topics into small, digestible modules. A well-structured module should:
- Have one clear learning objective.
- Provide a concise theoretical explanation.
- Include a practical example (code, formula, or case study).
- End with a short validation quiz.

## Balancing Theory and Practice

A common mistake is providing too much theory without immediate application. Use the "Explain $\rightarrow$ Demonstrate $\rightarrow$ Validate" cycle in every module.
@end content

@start quiz
@start title
Quiz: Course Design
@end title

@start description
Verify your understanding of educational structuring.
@end description

@start question
@start text
What is the ideal structure for a "lean" learning module?
@end text

@start answer
@start text
A long text block followed by a massive 50-question exam.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
A clear objective, concise content, a practical example, and a short quiz.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Only a quiz without any theoretical explanation.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
