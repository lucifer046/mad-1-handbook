# Jinja2 Templating Deep Dive

## Dynamic Rendering: The Core Concept

In modern web development, we need to generate HTML documents dynamically. Instead of creating a separate static HTML file for each student, user, or product, we create a single **template** with placeholders and fill them with data at runtime.

Python offers three primary ways to format or templating strings:
1. **f-strings** (Built-in string formatting)
2. **`string.Template`** (Standard library templating module)
3. **`jinja2.Template`** (Powerful external templating engine)

---

## 1. Python f-strings vs. Jinja2 Templates

### Python f-strings
Introduced in Python 3.6, f-strings provide a concise, readable syntax for embedding expressions directly inside string literals by prefixing the string with `f` and wrapping variables in curly braces `{}`.

```python
name = "Shiv"
place = "Chennai"
profession = "Data Analyst"

# Format string using f-strings
text = f"My name is {name}, I live in {place} and I am a {profession}."
print(text)
# Output: My name is Shiv, I live in Chennai and I am a Data Analyst.
```

### Jinja2 Templating
Jinja2 is an external, robust library that compiles templates into Python code. To use it, you must first install it:
```bash
pip install jinja2
```

In Jinja2, placeholders are represented by double curly braces `{{ }}`. Creating and rendering a template consists of three steps:

```python
from jinja2 import Template

name = "Shiv"
place = "Chennai"
profession = "Data Analyst"

# Step 1: Create Template Text with Placeholders
temp_string = "My name is {{name}}, I live in {{place}} and I am a {{profession}}"

# Step 2: Convert String into a Template Object
made_temp = Template(temp_string)

# Step 3: Render the Template with Data
output = made_temp.render(name=name, place=place, profession=profession)
print(output)
# Output: My name is Shiv, I live in Chennai and I am a Data Analyst
```

[NOTE]
**Left-Hand vs. Right-Hand Variables**: In `.render(name=name)`, the left parameter refers to the **placeholder identifier** inside the template, while the right parameter represents the **actual Python variable** containing the data.
[/CALLOUT]

---

## 2. Standard `string.Template` vs. `jinja2.Template`

The standard library's `string.Template` is designed for simple, safe string substitutions, whereas `jinja2.Template` is optimized for web page generation with advanced scripting controls.

### Syntax Differences
*   **`string.Template`**: Uses a dollar sign (`$`) prefix: `$variable`.
*   **`jinja2.Template`**: Uses double curly braces: `{{ variable }}`.

```python
# string.Template
from string import Template
temp_std = Template("Today is $today and tomorrow is $tomorrow.")

# jinja2.Template
from jinja2 import Template
temp_jinja = Template("Today is {{today}} and tomorrow is {{tomorrow}}.")
```

### Error Handling Comparison

| Feature | `string.Template` (`substitute`) | `string.Template` (`safe_substitute`) | `jinja2.Template` (`render`) |
| :--- | :--- | :--- | :--- |
| **Missing Variable** | Throws a **`KeyError`** | Leaves placeholder intact as text (e.g., `$tomorrow`) | Renders placeholder as a **blank empty string** |
| **Use Case** | Strict parameters validation | Simple command-line config formatting | HTML generation where missing attributes shouldn't crash the server |

```python
# string.Template - substitute raises KeyError if a variable is missing
try:
    temp_std.substitute(today="Monday")
except KeyError as e:
    print(f"Error raised: {e}") # Raises KeyError for 'tomorrow'

# string.Template - safe_substitute completes safely
print(temp_std.safe_substitute(today="Monday"))
# Output: Today is Monday and tomorrow is $tomorrow.

# jinja2.Template - render completes silently, rendering nothing for missing values
print(temp_jinja.render(today="Monday"))
# Output: Today is Monday and tomorrow is .
```

---

## 3. Dynamic HTML Generation

Jinja2 templates are typically used to construct complex HTML responses:

