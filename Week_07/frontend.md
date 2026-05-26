# Frontend Mechanisms

## What is the "Frontend"?

The **frontend** is everything the user can SEE and TOUCH in a web application. If the backend is the kitchen of a restaurant, the frontend is the dining room — the part that customers actually experience.

Frontend = HTML + CSS + JavaScript running inside the user's browser.

---

## Three Ways to Build a Web Page

Not all web pages are built the same way. There are three major approaches:

### Approach 1: Fully Static Pages

```
  How it works:

  Developer writes HTML file
       │
       ▼ (Uploaded to server, static)
  Browser requests `/index.html`
       │
       ▼ Server sends the EXACT same file to everyone
  Browser displays page

    Pros: Extreme speed (CDN delivery)
          Simple to host (no Python, no database)
          Great security (nothing to hack)

    Cons: Same for everyone (no personalization)
          Hard to update frequently
    Examples: Documentation sites, landing pages

```

### Approach 2: Server-Side Rendering (SSR)

This is what **Flask** does by default!

```
  Browser requests `/students`
       │
       ▼
  Flask runs Python code:
       ┌─────────────────────────────────┐
       │ 1. Query database               │
       │ 2. Fill Jinja2 template with data│
       │ 3. Generate complete HTML       │
       └─────────────────────────────────┘
       │
       ▼ (Personalized HTML page sent back)
  Browser displays page (User-Specific!)

    Pros: Dynamic content per user
          Great for SEO (Google sees full HTML)
          Simpler frontend code

    Cons: Every click = full page reload
          More server load (generates HTML often)
    Examples: Old-school websites, Flask apps

```

### Approach 3: Client-Side Rendering (CSR / SPA)

Modern approach. Used by React, Vue, Angular.

```
  [ FIRST VISIT ]
  Browser requests `/`  ──────>  Server sends tiny HTML + massive JS bundle
                                   │
                                   ▼ JS runs in browser, builds page from scratch

  [ SUBSEQUENT CLICKS ]
  Browser's JS (Fetch API)  ───>  Request only JSON data from Server API
                                   │
                                   ▼ JS updates only the modified UI components (No Reload!)

    Pros: Feels like an app, not a website!
          Very fast AFTER initial load
          Can update small parts without reloading

    Cons: Slow INITIAL load (huge JS bundle)
          SEO is harder (Google may not see data)
    Examples: Gmail, Twitter, Facebook, Notion

```

---

## Asynchronous Updates: AJAX / Fetch API

The **Fetch API** lets JavaScript request data from the server **in the background** without refreshing the page.

```
      [ TRADITIONAL (Full Page Reload) ]              [ MODERN (Asynchronous AJAX Fetch) ]
             User clicks "Like"                              User clicks "Like"
                     │                                               │
                     ▼                                               ▼
        Entire page reloads from server               JavaScript sends background API request
                     │                                 (Page stays fully interactive, no flicker!)
                     ▼                                               │
        Page displays updated like count                             ▼
          (Takes 1-2 seconds, jarring)                 Server updates DB and returns `{ "likes": 101 }`
                                                                     │
                                                                     ▼
                                                       JS updates ONLY the specific counter on screen
                                                                (Done in ~50 milliseconds!)
```

```javascript
// JavaScript Fetch API Example
// When the user clicks "Like":
async function likePost(postId) {
    // Sends a background POST request (page doesn't reload!)
    const response = await fetch(`/api/like/${postId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 42 })
    });

    // Parse the JSON response
    const data = await response.json();

    // Update ONLY the like counter on the page (no reload!)
    document.getElementById('like-count').innerText = data.likes;
}
```

---

## Single Page Applications (SPAs)

An SPA is an app where the browser **loads only once** and then updates the page dynamically:

```
  [ TRADITIONAL MULTI-PAGE WEBSITE ]                [ MODERN SINGLE PAGE APPLICATION (SPA) ]
  Click Home  ──> Browser loads `home.html`         Click Home  ──> JS mounts "Home" component
  Click About ──> Browser loads `about.html`        Click About ──> JS mounts "About" component (Instant!)
                  (FULL Page Reload)                                (No Page Reload!)
  Click Back  ──> Re-requests `home.html`           Click Back  ──> JS mounts "Home" component again (Instant!)
                  (FULL Page Reload)                                (No Page Reload!)
```

[NOTE]
This handbook you're reading RIGHT NOW is an SPA! When you click between topics, the page never reloads — JavaScript updates only the content pane. Check the network tab in your browser's developer tools to see the fetch calls!
[/CALLOUT]

---

## WebAssembly (WASM): Bringing Native Performance to the Web

JavaScript is powerful but not the fastest. **WebAssembly** allows other languages (like C++, Rust, Go) to run in the browser at near-native CPU speed.

```
  [ Traditional JS Pipeline ]
  JavaScript Code  ──────>  Interpreted by JS Engine  ──────>  10x slower than native execution

  [ WebAssembly Pipeline ]
  C++ / Rust / Go  ──────>  Compiled to WASM Binary   ──────>  Executes at near-native CPU speed!
```

Use cases:
- Video editing in the browser (like Figma's canvas engine)
- 3D games running in the browser (Doom, Unity games)
- Image processing (like Photoshop on the web)

---

## Browser Security: The Sandbox

Your browser runs JavaScript from ANY website. Without restrictions, a malicious website could:
- Read your files
- Access your webcam
- Contact other websites as you

The **Sandbox** prevents this:

```

  ┌────────────────────────────────────────────────────────────────────────┐
  │                            BROWSER SANDBOX                             │
  ├────────────────────────────────────────────────────────────────────────┤
  │  [ JavaScript & WebAssembly execution space ]                          │
  │                                                                        │
  │  ✅ ALLOWED ACTIONS:                                                   │
  │  • Read and write the web page DOM tree dynamically                    │
  │  • Make asynchronous fetch/network requests (CORS-compliant)           │
  │  • Read/write to client storage (localStorage, cookies)                │
  │                                                                        │
  │  ❌ RESTRICTED ACTIONS:                                                │
  │  • Cannot read or write local OS files directly                        │
  │  • Cannot send requests to external domains without CORS permission    │
  │  • Cannot access client cameras, mics, or hardware without prompting   │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
             [ Your OS, local filesystem, and private data are SAFE ]

```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Frontend** | The part of the app users see and interact with (HTML, CSS, JS) |
| **Backend** | The server-side logic that powers the frontend |
| **SSR** | Server-Side Rendering — HTML is built on the server |
| **CSR** | Client-Side Rendering — HTML is built in the browser by JavaScript |
| **SPA** | Single Page Application — page never reloads; JS swaps content |
| **AJAX** | Asynchronous JavaScript — fetch data in background without page reload |
| **Fetch API** | Modern JavaScript method for making async HTTP requests |
| **WASM** | WebAssembly — runs C++/Rust in the browser at near-native speed |
| **Sandbox** | A restricted environment where browser code runs safely |
| **CDN** | Content Delivery Network — serves static files from a server near you |
