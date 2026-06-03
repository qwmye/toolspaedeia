@start name
Python Data Science with Pandas
@end name

@start description
Master the art of data manipulation and analysis using NumPy and Pandas. Learn how to clean, transform, and visualize data for professional insights.
@end description

@start module
@start title
NumPy Fundamentals
@end title

@start description
Introduction to the NumPy library and the power of n-dimensional arrays.
@end description

@start content
## Why NumPy?

NumPy provides a fast, memory-efficient way to store and manipulate numerical data. Standard Python lists are slow for mathematical operations because they store pointers to objects. NumPy arrays store data in contiguous memory blocks.

```python
import numpy as np

arr = np.array([1, 2, 3, 4])
print(arr * 2)  # [2, 4, 6, 8] - Element-wise operation
```

## Array Shaping and Slicing

You can reshape arrays to change their dimensions without changing the data.

```python
arr_2d = np.array([[1, 2], [3, 4]])
print(arr_2d.shape) # (2, 2)
```
@end content

@start quiz
@start title
Quiz: NumPy
@end title

@start description
Verify your understanding of NumPy arrays.
@end description

@start question
@start text
What is the primary advantage of NumPy arrays over Python lists for numerical data?
@end text

@start answer
@start text
They are easier to read.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
They provide element-wise operations and better memory efficiency.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
They cannot be modified after creation.
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
Pandas DataFrames and Series
@end title

@start description
Learn the core data structures of Pandas: the Series and the DataFrame.
@end description

@start content
## Pandas Series

A Series is a one-dimensional labeled array. Think of it as a column in a table.

## Pandas DataFrame

A DataFrame is a two-dimensional table with rows and columns. It is the most common way to represent tabular data in Python.

```python
import pandas as pd

data = {
    "Name": ["Ana", "Bogdan"],
    "Age": [21, 24]
}
df = pd.DataFrame(data)
print(df.head())
```
@end content

@start quiz
@start title
Quiz: Pandas Basics
@end title

@start description
Test your knowledge of DataFrames.
@end description

@start question
@start text
Which Pandas object is used to represent a 2D table?
@end text

@start answer
@start text
Series
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
DataFrame
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Array
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
Handle missing values and transform data for analysis.
@end description

@start content
## Handling Missing Data

Real-world data is often messy. Pandas provides `fillna()` and `dropna()` to manage missing values (`NaN`).

```python
df['Age'] = df['Age'].fillna(df['Age'].mean())
```

## Filtering and Grouping

Use boolean indexing to filter data and `groupby()` to aggregate results.

```python
filtered_df = df[df['Age'] > 20]
grouped = df.groupby('City').mean()
```
@end content

@start quiz
@start title
Quiz: Data Cleaning
@end title

@start description
Verify your data transformation skills.
@end description

@start question
@start text
What is the purpose of the `fillna()` method in Pandas?
@end text

@start answer
@start text
To delete rows with missing values.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
To replace missing values with a specific value or method.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
To sort the data by a specific column.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
