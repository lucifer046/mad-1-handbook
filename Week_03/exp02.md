## Project Structure
```text
experiment-templates/
 app.py
 janapith.html
```

---

# Experiment 02: Jinja2 Templates
This experiment demonstrates how to separate data from presentation using the **Jinja2** templating engine.

## Detailed Code Breakdown

### 1. The Template String (`TPL`)
* Instead of writing a static HTML file, we write a template with "placeholders".
* `{% for item in data %}`: This is a Jinja2 control structure. It tells the engine to loop through a Python list and repeat the HTML code inside for every item.
* `{{ item["year"] }}`: The double curly braces indicate an expression that should be evaluated and printed into the HTML.

### 2. The Data (`j_data`)
* We use a standard Python list of dictionaries. This represents the dynamic data that would typically come from a database or an API.

### 3. The Rendering Process
* `tpl_obj = Template(TPL)`: We compile the raw string into a Jinja2 template object.
* `tpl_obj.render(data=j_data)`: This is the critical step. The engine merges the Python data into the HTML placeholders to produce a final, standard HTML string.
* `f.write(rendered_html)`: Finally, we save the generated HTML to a file so it can be viewed in a browser.
