@start name
Python for Web Scraping
@end name

@start description
Learn how to extract data from websites using BeautifulSoup and Selenium. This course covers HTML parsing, handling dynamic content, and ethical scraping practices.
@end description

@start module
@start title
HTTP Requests and BeautifulSoup
@end title

@start description
Understand the basics of sending requests and parsing static HTML.
@end description

@start content
## Sending Requests

The `requests` library is the standard for fetching web pages.

```python
import requests
response = requests.get("https://example.com")
html_content = response.text
```

## Parsing with BeautifulSoup

BeautifulSoup allows you to navigate the HTML tree and find specific elements using tags, classes, and IDs.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, "html.parser")
title = soup.find("h1").text
links = soup.find_all("a")
```

### CSS Selectors

You can use `select()` to find elements using CSS selector syntax: `soup.select("div.article > p")`.
@end content

@start quiz
@start title
Quiz: BeautifulSoup Basics
@end title

@start description
Verify your ability to extract data from static HTML.
@end description

@start question
@start text
Which library is typically used to send HTTP requests in Python web scraping?
@end text

@start answer
@start text
BeautifulSoup
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
requests
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
Selenium
@end text

@start is_correct
false
@end is_correct
@end answer
@end question

@start question
@start text
What does the `find_all()` method in BeautifulSoup return?
@end text

@start answer
@start text
A single element
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
A list of all matching elements
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
A string containing the inner text
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
Handling Dynamic Content with Selenium
@end title

@start description
Extract data from websites that use JavaScript to render content.
@end description

@start content
## The Need for Browser Automation

Some websites use frameworks like React or Vue that render content on the client side. A simple `requests.get()` will only see the initial empty HTML.

Selenium automates a real browser (Chrome, Firefox) to execute JavaScript and load the full content.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")
element = driver.find_element(By.ID, "dynamic-content")
print(element.text)
driver.quit()
```

## Headless Browsing

Running a browser in "headless" mode means it runs in the background without a GUI, which is faster and essential for server-side scraping.
@end content

@start quiz
@start title
Quiz: Selenium and Dynamic Content
@end title

@start description
Test your knowledge of browser automation.
@end description

@start question
@start text
Why is Selenium preferred over BeautifulSoup for some websites?
@end text

@start answer
@start text
It is faster at parsing HTML.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
It can execute JavaScript to render dynamic content.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
It does not require a driver to be installed.
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
Ethical Scraping and Robots.txt
@end title

@start description
Learn the legal and ethical guidelines for scraping web data.
@end description

@start content
## The Robots Exclusion Protocol

Websites use a file called `robots.txt` to tell crawlers which parts of the site can be visited.
Check `https://example.com/robots.txt` before scraping.

## Best Practices

To avoid being blocked or overloading servers:
- **Rate Limiting:** Add delays between requests using `time.sleep()`.
- **User-Agent:** Set a realistic `User-Agent` header to identify your bot.
- **Respect Terms of Service:** Always check the site's TOS for prohibitions on scraping.
@end content

@start quiz
@start title
Quiz: Ethical Scraping
@end title

@start description
Check your understanding of scraping ethics.
@end description

@start question
@start text
What is the purpose of the `robots.txt` file?
@end text

@start answer
@start text
To store the site's CSS styles.
@end text

@start is_correct
false
@end is_correct
@end answer

@start answer
@start text
To specify which pages should not be crawled by bots.
@end text

@start is_correct
true
@end is_correct
@end answer

@start answer
@start text
To encrypt the data on the website.
@end text

@start is_correct
false
@end is_correct
@end answer
@end question
@end quiz
@end module
