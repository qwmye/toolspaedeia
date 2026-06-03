@start name
Python Web Development with Django
@end name

@start description
Learn to build robust, scalable web applications using the Django framework.
@end description

@start module
@start title
Django Architecture: MVT Pattern
@end title

@start description
Understanding the Model-View-Template architecture that powers Django.
@end description

@start content
# The Django MVT Architecture

Django follows a variation of the MVC (Model-View-Controller) pattern called **MVT (Model-View-Template)**.

## The Model
The Model is the data access layer. It defines the database structure and handles data validation.

```python
# models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
```

## The View
The View is the business logic layer. It processes user requests and returns the appropriate response (usually by calling a template).

```python
# views.py
from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})
```

## The Template
The Template is the presentation layer. It is an HTML file that uses the Django Template Language (DTL) to display dynamic data.

```html
<!-- list.html -->
{% for article in articles %}
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
{% endfor %}
```
@end content

@start quiz
@start title
MVT Architecture Quiz
@end title

@start description
Check your understanding of the Model-View-Template pattern.
@end description

@start question
@start text
In Django, which component is responsible for interacting with the database?
@end text
@start answer
@start text
The Template
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
The Model
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is the role of the View in the MVT architecture?
@end text
@start answer
@start text
To define the HTML structure of the page.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To handle the business logic and coordinate between the Model and the Template.
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
URL Routing and Request Handling
@end title

@start description
Mapping web addresses to the correct views using URLconf.
@end description

@start content
# Routing in Django

Routing is the process of mapping a URL pattern to a specific view function.

## The `urls.py` File
Django uses a list of URL patterns. When a request comes in, Django searches this list from top to bottom.

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
]
```

## Path Converters
Path converters allow you to capture parts of the URL as arguments to your view.
- `<int:pk>`: Captures an integer (usually a Primary Key).
- `<str:slug>`: Captures a string.

## Request and Response Objects
- **HttpRequest**: Contains metadata about the request (headers, GET/POST data).
- **HttpResponse**: The content sent back to the client (HTML, JSON, etc.).
@end content

@start quiz
@start title
URL Routing Quiz
@end title

@start description
Verify your knowledge of Django routing.
@end description

@start question
@start text
Which file is primarily used to define the URL patterns of a Django application?
@end text
@start answer
@start text
`models.py`
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
`urls.py`
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
What is the purpose of the `<int:pk>` converter in a URL path?
@end text
@start answer
@start text
To ensure that only integer values are captured from that part of the URL.
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
To encrypt the URL for security.
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
The Django Admin and ORM
@end title

@start description
Exploring the powerful built-in admin interface and the Object-Relational Mapper.
@end description

@start content
# The Power of Django's Toolset

One of Django's "batteries-included" features is the automatic admin interface and the ORM.

## The ORM (Object-Relational Mapper)
The ORM allows you to interact with your database using Python code instead of writing raw SQL.

- **Create**: `Article.objects.create(title="Hello", content="World")`
- **Read**: `Article.objects.filter(title__contains="Hello")`
- **Update**: `article.title = "New Title"; article.save()`
- **Delete**: `article.delete()`

## The Django Admin
By registering your models in `admin.py`, Django automatically creates a professional backend for managing your data.

```python
# admin.py
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

## Migrations
Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema.
- `python manage.py makemigrations`: Creates the migration file.
- `python manage.py migrate`: Applies the migration to the DB.
@end content

@start quiz
@start title
Admin and ORM Quiz
@end title

@start description
Check your understanding of the ORM and migrations.
@end description

@start question
@start text
What is the purpose of the Django ORM?
@end text
@start answer
@start text
To optimize the speed of the HTML templates.
@end text
@start is_correct
false
@end is_correct
@end answer
@start answer
@start text
To allow database interaction using Python objects instead of raw SQL.
@end text
@start is_correct
true
@end is_correct
@end answer
@end question

@start question
@start text
Which command is used to actually apply migrations to the database?
@end text
@start answer
@start text
`python manage.py migrate`
@end text
@start is_correct
true
@end is_correct
@end answer
@start answer
@start text
`python manage.py makemigrations`
@end text
@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
