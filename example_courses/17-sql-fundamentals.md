@start name
SQL Fundamentals
@end name

@start description
Introduction to relational databases, the SQL language, and the art of designing efficient data schemas.
@end description

@start module
@start title
Relational Model and Basic Queries
@end title

@start description
Understand the structure of relational databases and how to retrieve data using SELECT.
@end description

@start content
## The Relational Model

A relational database stores data in tables, consisting of rows (records) and columns (attributes). Every table must have a **Primary Key**—a unique identifier for each row.

## Basic Querying

The `SELECT` statement is used to retrieve data.

```sql
-- Select all columns from the courses table
SELECT * FROM courses;

-- Select only specific columns with a filter
SELECT title, price
FROM courses
WHERE price < 20.00;
```

## Sorting and Limiting

Use `ORDER BY` to sort results and `LIMIT` to restrict the number of rows returned.
@end content

@start quiz
@start title
Quiz: Basic SQL
@end title

@start description
Verify your ability to write basic SELECT queries.
@end description

@start question
@start text
Which SQL clause is used to filter rows based on a specific condition?
@end text

@start answer
@start text
GROUP BY
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
WHERE
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
ORDER BY
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
Joining Tables and Aggregations
@end title

@start description
Combine data from multiple tables and calculate summary statistics.
@end description

@start content
## Joins

Joins allow you to link tables using common columns (Foreign Keys).
- **INNER JOIN**: Returns rows when there is a match in both tables.
- **LEFT JOIN**: Returns all rows from the left table, and matched rows from the right.

```sql
SELECT courses.title, users.first_name
FROM courses
JOIN users ON courses.publisher_id = users.id;
```

## Aggregations

Use functions like `COUNT()`, `SUM()`, `AVG()`, `MIN()`, and `MAX()` to summarize data. When using these, you must group non-aggregated columns using `GROUP BY`.

```sql
SELECT publisher_id, COUNT(*)
FROM courses
GROUP BY publisher_id;
```
@end content

@start quiz
@start title
Quiz: Joins and Aggregates
@end title

@start description
Test your knowledge of relational data retrieval.
@end description

@start question
@start text
Which JOIN type returns all rows from the left table regardless of whether a match exists in the right table?
@end text

@start answer
@start text
INNER JOIN
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
LEFT JOIN
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
FULL OUTER JOIN
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
Data Modification and Schema Design
@end title

@start description
Learn how to insert, update, and delete data, and how to design normalized tables.
@end description

@start content
## Data Manipulation (DML)

- **INSERT**: Adds new rows.
- **UPDATE**: Modifies existing rows.
- **DELETE**: Removes rows.

```sql
UPDATE courses SET price = 15.00 WHERE id = 1;
```

## Normalization

Normalization is the process of organizing data to reduce redundancy.
- **1st Normal Form (1NF)**: Each column contains atomic (indivisible) values.
- **2nd Normal Form (2NF)**: All non-key attributes are fully dependent on the primary key.
- **3rd Normal Form (3NF)**: No transitive dependencies (columns depend only on the primary key).
@end content

@start quiz
@start title
Quiz: Schema and DML
@end title

@start description
Verify your understanding of database design.
@end description

@start question
@start text
What is the main goal of database normalization?
@end text

@start answer
@start text
To make the database take up more disk space.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
To reduce data redundancy and improve data integrity.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
To eliminate the need for primary keys.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
