from jinja2 import Template

# j_data: janapith_awardees_data
j_data = [
    {"year": 1965, "awardees" : "G. Sankara Kurup", "language":"Malayalam"} ,
    {"year": 1966, "awardees" : "Tarashankar Bandopadhyaya", "language":"Bengali"} ,
    {"year": 1967, "awardees" : "Kuppali Venkatappagowda Puttappa", "language":"Kannada"} ,
]

# TPL: html_template_string
TPL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title> Jnanpith </title>
    <meta name="description" content="This page lists Jnanpith Awardees"/>
</head>
<body>
    <h1> Awardees </h1>
    <table border="1">
        <thead>
            <tr>
                <th>Year</th>
                <th>Awardees</th>
                <th>Language</th>
            </tr>
        </thead>
        <tbody>
            {% for item in data %}
            <tr>
                <td>{{ item["year"] }}</td>
                <td>{{ item["awardees"] }}</td>
                <td>{{ item["language"] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>                    
</body>
</html>
"""

# Init Jinja2 template
tpl_obj = Template(TPL)

# Render template with data
rendered_html = tpl_obj.render(data=j_data)

# Write to file
with open('janapith.html', 'w') as f:
    f.write(rendered_html)