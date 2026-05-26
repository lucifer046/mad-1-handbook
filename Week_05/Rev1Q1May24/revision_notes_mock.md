# Revision Notes & Mock Quiz-1 Problems

## Part 1: Quick Revision Reference

### 1. Data Size & Encodings
*   **Formula**: $\text{Storage Size} = \text{Character Count} \times \text{Bits per Character}$
*   **Standard Encodings**:
    *   **7-bit ASCII**: Each character is represented by 7 bits (e.g., `'A'` is decimal 65, binary `1000001`).
    *   **8-bit ASCII**: Extended ASCII using 8 bits (1 byte) per character.
    *   **UCS-2**: Fixed-width 2 bytes (16 bits) per character, covering the Basic Multilingual Plane.
    *   **UCS-4**: Fixed-width 4 bytes (32 bits) per character.
    *   **UTF-8**: Variable-width encoding using 1 to 4 bytes per character, backward-compatible with 7-bit ASCII.

---

### 2. Network Calculations & Unit Conversions
*   **Formula**: $\text{Bandwidth Requirement} = \text{Request Count per Second} \times \text{Size of Single Request}$
*   **Unit Balance (Bits vs. Bytes)**:
    *   $1 \text{ Byte} = 8 \text{ bits}$
    *   $1 \text{ Mbps} = \frac{1}{8} \text{ MBps} = 0.125 \text{ Megabytes per second}$
    
    ```javascript
    // Example: Calculate total megabytes transferred
    let Mbps = 100; // Megabits per second
    let timeInSeconds = 10;
    let totalDataInMegabits = Mbps * timeInSeconds; // 1000 Mb
    let totalDataInMegabytes = totalDataInMegabits / 8; // 125 MB
    console.log(`Total data: ${totalDataInMegabytes} MB`);
    ```

---

### 3. Styling & Selectors (HTML/CSS)
*   **Embedding Styles**:
    *   **Inline CSS**: `<p style="color: red;">Red Text</p>`
    *   **Internal CSS**: `<style>p { color: blue; }</style>`
    *   **External CSS**: `<link rel="stylesheet" href="styles.css">`
*   **CSS Selectors**:
    *   **ID Selector**: `#myDiv { color: red; }` (target uniquely via `<div id="myDiv">`)
    *   **Class Selector**: `.myClass { color: green; }` (target repeatedly via `<div class="myClass">`)

---

### 4. Template Engines (Python)
*   **Python `string.Template`**:
    ```python
    from string import Template
    t = Template('Hello, $name!')
    # substitute() raises KeyError if variable is missing
    print(t.substitute(name='Ravi')) # "Hello, Ravi!"
    
    # safe_substitute() retains placeholder if variable is missing
    print(t.safe_substitute()) # "Hello, $name!"
    ```
*   **Jinja2 Templates**:
    ```python
    from jinja2 import Template
    template = Template('Hello {{ name }}!')
    print(template.render(name='Ravi')) # "Hello Ravi!"
    ```

---

### 5. HTML Display Properties
*   **Inline**: Elements do not start on a new line and only take as much width as necessary (e.g., `<span>`, `<a>`, `<img>`).
*   **Block**: Elements start on a new line and stretch to fill the container width (e.g., `<div>`, `<p>`, `<h1>`).
*   **Inline-Block**: Elements sit inline like text but allow custom width and height specifications.

---

### 6. MVC Architecture & Web Operations
*   **Model**: Represents the structural schema and manages business logic and database interactions.
*   **View**: Handles layout template presentation and UI rendering for clients.
*   **Controller**: Binds Models and Views together, handling request routing and coordinating state.
*   **cURL Operations**:
    *   `curl -I <URL>`: Fetches only the response headers (HEAD method).
    *   `curl -X GET <URL>`: Fetches both the header and response body (GET method).
    *   `curl -X POST <URL> -d '{"key":"value"}' -H "Content-Type: application/json"`: Submits a POST request with payload data.

---

## Part 2: Mock Quiz-1 Problems & Solutions

### Problem 1 (Encoding Calculation)
**Question:** Let $L = \{'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D', '0', '1', ' '\}$ be a complete character set. If a document that uses fixed encoding for all characters is created using the character set $L$ and has a disk size of 2 Kilobytes, the number of characters in the document would be_______. 
*(Take 1 Byte = 8 bits, 1 KB = 1000 Bytes, 1 MB = 1000 Kilobytes and so on.)*

**Solution:**
1. The character set $L$ contains **11** unique characters.
2. To represent 11 distinct states, we need **4 bits** per character (since $2^4 = 16$ is the smallest power of 2 greater than or equal to 11).
3. The document size is **2 KB**, which equals **2000 Bytes**.
4. Since each byte contains 8 bits, the document size in bits is:
   $$2000 \text{ Bytes} \times 8 \text{ bits/Byte} = 16,000 \text{ bits}$$
5. Since each character takes exactly 4 bits, the character capacity is:
   $$\frac{16,000 \text{ bits}}{4 \text{ bits/char}} = 4000 \text{ characters}$$

**Answer:** **4000** characters.

---

### Problem 2 (Character Bounds with 5 Bits)
**Question:** How many unique characters can be encoded using 5 bits?

**Solution:**
Using $N$ bits, we can represent $2^N$ distinct states:
$$2^5 = 32$$

**Answer:** **32**

---

### Problem 3 (ASCII Representation Calculation)
**Question:** How many bits are required to represent 'IITM' in ASCII?

**Solution:**
1. Each standard ASCII character requires exactly 1 byte (**8 bits**).
2. The string `'IITM'` contains exactly **4 characters**.
3. Total bits required:
   $$4 \text{ characters} \times 8 \text{ bits/character} = 32 \text{ bits}$$

**Answer:** **32** bits.

---

### Problem 4 (Cruising Mobile Bandwidth Data Consumption)
**Question:** A mobile client starts from and is cruising away continuously at 60 kmph from a network tower whose network range is 40 km and bandwidth is 120 Mbps. How much data (in Gigabytes) will be consumed by the client who is continuously using the entire bandwidth before completely moving out of the network?
*(Take 1 Byte = 8 bits, 1 KB = 1000 Bytes, 1 MB = 1000 Kilobytes and so on. Consider the speed of light in air to be $3 \times 10^8$ m/sec.)*

**Solution:**
1. **Calculate Time in Network**:
   The client travels at 60 km/h and must cover a radius of 40 km before leaving signal range:
   $$\text{Time } (t) = \frac{\text{Distance}}{\text{Speed}} = \frac{40 \text{ km}}{60 \text{ km/h}} = \frac{2}{3} \text{ hours}$$
   Convert to seconds:
   $$t = \frac{2}{3} \times 3600 \text{ seconds} = 2400 \text{ seconds}$$

2. **Calculate Total Data Transmitted**:
   The full bandwidth of 120 Mbps is used for 2400 seconds:
   $$\text{Total Megabits} = 120 \text{ Mbps} \times 2400 \text{ seconds} = 288,000 \text{ Mb}$$

3. **Convert to Gigabytes (GB)**:
   Convert Megabits to Megabytes (MB) by dividing by 8:
   $$\text{Total Megabytes (MB)} = \frac{288,000 \text{ Mb}}{8} = 36,000 \text{ MB}$$
   Convert Megabytes to Gigabytes (GB) using $1 \text{ GB} = 1000 \text{ MB}$:
   $$\text{Total Gigabytes (GB)} = \frac{36,000 \text{ MB}}{1000} = 36 \text{ GB}$$

**Answer:** **36** GB.
