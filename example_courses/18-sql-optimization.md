@start name
Advanced SQL & Query Optimization
@end name

@start description
Take your database skills to the professional level. Learn about indexing, execution plans, and the art of writing high-performance queries.
@end description

@start module
@start title
Indexes and Performance
@end title

@start description
Understand how B-Trees and Hash indexes speed up data retrieval.
@end description

@start content
## What is an Index?

An index is a separate data structure (usually a B-Tree) that stores pointers to the rows in a table. Instead of scanning the entire table (Full Table Scan), the database can find the data in O(log n) time.

## Types of Indexes

- **Clustered Index**: Determines the physical order of data in the table. A table can have only one clustered index (usually the Primary Key).
- **Non-Clustered Index**: A separate structure that points to the data. You can have many of these.

## The Cost of Indexing

Indexes speed up `SELECT` queries but slow down `INSERT`, `UPDATE`, and `DELETE` operations because the index must be updated every time the data changes.
@end content

@start quiz
@start title
Quiz: Indexing Basics
@end title

@start description
Verify your understanding of database indexing.
@end description

@start question
@start text
Which type of index determines the physical ordering of data in a table?
@end text

@start answer
@start text
Non-Clustered Index
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Clustered Index
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Hash Index
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
Execution Plans and EXPLAIN
@end title

@start description
Learn how to read the database's internal "roadmap" to find bottlenecks.
@end description

@start content
## The Query Optimizer

The database engine doesn't just execute your SQL. It uses a "Query Optimizer" to decide the most efficient way to get the data.

## Using EXPLAIN

By prepending `EXPLAIN` to a query, you can see the execution plan:

```sql
EXPLAIN SELECT * FROM courses WHERE publisher_id = 5;
```

Key things to look for:
- **Full Table Scan**: Bad performance for large tables.
- **Index Seek / Index Scan**: Efficient retrieval.
- **Nested Loop Join**: Common but can be slow for very large datasets.
@end content

@start quiz
@start title
Quiz: Execution Plans
@end title

@start description
Test your ability to analyze query performance.
@end description

@start question
@start text
Which command allows you to see the la-planned execution path of a SQL query?
@end text

@start answer
@start text
DESCRIBE
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
EXPLAIN
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
ANALYZE
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
Advanced Optimization Techniques
@end title

@start description
Avoid common pitfalls and implement advanced strategies for massive datasets.
@end description

@start content
## SARGability (Search ARGumentable)

A query is "SARGable" if it can take advantage of an index. Using functions on columns prevents index usage.

- **Non-SARGable**: `WHERE YEAR(created_at) = 2023` (Forces full scan)
- **SARGable**: `WHERE created_at >= '2023-01-01' AND created_at < '2024-01-01'` (Uses index)

## Denormalization

In extreme cases, it is better to duplicate some data to avoid expensive joins. This is common in Data Warehousing.

## Materialized Views

A view that stores the result of a query physically on disk, allowing for near-instant retrieval of complex aggregations.
@end content

@start quiz
@start title
Quiz: Optimization
@end title

@start description
Check your knowledge of advanced optimization.
@end description

@start question
@start text
Why is using a function on a column in a WHERE clause (e.g. `WHERE UPPER(name) = 'ANA'`) usually bad for performance?
@end text

@start answer
@start text
It makes the query result incorrect.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It prevents the database from using an index on that column.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It causes a syntax error in MySQL.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
