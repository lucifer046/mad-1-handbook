# HTML and the Document Object Model

## What is HTML?

Imagine you are building a house. Before the painter comes, before the interior designer arrives, you need a **skeleton** — the basic structure of walls, rooms, and a roof.

**HTML (HyperText Markup Language)** is the skeleton of every webpage. It defines:
- Where the heading goes
- Where the paragraph goes
- Where the image goes
- Which words are links

HTML does NOT decide colors, fonts, or spacing — that's CSS's job!

---

## What Does an HTML File Look Like?

An HTML file is just a **text file** with special tags wrapped in `< >` brackets. The browser reads these tags and knows how to display the content.

```
<tag>Content goes here</tag>
  ↑                       ↑
Opening tag         Closing tag (has a /)
```

---

## The Structure of Every HTML Page

Every HTML file in the world has the same basic skeleton:

```html
<!DOCTYPE html> <!-- Tells the browser "this is HTML5" -->
<html lang="en"> <!-- The root tag. Everything is inside this. -->

  <head> <!-- INVISIBLE section (info FOR the browser) -->
    <meta charset="UTF-8"> <!-- "Use UTF-8 encoding for all characters" -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- Mobile responsiveness -->
    <title>My Page</title> <!-- What appears in the browser tab -->
  </head>

  <body> <!-- VISIBLE section (what users SEE) -->
    <h1>Hello World!</h1> <!-- A big heading -->
    <p>My first page.</p> <!-- A paragraph of text -->
  </body>

</html>
```

---

## Deep Dive: Core HTML Elements Explained

### 1. `<!DOCTYPE html>`
This declaration tells the browser the document type is HTML5. It ensures that the browser uses modern standards rendering rather than quirks mode.

### 2. `<html>`
The root element of the document. The `lang="en"` attribute specifies that the page language is English, helping search engines and translation tools.

### 3. `<head>`
Contains metadata that is essential for browsers, crawlers, and search engines. It includes character encodings, responsive viewports, stylesheet links (`<link rel="stylesheet">`), and the document title (`<title>`).

### 4. `<body>`
Contains all the visible content (text, forms, buttons, layout divisions).

---

## Core HTML Tags: Your Toolbox

### Structural & Semantic Tags (For organizing sections)
Semantic HTML tags describe the **meaning** of the block, not just its styling.

```html
<header> → Top section of a page (logo, navigation)
<nav> → Navigation links container
<main> → The unique main content area of the document
<section> → A thematic group of content (usually has a heading)
<article> → A self-contained piece of content (like a blog post or comment)
<aside> → Content indirectly related to main content (sidebars)
<footer> → Bottom section (copyright, contact, footer links)
<div> → A generic, non-semantic container (for layout grouping and styles)
```

### Content & Typography Tags
```html
<h1>Largest Heading</h1>
<h2>Smaller Heading</h2> <!-- h1 to h6 (h6 is smallest) -->
<p>A paragraph of text.</p>
<a href="https://google.com">Click me!</a> <!-- Hyperlink anchor -->
<img src="photo.jpg" alt="My photo"> <!-- Self-closing image tag -->
<ul> <!-- Unordered list (bulleted list) -->
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
<ol> <!-- Ordered list (numbered list) -->
  <li>First</li>
  <li>Second</li>
</ol>
<strong>Bold emphasis text</strong>
<em>Italicized emphasized text</em>
<span>Inline wrapper (non-semantic inline helper)</span>
```

### Form & User Input Tags
```html
<form method="POST" action="/submit">
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" placeholder="you@example.com" required>

  <label for="password">Password:</label>
  <input type="password" id="password" name="password" required>

  <button type="submit">Login</button>
</form>
```

#### Key Form Attributes to Remember:
- **`action`**: Specifies where the form data is sent to the server (the endpoint url).
- **`method`**: Defines the HTTP verb (`GET` or `POST`) used during transmission.
- **`for` & `id`**: The `for` attribute in the `<label>` links with the input's `id`, increasing click area and improving screen reader accessibility.
- **`placeholder`**: Gives users a dynamic input hint.
- **`required`**: Client-side validation ensuring fields are not left blank.

