@start name
Python Data Science with Pandas
@end name

@start description
Mastering the Pandas library for data manipulation, analysis, and cleaning in Python.
@end description

@start module
@start title
Introduction to Pandas Series and DataFrames
@end title

@start description
Understanding the core data structures of Pandas: Series and DataFrames.
@end description

@start content
# Core Data Structures in Pandas

Pandas provides two primary data structures: the **Series** and the **DataFrame**.

## The Pandas Series
A Series is a one-dimensional labeled array capable of holding any data type. Think of it as a single column in a table.

```python
import pandas as pd

s = pd.Series([1, 3, 5, numpy.nan, 6, 8], index=['a', 'b', 'c', 'd', 'e', 'f'])
print(s)
```

## The Pandas DataFrame
A DataFrame is a two-dimensional, size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns). It is like a spreadsheet or SQL table.

```python
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)
print(df)
```

## Loading Data
Pandas makes it easy to load data from various formats:
- `pd.read_csv('file.csv')`
- `pd.read_excel('file.xlsx')`
- `pd.read_sql('SELECT * FROM table', connection)`
@end content

@start quiz
@start title
Data Structures Quiz
@end title

@start description
Verify your understanding of Series and DataFrames.
@end description

@start question
@start text
What is the main difference between a Series and a DataFrame in Pandas?
@end text
@start answer
@start text
A Series is 1D, while a DataFrame is 2D.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
A Series can only hold integers, while a DataFrame can hold any type.
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
Which function is used to read a CSV file into a DataFrame?
@end text
@start answer
@start text
`pd.read_file()`
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`pd.read_csv()`
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
Data Selection and Filtering
@end title

@start description
Techniques for slicing, dicing, and filtering data within DataFrames.
@end description

@start content
# Accessing and Filtering Data

Pandas provides powerful tools to extract specific subsets of data.

## Selection with `.loc` and `.iloc`
- **`.loc`**: Label-based selection.
- **`.iloc`**: Integer-position-based selection.

```python
# Selecting row index 0 to 2 and column 'Name'
df.loc[0:2, 'Name']

# Selecting first 2 rows and first 2 columns
df.iloc[0:2, 0:2]
```

## Boolean Indexing
You can filter data based on conditions.

```python
# Find people older than 28
older_than_28 = df[df['Age'] > 28]
```

## The `.query()` Method
For more readable filtering, use the `.query()` method.

```python
df.query('Age > 28 and City == "London"')
```
@end content

@start quiz
@start title
Selection and Filtering Quiz
@end title

@start description
Test your ability to filter data in Pandas.
@end description

@start question
@start text
Which Pandas indexer is used for label-based selection?
@end text
@start answer
@start text
`.iloc`
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`.loc`
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is the result of `df[df['Age'] > 28]`?
@end text
@start answer
@start text
A DataFrame containing only the rows where the Age column is greater than 28.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
A list of all ages in the DataFrame.
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
Data Cleaning and Transformation
@end title

@start description
Handling missing data, renaming columns, and transforming values.
@end description

@start content
# Cleaning Messy Data

Real-world data is rarely clean. Pandas provides tools to handle missing values and incorrect formatting.

## Handling Missing Data
Missing data is typically represented as `NaN` (Not a Number).

- **Detecting**: `df.isna()` or `df.isnull()`
- **Filling**: `df.fillna(value)` (e.g., fill with mean or zero).
- **Dropping**: `df.dropna()` (removes rows/columns with missing values).

## Data Transformation
- **Renaming**: Use `df.rename(columns={'old': 'new'})`.
- **Applying Functions**: Use `.apply()` to run a function on every element.

```python
df['Name'] = df['Name'].apply(lambda x: x.upper())
```

## Aggregation and GroupBy
The `.groupby()` method allows you to group data by a certain column and apply an aggregate function.

```python
# Average age per city
df.groupby('City')['Age'].mean()
```
@end content

@start quiz
@start title
Data Cleaning Quiz
@end title

@start description
Check your knowledge of data cleaning techniques.
@end description

@start question
@start text
Which method is used to remove rows that contain missing values?
@end text
@start answer
@start text
`.dropna()`
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
`.remove_nulls()`
@end text
@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
How do you change the names of columns in a DataFrame?
@end text
@start answer
@start text
By renaming the original CSV file.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
Using the `.rename(columns={...})` method.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question
@end quiz
@end module
