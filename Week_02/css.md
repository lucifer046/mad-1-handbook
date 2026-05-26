# CSS: Styling Your Webpage

## What is CSS?

If HTML is the **skeleton** of a webpage, then CSS is the **skin, clothes, and hairstyle**.

CSS (Cascading Style Sheets) controls:
- **Colors** (background, text, borders)
- **Fonts** (size, weight, family)
- **Spacing** (margins, padding)
- **Layout** (how elements are positioned)
- **Animations** (transitions, hover effects)

Without CSS, every webpage would look like a plain text document!

---

## How CSS Connects to HTML

You write CSS rules in a separate file (e.g., `styles.css`) and link it to your HTML:

```html
<head>
  <link rel="stylesheet" href="styles.css">
</head>
```

A CSS rule looks like this:

```
       selector
          ↓
        h1 {
            color: blue; ← property: value
            font-size: 2rem; ← each rule ends with ;
        }
        ↑ ↑
     opening closing
     brace brace
```

This rule says: **"Find ALL `<h1>` tags and make them blue, size 2rem."**

---

## Selectors: How to Target Elements

Selectors tell CSS **which HTML elements to style**.

```css
/* 1. TAG selector - targets ALL elements of that type */
h1 { color: red; } /* Every h1 on the page goes red */
p { font-size: 1rem; } /* Every paragraph on the page */

/* 2. CLASS selector - targets elements with that class */
.warning-text { color: orange; } /* <p class="warning-text"> */
.big-button { padding: 1rem; } /* <button class="big-button"> */

/* 3. ID selector - targets ONE specific element */
#main-title { font-size: 3rem; } /* <h1 id="main-title"> */

/* 4. PSEUDO-CLASS - targets a specific STATE of an element */
a:hover { color: purple; } /* When mouse hovers over a link */
input:focus { border: 2px solid blue; } /* When you click inside an input */

/* 5. Combining selectors */
nav a { text-decoration: none; } /* Links INSIDE a nav, not all links */
```

[NOTE]
**Specificity**: IDs (`#id`) are more specific than classes (`.class`), which are more specific than tags (`h1`). When two rules conflict, the more specific one wins!
[/CALLOUT]

---

## The Cascade: Who Wins When Rules Conflict?

The "Cascading" in CSS means there's a priority system:

```
  ┌─────────────────────────────────────────────────────────────┐
  │              THE CSS CASCADE SPECIFICITY RANK               │
  ├─────────────────────────────────────────────────────────────┤
  │  🥇 1. Inline CSS      e.g., <h1 style="color: red;">       │ (Highest - WINS)
  │  🥈 2. Internal CSS    e.g., <style>h1 {color: blue;}</style>│
  │  🥉 3. External CSS    e.g., linked styles.css file         │
  │  🪫 4. Browser Default e.g., user agent default stylesheet   │ (Lowest - Loses)
  └─────────────────────────────────────────────────────────────┘

```

If two rules have the SAME priority, the one written LATER in the file wins:

```css
/* This applies first... */
h1 { color: blue; }

/* ...but this comes later, so it WINS */
h1 { color: red; } /* h1 will be RED */
```

---

## The Box Model: Every Element is a Box

This is the single most important concept in CSS layout. **EVERY element on a webpage is a rectangular box**, made of 4 layers:

```

  ┌─────────────────────────────────────────────────────────┐
  │  MARGIN (Space between elements)                        │
  │    ┌───────────────────────────────────────────────┐    │
  │    │  BORDER (The visible edge line)               │    │
  │    │    ┌─────────────────────────────────────┐    │    │
  │    │    │  PADDING (Space inside border)      │    │    │
  │    │    │    ┌───────────────────────────┐    │    │    │
  │    │    │    │  CONTENT                  │    │    │    │
  │    │    │    │  (Text, Images, Elements) │    │    │    │
  │    │    │    └───────────────────────────┘    │    │    │
  │    │    └─────────────────────────────────────┘    │    │
  │    └───────────────────────────────────────────────┘    │
  └─────────────────────────────────────────────────────────┘




```