---

## Semantic HTML vs. Generic Divs

Two ways to write navigation links:

```html
<!-- ❌ BAD: Generic div (no meaning) -->
<div class="navigation">
  <div><a href="/">Home</a></div>
  <div><a href="/about">About</a></div>
</div>

<!-- ✅ GOOD: Semantic nav tag (meaningful!) -->
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
```

**Why does it matter?**
- **Accessibility**: Screen readers for blind users know `<nav>` is navigation.
- **SEO**: Search engine crawlers understand structural layout easily.
- **Readability**: Code is significantly cleaner and easier to maintain.

> [!IMPORTANT]
> **Accessibility Rule**: Always add an `alt` attribute to every `<img>` tag. Screen readers read this aloud to visually impaired users. `<img src="cat.jpg" alt="A fluffy orange cat sitting on a chair">` is much better than `<img src="cat.jpg">`.

---

## The HTML Tree (Document Object Model - DOM)

When a browser reads your HTML file, it builds it into a **tree structure** in memory. This is called the **Document Object Model (DOM)**.

```
                                document
                                   │
                                  html
                           ┌───────┴───────┐
                         head            body
                      ┌────┴────┐     ┌────┴────┐
                    title      meta  h1         p
                      │         │     │         │
                  "My Page"  "UTF-8" "Hello"  "Text"
```

Each item in the tree is called a **node**. JavaScript can walk through this tree and change any part of the page in real time:

```javascript
document.getElementById("title").innerText = "Goodbye";
```

This updates the screen **without reloading the page!**

---

## What is a DOM Reflow?

Every time you add, remove, or resize an element, the browser has to **recalculate** where every element on the page goes. This is called a **Reflow**.

```
  [ BEFORE CHANGE ]                           [ AFTER CHANGE (Reflow) ]
  ┌──────────────────────┐                    ┌──────────────────────┐
  │ Box A (top: 10px)    │                    │ Box A (top: 10px)    │
  ├──────────────────────┤                    ├──────────────────────┤
  │ Box B (top: 50px)    │                    │ NEW BOX (top: 50px)  │
  └──────────────────────┘                    ├──────────────────────┤
                                              │ Box B (top: 90px) ◄──┼─ [ Pushed Down! ]
                                              └──────────────────────┘
```

Reflows are computationally expensive. Modern frontend frameworks (like React) use a "Virtual DOM" to batch and execute changes in memory first, minimizing page reflows.

---

## A Complete Real-World HTML Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Profile</title>
</head>
<body>

    <header>
        <h1>Student Portal</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/grades">Grades</a>
            <a href="/logout">Logout</a>
        </nav>
    </header>

    <main>
        <section>
            <h2>Profile: Alice</h2>
            <img src="alice.jpg" alt="Alice's profile photo">
            <p>Roll Number: 21CS001</p>
            <p>Department: Computer Science</p>
        </section>

        <section>
            <h2>Enrolled Courses</h2>
            <ol>
                <li>Modern Application Development (MAD-I)</li>
                <li>Database Systems</li>
                <li>Machine Learning Foundations</li>
            </ol>
        </section>
    </main>

    <footer>
        <p>IIT Madras — Online Degree Program</p>
    </footer>

</body>
</html>
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Tag** | An HTML keyword wrapped in `< >` brackets |
| **Element** | An opening tag + content + closing tag together |
| **Attribute** | Extra information inside a tag (e.g., `href="url"`, `src="image.jpg"`) |
| **DOM** | The tree structure a browser builds from your HTML |
| **Semantic** | Tags that describe MEANING, not just appearance |
| **Reflow** | When the browser recalculates all element positions |
| **Entity** | Special character codes like `&copy;` (©) or `&amp;` (&) |
