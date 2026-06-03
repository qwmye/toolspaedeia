@start name
Python Web Development with Django
@end name

@start description
Build robust, scalable web applications using the Django framework. Learn the MVT architecture, ORM, and how to create a secure production-ready site.
@end description

@start module
@start title
Introduction to MVT Architecture
@end title

@start description
Understand how Django separates data, logic, and presentation.
@end description

@start content
## The Model-View-Template (MVT) Pattern

Django follows the MVT pattern:
- **Model**: Defines the data structure and interacts with the database.
- **View**: Contains the business logic and processes the user's request.
- **Template**: The HTML file that renders the final output to the user.

### Request-Response Cycle

When a user visits a URL:
1. `urls.py` maps the URL to a specific view.
2. The View retrieves data from the Model.
3. The View passes that data to the Template.
4. The Template renders HTML and is sent back to the user.
@end content

@start quiz
@start title
Quiz: MVT Architecture
@end title

@start description
Verify your understanding of the MVT flow.
@end description

@start question
@start text
Which component in Django is responsible for interacting with the database?
@end text

@start answer
@start text
Template
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
View
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
Model
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
Django ORM and Database Modeling
@end title

@start description
Learn how to define models and query data without writing raw SQL.
@end description

@start content
## Defining Models

Models are Python classes that inherit from `django.db.models.Model`.

```python
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

## Querying Data

The Django ORM allows you to perform complex queries using Python methods.

```python
# Get all courses with price > 10
expensive_courses = Course.objects.filter(price__gt=10)

# Get a single course by ID
course = Course.objects.get(id=1)
```
@end content

@start quiz
@start title
Quiz: Django ORM
@end title

@start description
Test your knowledge of database interactions in Django.
@end description

@start question
@start text
Which method is used to retrieve all objects from a model?
@end text

@start answer
@start text
all()
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
get()
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
filter()
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
Templates and Static Files
@end title

@start description
Create dynamic HTML pages using the Django Template Language (DTL).
@end description

@start content
## Django Template Language (DTL)

DTL allows you to embed Python-like logic in HTML using tags:
- `{{ variable }}`: Renders a variable.
- `{% if ... %}`: Conditional logic.
- `{% for ... %}`: Loops through a list.

Example:
```html
<h1>{{ course.title }}</h1>
<ul>
    {% for module in course.modules.all %}
        <li>{{ module.title }}</li>
    {% endfor %}
</ul>
```

## Static Files

Images, CSS, and JS are handled as static files. Use `{% load static %}` and `{% static 'path/to/file' %}` to reference them.
@end content

@start quiz
@start title
Quiz: Templates
@end title

@start description
Verify your knowledge of the Django Template Language.
@end description

@start question
@start text
Which tag is used to loop through a list of items in a Django template?
@end text

@start answer
@start text
{% loop %}
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
{% for %}
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
{% while %}
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