```css
div {
    /* Content is sized by width/height */
    width: 200px;
    height: 100px;

    /* Padding: space inside the border */
    padding: 20px; /* 20px on ALL sides */
    padding: 10px 20px; /* 10px top/bottom, 20px left/right */

    /* Border: the visible edge */
    border: 2px solid black; /* thickness | style | color */
    border-radius: 10px; /* Rounds the corners! */

    /* Margin: space outside the border */
    margin: 30px; /* 30px on ALL sides */
    margin: 0 auto; /* 0 top/bottom, auto left/right = CENTER! */
}
```

[TIP]
**Pro Tip — Use `box-sizing: border-box`**: By default, when you set `width: 200px` and then add `padding: 20px`, the element becomes `240px` wide! To avoid this confusing math, add this to the top of your CSS:
```css
* { box-sizing: border-box; }
```
Now `width: 200px` INCLUDES padding and border. Much more predictable!
[/CALLOUT]

---

## Modern Layout Systems

### Flexbox: 1D Layout (a single row OR column)

Flexbox is perfect for aligning items in a **row** or **column**:

```
  [ WITHOUT FLEXBOX (Block Stack) ]             [ WITH FLEXBOX (Row Alignment) ]
  ┌────────┐                                    ┌────────┐ ┌────────┐ ┌────────┐
  │ Box 1  │                                    │ Box 1  │ │ Box 2  │ │ Box 3  │
  ├────────┤                                    └────────┘ └────────┘ └────────┘
  │ Box 2  │
  ├────────┤
  │ Box 3  │
  └────────┘
```

```css
.container {
    display: flex; /* Turn on Flexbox */
    flex-direction: row; /* Items go left to right (default) */
    justify-content: center; /* Center items horizontally */
    align-items: center; /* Center items vertically */
    gap: 1rem; /* Space between items */
}
```

### Grid: 2D Layout (rows AND columns together)

Grid is perfect for full page layouts:

```css
.page-layout {
    display: grid;
    grid-template-columns: 250px 1fr; /* Sidebar | Main Content */
    grid-template-rows: 80px 1fr; /* Header | Body */
}
```

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                       HEADER (height: 80px)                             │
  ├─────────────────────────────────┬───────────────────────────────────────┤
  │            SIDEBAR              │             MAIN CONTENT              │
  │         (width: 250px)          │            (width: 1fr)               │
  │                                 │                                       │
  │                                 │                                       │
  └─────────────────────────────────┴───────────────────────────────────────┘
```

### Responsive Design with Media Queries

Your webpage should look good on **phones, tablets, AND desktops**. Media queries let you change styles based on screen size:

```css
/* Default: desktop styles */
.container {
    width: 1200px;
    display: grid;
    grid-template-columns: 250px 1fr;
}

/* When screen is smaller than 768px (tablet/phone): */
@media (max-width: 768px) {
    .container {
        width: 100%; /* Full width */
        grid-template-columns: 1fr; /* Single column, no sidebar */
    }
}
```

---

## Colors in CSS

CSS supports many ways to specify colors:

```css
h1 {
    color: red; /* Named color */
    color: #FF5733; /* Hex code (most common) */
    color: rgb(255, 87, 51); /* RGB values (0-255) */
    color: rgba(255, 87, 51, 0.5); /* With 50% transparency */
    color: hsl(14, 100%, 60%); /* Hue, Saturation, Lightness */
}
```

---

## CSS Variables (Custom Properties)

Instead of repeating the same color 50 times, define it once and reuse it:

```css
/* Define variables at the root level */
:root {
    --primary-color: #1e5a8f;
    --text-color: #333333;
    --border-radius: 8px;
}

/* Use them anywhere */
button {
    background: var(--primary-color);
    border-radius: var(--border-radius);
}

h1 {
    color: var(--text-color);
}
```

This handbook itself uses CSS variables! (Check `book/style.css`)

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Selector** | The part of a CSS rule that picks which elements to style |
| **Property** | What you want to change (color, font-size, margin) |
| **Value** | How you want to change it (red, 1rem, 20px) |
| **Cascade** | The priority system that decides which rule wins when there's a conflict |
| **Box Model** | The concept that every element is a box with content, padding, border, margin |
| **Flexbox** | CSS system for 1D layouts (rows or columns) |
| **Grid** | CSS system for 2D layouts (rows AND columns) |
| **Media Query** | A CSS rule that only applies at certain screen sizes |
| **Hex Code** | A color written in hexadecimal (e.g., `#FF5733`) |
