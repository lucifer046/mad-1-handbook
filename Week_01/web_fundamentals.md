# Web Fundamentals

## How Does the Internet Actually Work?

Imagine you want to send a letter to your friend in another city.

1. You write the letter and put it in an **envelope**
2. You write your friend's **address** on the envelope
3. The **post office** figures out the best route to deliver it
4. Multiple **trucks and planes** carry parts of the letter (yes, like puzzle pieces!)
5. Your friend receives all pieces and **reassembles** the letter

The internet works almost exactly like this! This system of splitting data into pieces and routing them is called **Packet Switching**.

---

## The Old Way vs. The New Way

### Old Way: Circuit Switching (Like Telephone Calls)

```
Before the call: A phone wire is PHYSICALLY connected between You and Your Friend
During the call: Only YOU and your friend can use that wire
After the call: The wire is "released" for others to use
```

**Problem**: Massively wasteful. If 1 million people call at once, you need 1 million separate physical wires!

### New Way: Packet Switching (How the Internet Works)

```
Your message: "Hello, how are you?"

Split into packets:
  [Packet 1: "Hello,"] → Route via Australia
  [Packet 2: " how"] → Route via Europe
  [Packet 3: " are"] → Route via USA
  [Packet 4: " you?"] → Route via Africa

All arrive and are reassembled in order: "Hello, how are you?"
```

**Advantage**: The network can use ALL routes at the same time. Super efficient!

---

## The Rules of the Internet: TCP/IP

For all these packets to work, computers need to agree on rules. These rules are called **protocols**.

### IP (Internet Protocol) — The Addressing System

Every device on the internet has a unique **IP address** — just like a home address.

```
  Your Home Address: Your IP Address:
  "42, MG Road, "192.168.1.105"
   Bengaluru, 560001"
```

IP's job: Put the correct **destination address** on every packet.

### TCP (Transmission Control Protocol) — The Post Office That Guarantees Delivery

TCP sits on top of IP and makes sure all your packets arrive:
- **In the correct order** (Packet 1 before Packet 4)
- **All of them** (if any packet is lost, TCP asks for it to be resent)
- **Without corruption** (it checks each packet like a seal on a letter)

### TCP vs UDP — When to Guarantee vs. When to Risk It

| | TCP | UDP |
|:---|:---|:---|
| **Analogy** | Registered Post — guaranteed delivery | Regular Post — no tracking |
| **Reliability** | Yes, retransmits lost packets | No, packets can be dropped |
| **Speed** | Slower (waits for confirmation) | Faster (no waiting) |
| **Use For** | Loading webpages, emails, banking | Video calls, live gaming, streaming |

[NOTE]
**Why use UDP for video calls?** If you're on a Zoom call and one packet gets lost, it's better to skip that tiny blip of audio than to freeze the entire call waiting for a resend. Speed matters more than perfection here!
[/CALLOUT]

---

## What Happens When You Type a URL?

Let's trace every step of what happens when you type `http://example.com` and press Enter.

```
     YOU (Browser)                 DNS SERVER            WEB SERVER (93.184.216.34)
          │                            │                          │
          │ 1. Type URL                │                          │
          │                            │                          │
          │ 2. "What is the IP for     │                          │
          │     example.com?"          │                          │
          ├───────────────────────────>│                          │
          │                            │                          │
          │ 3. "It's 93.184.216.34"    │                          │
          │<───────────────────────────┤                          │
          │                            │                          │
          │ 4. Send HTTP GET           │                          │
          ├────────────────────────────┼─────────────────────────>│
          │                            │                          │
          │ 5. Send back HTML code     │                          │
          │<───────────────────────────┼──────────────────────────┤
          │                            │                          │
          │ 6. Render webpage on screen│                          │
          ▼                            ▼                          ▼
```

### What is DNS?

DNS (Domain Name System) is the **phonebook of the internet**.

- You remember names (`google.com`), not phone numbers (`142.250.195.110`)
- DNS translates the name into a number (IP address) that computers understand
- Without DNS, you'd have to memorize IP addresses for every website!

---

## HTTP: The Language of the Web

When your browser and the server talk to each other, they use **HTTP** (HyperText Transfer Protocol). Think of it as the **language** they both agree to speak.

### HTTP is Stateless

Here is a very important quirk:

```
Request 1: Browser → "Give me the homepage"
Server: Server → "Here it is. *Server forgets this interaction*"

Request 2: Browser → "I am Alice, remember me?"
Server: Server → "Who are you? I don't know you."
```

The server has **amnesia** after every response! This is called being **stateless**. The server does not remember who it talked to. This is why websites need **login sessions and cookies** — they're a workaround for this amnesia.

[WARNING]
Statelessness is not a bug — it's a feature! It means the server doesn't waste memory tracking millions of users. But it also means WE must build login/session systems ourselves.
[/CALLOUT]

### HTTP Request Methods (Verbs)

When you talk to a server, you tell it *what you want to do* using a **method**:

| Method | Real-World Analogy | When Used |
|:---|:---|:---|
| **GET** | "Give me the menu" — read only | Loading any webpage |
| **POST** | "I want to order this item" — creates new data | Login forms, sign-up forms |
| **PUT** | "Change my order completely" — replaces data | Editing your profile |
| **DELETE** | "Cancel my order" — removes data | Deleting an account |

### HTTP Status Codes

When the server responds, it includes a **status code** — a 3-digit number that tells you if things went well:

```
2xx = ✅ SUCCESS
  200 OK → Everything worked perfectly
  201 Created → Your new resource was created

3xx = ↩ REDIRECT
  301 Moved → Page has a new address, go there

4xx = ❌ CLIENT ERROR (Something YOU did was wrong)
  400 Bad Request → You sent garbage data
  401 Unauthorized → You need to log in first
  403 Forbidden → You are logged in but not allowed here
  404 Not Found → This page doesn't exist

5xx = SERVER ERROR (Something the SERVER did was wrong)
  500 Internal Error → The server's code crashed
```

---

## Making an HTTP Request with Python

You can write Python code that acts **exactly like a browser** and makes HTTP requests:

```python
import requests # Install with: pip install requests

# ---- Step 1: Send a GET request (like typing a URL in your browser) ----
response = requests.get('https://api.github.com')

# ---- Step 2: Check if it was successful ----
# Status 200 means "OK, everything worked!"
if response.status_code == 200:
    print("SUCCESS! Connected to GitHub API")

    # ---- Step 3: Read the data (it comes as JSON) ----
    data = response.json()
    print("Current User URL:", data['current_user_url'])
else:
    print(f"FAILED. Server returned code: {response.status_code}")
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Protocol** | A set of rules that computers agree to follow for communication |
| **DNS** | Domain Name System — translates names like "google.com" to IP addresses |
| **IP Address** | The unique "home address" of every device on the internet |
| **Port** | A virtual "door number" on a computer (HTTP uses port 80, HTTPS uses 443) |
| **RTT** | Round-Trip Time — how long it takes for a packet to go and come back |
| **Packet** | A small chunk of data. Big messages are split into many packets |
