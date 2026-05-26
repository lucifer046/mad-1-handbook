# Information Representation

## The Big Question: How do Computers "Know" Anything?

Computers are just machines made of electronic switches. Each switch has only **two states**: ON or OFF.

We write this as:
- **1** = ON (electricity is flowing)
- **0** = OFF (no electricity)

This is called **binary** — the language of all computers.

Everything you do on a computer — typing a letter, watching a video, clicking a button — is ultimately converted into a series of 0s and 1s and back again.

---

## Understanding Binary Numbers

Our normal counting system uses **10 digits** (0-9). We call this **base-10** (or decimal).

Computers count using only **2 digits** (0 and 1). This is **base-2** (or binary).

### How to Read Binary

Think of it like light switches in a row. Each switch represents a **power of 2**:

```
Switch position: 8th 7th 6th 5th 4th 3rd 2nd 1st
Power of 2: 128 64 32 16 8 4 2 1
Binary (6): 0 0 0 0 0 1 1 0
                                               | |
                                               4 + 2 = 6
```

So **6 in binary is `110`** because: 4 + 2 = 6

### Let's Convert Step by Step

Convert the number **13** to binary:
```
13 ÷ 2 = 6 remainder 1 → Write down: 1
 6 ÷ 2 = 3 remainder 0 → Write down: 0
 3 ÷ 2 = 1 remainder 1 → Write down: 1
 1 ÷ 2 = 0 remainder 1 → Write down: 1

Read remainders BOTTOM to TOP: 1101

CHECK: 1×8 + 1×4 + 0×2 + 1×1 = 8 + 4 + 0 + 1 = 13
```

---

## Negative Numbers: Two's Complement

How does a computer store **-6**? It can't write a minus sign! It uses a clever trick called **Two's Complement**.

```
Step 1: Start with +6 in binary (using 4 bits):
        0110

Step 2: FLIP every bit (0 becomes 1, 1 becomes 0):
        1001 ← This is called "one's complement"

Step 3: ADD 1 to the result:
        1001
      + 1
        ----
        1010 ← This is -6 in Two's Complement!
```

**Why is this clever?** If you add `0110` (6) and `1010` (-6) together, you get `0000` (0). It works mathematically!

---

## Text Encoding: Turning Letters into Numbers

A computer can only store numbers. So how does it store the letter **'A'**?

Simple: We agree on a **table** that maps every letter to a number. This is called **encoding**.

### Stage 1: ASCII (1963) — The First Table

ASCII (American Standard Code for Information Interchange) was the first widely used encoding.

```
     Character → Number → Binary
     --------- ------ ------
       'A' → 65 → 01000001
       'B' → 66 → 01000010
       'a' → 97 → 01100001
       '0' → 48 → 00110000
       ' ' (space) → 32 → 00100000
```

So the word "Hi" is stored as: `72 105` (or in binary: `01001000 01101001`)

**Problem with ASCII**: It only had 128 characters — perfect for English, but what about Hindi, Chinese, Arabic, or emoji?

### Stage 2: Unicode — One Table for EVERY Language

Unicode assigns a unique **code point** (a number) to every character in every language in the world.

```
  'A' → U+0041 (English)
  'ñ' → U+00F1 (Spanish)
  'भ' → U+092D (Hindi - Devanagari)
  '' → U+4E2D (Chinese)
  '😀' → U+1F600 (Emoji!)
```

Unicode can represent over **1 million** different characters!

### Stage 3: UTF-8 — The Smart Way to Store Unicode

Unicode defines the code points, but how do we store them efficiently?

UTF-8 is **variable length** — simple characters (like English letters) use fewer bytes, complex ones use more:

```
  1 byte = for basic English (A-Z, 0-9) [Backward compatible with ASCII!]
  2 bytes = for accented characters (ñ, ü)
  3 bytes = for most Asian scripts (Chinese, Japanese, Hindi)
  4 bytes = for rare symbols and emojis (😀)
```

**Why is this brilliant?** An English website doesn't waste space. But it can still include a Chinese character when needed!

```
                    UTF-8 Byte Layout

    Bytes Bit Pattern Code Points

     1 0xxxxxxx U+0000-U+007F
     2 110xxxxx 10xxxxxx U+0080-U+07FF
     3 1110xxxx 10xxxxxx 10xxxxxx U+0800-U+FFFF
     4 11110xxx 10xxxxxx 10xxxxxx ... U+10000+

  (The 'x' positions are where the actual character bits go)
```

[TIP]
**UTF-8 is the default for the web!** If you save an HTML file and want to include any international characters or emoji, always add this in your `<head>` tag: `<meta charset="UTF-8">`. It tells the browser which encoding to use.
[/CALLOUT]

---

## Markup vs. Style: Two Different Jobs

When you look at a webpage, two completely different systems are working together:

```
+-----------------------------------------+
| A WEBPAGE IS BUILT WITH: |
+-----------------------------------------+
| |
| MARKUP (HTML) STYLE (CSS) |
| |
| "This is a title" "Make the |
| "This is a list" title red" |
| "This is a link" "Make the |
| list smaller" |
| Describes MEANING Describes |
| and STRUCTURE APPEARANCE |
+-----------------------------------------+
```

Think of markup as the **skeleton** of a body and CSS as the **clothes and makeup**. The skeleton defines what's there; the clothes define how it looks.

---

## Summary

```
All data → Converted to BINARY (0s and 1s)
                    ↓
Numbers → Binary directly (Two's complement for negatives)
                    ↓
Text → ASCII table (English only, 128 chars)
                    ↓
Text → Unicode (every language, 1M+ chars)
                    ↓
Storage → UTF-8 (smart, variable-length encoding)
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Bit** | A single 0 or 1 — the smallest unit of data |
| **Byte** | 8 bits grouped together |
| **Encoding** | A system for turning characters into numbers |
| **ASCII** | The original 128-character English encoding table |
| **Unicode** | The universal standard with code points for every character |
| **UTF-8** | The most popular way to store Unicode on the web |
| **Endianness** | The order bytes are stored (Big-endian: most important byte first; Little-endian: least important byte first) |
