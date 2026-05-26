## Project Structure
```text
experiment1/
 bootstrap_test.html
 index.html
 jnanpith.html
 style.css
```

---

# Experiment 01: Frontend Basics
This experiment covers the foundational structure of a web page using HTML and styling with CSS.

## Detailed Code Breakdown

### 1. HTML Structure (`jnanpith.html`)
* `<!DOCTYPE html>`: Tells the browser that this is an HTML5 document.
* `<link rel="stylesheet" href="style.css">`: Links our external CSS file so the styles are applied to this page.
* `<table>, <thead>, <tbody>`: Uses semantic HTML to structure data into a readable grid.

### 2. CSS Styling (`style.css`)
* `border-collapse: collapse`: Ensures that table cells share a single border instead of having double lines.
* `tr:nth-child(even)`: A "pseudo-class" used for Zebra-striping. It automatically colors every second row to improve readability of large tables.
* `text-align: center`: Ensures that all data within the table is perfectly aligned in the middle of each cell.

### 3. Bootstrap Integration (`bootstrap_test.html`)
* This file demonstrates how to include an external framework (Bootstrap) via a CDN (Content Delivery Network). This gives us access to pre-built components like navbars and grids without writing custom CSS.