```python
from jinja2 import Template

name = "Divya"
place = "Delhi"

temp_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Profile</title>
</head>
<body>
    <h2>My name is {{name}}</h2>
    <h2>I live in {{place}}</h2>
</body>
</html>
"""

template = Template(temp_html)
rendered_html = template.render(name=name, place=place)
print(rendered_html)
```

---

## 4. Control Structures & Loops in Jinja2

Jinja2 templates support logic structures (loops and conditionals) using curly-brace-percent tags `{% %}`.

### For Loops
To render lists dynamically (e.g., table rows or menu links):

```python
from jinja2 import Template

jobs = ["Programmer", "Analyst", "Scientist"]
temp_loop = "My data is: {% for i in Data %} {{i}} {% endfor %}"

template = Template(temp_loop)
print(template.render(Data=jobs))
# Output: My data is:  Programmer  Analyst  Scientist 
```

### For Loops with Conditionals (If statements)
You can filter lists dynamically inside the template loop:

```python
from jinja2 import Template

jobs = ["Programmer", "Analyst", "Scientist"]
temp_filtered = """
{% for i in data %}
   {% if "z" in i %}
      {{i}}
   {% endif %}
{% endfor %}
No data found
"""

template = Template(temp_filtered)
print(template.render(data=jobs))
# Output: No data found (since none of the words have the character 'z')
```

### If-Else Statements
```python
from jinja2 import Template

subject = "MAD 1"
temp_cond = """
{% if "2" in sub %}
    Subject: {{sub}}
{% else %}
    Required subject not found
{% endif %}
"""

template = Template(temp_cond)
print(template.render(sub=subject))
# Output: Required subject not found (since '2' is not in 'MAD 1')
```

---

## 5. Jinja2 Filters

Filters allow you to **transform** variables inside templates using the pipe operator `|`.

### Length Filter (`| length`)
In pure Python, we calculate a list's length using the `len()` function. In Jinja2, we use the `length` filter:

```python
# Python
my_list = [1, 2, 3, 4]
print(len(my_list)) # Outputs 4

# Jinja2 Template
# {{ my_list | length }} -> Outputs 4
```

### Group By Filter (`| groupby`)
The `groupby` filter allows you to group a list of dictionaries by a common key, functioning similarly to SQL's `GROUP BY` clause. It returns a list of grouped objects containing a `grouper` (the key's value) and the `list` of associated items.

```python
from jinja2 import Template

movies = [
    {"title": "Movie A", "producer": "Producer 1"},
    {"title": "Movie B", "producer": "Producer 2"},
    {"title": "Movie C", "producer": "Producer 1"},
    {"title": "Movie D", "producer": "Producer 2"}
]

temp_group = """
{% for producer, group in movies | groupby("producer") %}
  <h2>{{ producer }}</h2>
  <ul>
    {% for movie in group %}
      <li>{{ movie.title }}</li>
    {% endfor %}
  </ul>
{% endfor %}
"""

template = Template(temp_group)
print(template.render(movies=movies))
```

#### Rendered Output:
```html
  <h2>Producer 1</h2>
  <ul>
      <li>Movie A</li>
      <li>Movie C</li>
  </ul>

  <h2>Producer 2</h2>
  <ul>
      <li>Movie B</li>
      <li>Movie D</li>
  </ul>
```

---

## Glossary

| Term | Meaning |
| :--- | :--- |
| **Template** | A string/file with placeholders that is dynamically parsed |
| **`{{ }}`** | Jinja2 variable placeholder tag |
| **`{% %}`** | Jinja2 control block tag (for loops, conditionals) |
| **`{# #}`** | Jinja2 comment tag (ignored during rendering) |
| **Rendering** | The process of compiling a template and substituting placeholders with variables |
| **Filter** | A post-processor function triggered by `\|` (e.g., `length`, `groupby`, `upper`) |
| **Grouper** | The grouping key-value returned during a `groupby` operation |
