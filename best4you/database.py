import sqlite3
import hashlib
import secrets

DB_PATH = 'best4you.db'

def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            username TEXT    NOT NULL UNIQUE,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            salt     TEXT    NOT NULL,
            joined   TEXT    DEFAULT (DATE('now'))
        )
    ''')

    # Posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            category   TEXT    NOT NULL,
            tags       TEXT    DEFAULT '',
            created_at TEXT    DEFAULT (DATETIME('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialised successfully.")
    seed_data()


def seed_data():
    """Insert sample users and posts only if the DB is empty."""
    conn = get_db()
    existing = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    conn.close()
    if existing > 0:
        return  # Already seeded — don't add duplicates

    # ── Seed Users ────────────────────────────────────────────
    sample_users = [
        ('Aarav Kumar',  'aarav_k',  'aarav@college.edu',  'pass123'),
        ('Sneha Rao',    'sneha_r',  'sneha@college.edu',  'pass123'),
        ('Priya Mehta',  'priya_m',  'priya@college.edu',  'pass123'),
        ('Rohan Joshi',  'rohan_j',  'rohan@college.edu',  'pass123'),
        ('Demo User',    'demo',     'demo@college.edu',   'demo123'),
    ]
    user_ids = {}
    for name, username, email, password in sample_users:
        ok, uid = create_user(name, username, email, password)
        if ok:
            user_ids[username] = uid

    # ── Seed Posts ────────────────────────────────────────────
    sample_posts = [
        (
            user_ids.get('aarav_k', 1),
            'Mastering Dynamic Programming — A Beginner\'s Complete Guide',
            '''Dynamic Programming (DP) is one of the most powerful techniques in competitive programming and technical interviews. Once you understand the core idea, it unlocks solutions to hundreds of problems.

What is Dynamic Programming?
DP is about breaking a problem into smaller overlapping subproblems, solving each once, and storing the result to avoid redundant work.

Two main approaches:
1. Memoization (Top-Down) — Recursion + cache. Start from the big problem and break it down.
2. Tabulation (Bottom-Up) — Fill a table iteratively from the base case upward.

Key DP Patterns to Learn:
- Fibonacci / Climbing Stairs (basic intro)
- 0/1 Knapsack (classic resource allocation)
- Longest Common Subsequence (string problems)
- Coin Change (unbounded knapsack variant)
- Matrix Chain Multiplication (interval DP)

My Study Plan:
Week 1: Fibonacci, Climbing Stairs, House Robber
Week 2: 0/1 Knapsack, Subset Sum, Partition Equal Subset
Week 3: LCS, Edit Distance, Longest Palindromic Subsequence
Week 4: Mixed hard problems from LeetCode

Practice at least 3 DP problems daily and you'll crack most interview DP questions within a month!''',
            'coding',
            'DSA, LeetCode, DP, Python',
        ),
        (
            user_ids.get('sneha_r', 2),
            'How I Got Placed at Google After 3 Rejections',
            '''Getting rejected from Google three times was one of the hardest experiences of my life. Each rejection email felt like a door slamming shut. But looking back, every failure taught me exactly what I needed to fix.

Rejection #1 — Poor Problem Communication
I was solving problems but not explaining my thought process. The interviewer had no idea how I was thinking. Lesson: Always think aloud.

Rejection #2 — Weak System Design
I hadn't prepared system design at all. I stumbled through designing a URL shortener and it showed. Lesson: Practice HLD/LLD seriously, not as an afterthought.

Rejection #3 — Behavioral Round Failure
I panicked. I gave vague answers. I didn't use the STAR method. Lesson: Prepare 10–12 strong behavioral stories in advance.

What I Did Differently for Round 4:
✅ Solved 280+ LeetCode problems (60% medium, 30% hard)
✅ Completed 40+ mock system design sessions with a friend
✅ Recorded myself answering behavioral questions and reviewed the recordings
✅ Found a mentor who had cracked Google and did weekly 1:1s

The Result: L4 SWE offer, 42 LPA.

Don't give up. Rejection is just redirection.''',
            'placement',
            'Google, FAANG, Placement, SWE',
        ),
        (
            user_ids.get('priya_m', 3),
            'The STAR Method Decoded — Ace Every Behavioral Interview',
            '''Behavioral interviews trip up even the most technically strong candidates. "Tell me about a time you failed" — and suddenly the brilliant coder goes blank.

The STAR Method is your framework:
S — Situation: Set the context briefly
T — Task: What was your responsibility?
A — Action: What did YOU specifically do? (Most important part)
R — Result: Quantify the outcome if possible

Example Question: "Tell me about a time you dealt with a difficult team member."

Weak Answer: "My teammate wasn't doing his work so I talked to him."

STAR Answer:
Situation: During my 3rd year project, our 4-member team had a member consistently missing deadlines, putting our submission at risk.
Task: As the informal team lead, I needed to address this without damaging team morale.
Action: I had a private, non-confrontational 1:1 with him. I discovered he was overwhelmed with backlogs from other subjects. I redistributed tasks to play to everyone's strengths and set up daily 10-minute syncs.
Result: We submitted on time, received an A grade, and the teammate later thanked me for the approach.

Top 10 Behavioral Questions to Prepare:
1. Tell me about a time you failed
2. Describe a conflict with a teammate
3. Tell me about a challenging project
4. How did you handle a tight deadline?
5. Describe a time you showed leadership
6. Tell me about a time you influenced without authority
7. Describe a time you received critical feedback
8. Tell me about an innovative solution you built
9. Describe a time you prioritized competing deadlines
10. Tell me about your biggest achievement

Prepare 2–3 strong stories that you can adapt to answer most of these!''',
            'interview',
            'Behavioral, STAR, Interview Prep, Soft Skills',
        ),
        (
            user_ids.get('rohan_j', 4),
            'How React\'s Virtual DOM Works — Explained Simply',
            '''React is everywhere, but most students use it without truly understanding what makes it fast. Let's fix that.

The Problem with Direct DOM Manipulation
The browser's DOM is slow to update. Every time you change it, the browser may re-layout and repaint large portions of the screen. Doing this frequently (e.g., on every keystroke) makes apps feel sluggish.

What is the Virtual DOM?
The Virtual DOM (VDOM) is a lightweight JavaScript object that mirrors the structure of the real DOM. It lives in memory and is much faster to manipulate.

How React Uses It — The Reconciliation Process:
1. You update state (e.g., setCount(count + 1))
2. React creates a NEW Virtual DOM tree reflecting the new state
3. React diffs the new VDOM against the previous VDOM (this is the "diffing algorithm")
4. React calculates the minimum number of changes needed
5. Only those specific changes are applied to the real DOM

This is called reconciliation, and it's what makes React efficient.

React Fiber (React 16+)
React Fiber is a complete rewrite of React's reconciliation engine. It introduced:
- Incremental rendering: Split rendering work into chunks
- Priority scheduling: High-priority updates (user input) are processed before low-priority ones (data fetching)
- Concurrent Mode (React 18): Render in the background without blocking the UI

Key Takeaway:
React's VDOM doesn't make individual operations faster — it makes batched UI updates smarter. The real win is fewer, targeted DOM mutations rather than full re-renders.''',
            'tech',
            'ReactJS, JavaScript, Frontend, Web Dev',
        ),
        (
            user_ids.get('aarav_k', 1),
            'Top 15 SQL Interview Questions with Answers',
            '''SQL is tested in almost every backend, data, and full-stack role. Here are the 15 questions I got asked most across 8 interviews.

1. INNER JOIN vs LEFT JOIN?
INNER returns only matching rows. LEFT returns all rows from the left table + matching rows from right (NULLs where no match).

2. How do you find duplicate records?
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

3. What are window functions?
Functions that operate over a set of rows related to the current row, without collapsing them into groups.
Example: SELECT name, salary, RANK() OVER (ORDER BY salary DESC) FROM employees;

4. GROUP BY vs HAVING?
WHERE filters rows before grouping. HAVING filters after grouping.

5. What is a CTE?
Common Table Expression — a named temporary result set.
WITH top_users AS (SELECT * FROM users WHERE posts > 10) SELECT * FROM top_users;

6. How does indexing improve performance?
An index creates a data structure (B-tree) that allows the DB engine to find rows without scanning the full table.

7. What are ACID properties?
Atomicity, Consistency, Isolation, Durability — guarantees for reliable transactions.

8. Find the second highest salary:
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);

9. DELETE vs TRUNCATE vs DROP?
DELETE: Removes specific rows, can be rolled back.
TRUNCATE: Removes all rows, faster, cannot be rolled back easily.
DROP: Removes the entire table structure.

10. What is a self join?
Joining a table with itself. Useful for hierarchical data.
SELECT e.name, m.name AS manager FROM employees e JOIN employees m ON e.manager_id = m.id;

Prepare these cold and you'll handle most SQL interview rounds confidently!''',
            'interview',
            'SQL, Database, Interview, Backend',
        ),
        (
            user_ids.get('sneha_r', 2),
            'My Microsoft MSIDC Campus Interview — All 5 Rounds Explained',
            '''Microsoft visited our campus for MSIDC (Microsoft India Development Center) roles. Here's a full breakdown of every round I faced.

Shortlisting: Resume + Online Coding Test
2 coding questions in 90 minutes on HackerRank.
Q1: Merge overlapping intervals (Medium)
Q2: Serialize and deserialize a binary tree (Hard)
I solved both fully. 140/180 was the cutoff at our college.

Round 1 — Coding (45 min)
Interviewer: Friendly senior SDE
Q: Given a matrix, find the longest path where each step is strictly increasing.
I used DFS with memoization. Explained my approach clearly before coding. Got optimal solution.

Round 2 — Coding (45 min)
Q1: Design a LRU Cache (classic — use OrderedDict in Python)
Q2: Check if a binary tree is a valid BST
Both solved within time. Interviewer asked about edge cases.

Round 3 — System Design (60 min)
Design a Notification System (like WhatsApp delivery receipts).
Topics covered: message queues, pub-sub, database schema, fan-out problem, read receipts.
I used Kafka + Redis + PostgreSQL. Interviewer seemed happy.

Round 4 — Behavioral (30 min)
Standard behavioral with a twist — Microsoft loves "Growth Mindset" questions.
"Tell me about something you learned recently outside your comfort zone."
"Describe a time you improved a process."

Round 5 — HR
Salary discussion, relocation, joining date. Straightforward.

Offer: SDE-1, Hyderabad, 26 LPA + joining bonus.

Tips: Be collaborative, not just smart. Microsoft values culture fit heavily.''',
            'placement',
            'Microsoft, Campus Placement, SDE, MSIDC',
        ),
        (
            user_ids.get('priya_m', 3),
            'System Design Basics: Build a URL Shortener from Scratch',
            '''System Design is asked at SDE-1 level at companies like Microsoft, Amazon, and Flipkart. A URL Shortener is the most common starter problem. Here's how to approach it properly.

Step 1 — Clarify Requirements
Functional:
- Given a long URL, generate a short 6–8 character alias
- Redirect short URL to original URL
- Optional: custom aliases, expiry dates

Non-Functional:
- High availability (99.99% uptime)
- Low latency redirection (< 10ms)
- Scale: 100M URLs created/day, 10B redirections/day

Step 2 — Capacity Estimation
Writes: 100M/day = ~1200/sec
Reads: 10B/day = ~115,000/sec (read-heavy system)
Storage: 100M * 500 bytes = 50 GB/day

Step 3 — URL Shortening Algorithm
Option A: MD5 hash → take first 6 chars (collision risk)
Option B: Base62 encoding of an auto-incremented ID (recommended)
62^6 = 56 billion unique URLs — more than enough.

Step 4 — Database Design
URLs Table: id (bigint), short_code (varchar 8, indexed), original_url (text), user_id, created_at, expires_at

Step 5 — High-Level Architecture
Client → Load Balancer → App Servers → Cache (Redis) → DB (MySQL)
- Cache the most accessed short codes in Redis (LRU eviction)
- Use consistent hashing for distributed caching

Step 6 — Redirection Flow
1. User hits short URL
2. App server checks Redis cache
3. Cache miss → query DB → store in cache
4. Return HTTP 301 (permanent) or 302 (temporary) redirect

This structure shows you can think end-to-end. Practice 10 such problems before interviews!''',
            'coding',
            'System Design, HLD, Architecture, Interview',
        ),
        (
            user_ids.get('rohan_j', 4),
            'Understanding REST APIs — A Complete Guide for Students',
            '''REST APIs are the backbone of modern web development. If you're going into any software role, you need to understand them deeply — not just know what they are.

What is REST?
REST stands for Representational State Transfer. It's an architectural style for designing networked applications using HTTP.

The 6 REST Constraints:
1. Client-Server: Separation of concerns
2. Stateless: Each request contains all needed information
3. Cacheable: Responses can be cached
4. Uniform Interface: Consistent resource identification
5. Layered System: Client doesn't know if it's talking to the real server
6. Code on Demand (optional): Server can send executable code

HTTP Methods and When to Use Them:
GET    → Read a resource           (safe, idempotent)
POST   → Create a new resource     (not idempotent)
PUT    → Replace a resource fully  (idempotent)
PATCH  → Partially update          (not necessarily idempotent)
DELETE → Remove a resource         (idempotent)

HTTP Status Codes You Must Know:
200 OK — success
201 Created — resource created
400 Bad Request — client error
401 Unauthorized — not logged in
403 Forbidden — logged in but no permission
404 Not Found
409 Conflict — duplicate resource
422 Unprocessable Entity — validation error
500 Internal Server Error

REST vs GraphQL vs gRPC:
REST: Simple, widely supported, great for CRUD
GraphQL: Flexible queries, reduces over-fetching, good for complex UIs
gRPC: High-performance binary protocol, great for microservices

Good REST API Design Tips:
- Use nouns not verbs: /users not /getUsers
- Use plural: /posts not /post
- Version your API: /api/v1/posts
- Return meaningful error messages

Build a small CRUD REST API in Flask or Node.js this week — best way to internalize this!''',
            'tech',
            'REST API, HTTP, Web Dev, Backend, Flask',
        ),
    ]

    for user_id, title, content, category, tags in sample_posts:
        if user_id:
            conn = get_db()
            conn.execute(
                'INSERT INTO posts (user_id, title, content, category, tags) VALUES (?,?,?,?,?)',
                (user_id, title, content, category, tags)
            )
            conn.commit()
            conn.close()

    print(f"✅ Seeded {len(sample_users)} users and {len(sample_posts)} posts.")


# ── Password helpers ──────────────────────────────────────

def hash_password(password, salt=None):
    """Hash a password with a random salt using SHA-256."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def verify_password(password, stored_hash, salt):
    """Verify a plain password against its stored hash."""
    hashed, _ = hash_password(password, salt)
    return hashed == stored_hash


# ── User queries ──────────────────────────────────────────

def create_user(name, username, email, password):
    """Insert a new user. Returns (True, user_id) or (False, error_msg)."""
    conn = get_db()
    try:
        hashed, salt = hash_password(password)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, username, email, password, salt) VALUES (?,?,?,?,?)',
            (name, username, email, hashed, salt)
        )
        conn.commit()
        return True, cursor.lastrowid
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return False, 'Username already taken.'
        if 'email' in str(e):
            return False, 'Email already registered.'
        return False, 'Registration failed.'
    finally:
        conn.close()

def get_user_by_username(username):
    """Fetch a user row by username."""
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Fetch a user row by id."""
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user


# ── Post queries ──────────────────────────────────────────

def get_all_posts(category=None):
    """Fetch all posts, optionally filtered by category."""
    conn = get_db()
    if category:
        posts = conn.execute(
            '''SELECT p.*, u.name AS author_name
               FROM posts p JOIN users u ON p.user_id = u.id
               WHERE p.category = ?
               ORDER BY p.created_at DESC''',
            (category,)
        ).fetchall()
    else:
        posts = conn.execute(
            '''SELECT p.*, u.name AS author_name
               FROM posts p JOIN users u ON p.user_id = u.id
               ORDER BY p.created_at DESC'''
        ).fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    """Fetch a single post with author info."""
    conn = get_db()
    post = conn.execute(
        '''SELECT p.*, u.name AS author_name
           FROM posts p JOIN users u ON p.user_id = u.id
           WHERE p.id = ?''',
        (post_id,)
    ).fetchone()
    conn.close()
    return post

def get_posts_by_user(user_id):
    """Fetch all posts written by a specific user."""
    conn = get_db()
    posts = conn.execute(
        '''SELECT p.*, u.name AS author_name
           FROM posts p JOIN users u ON p.user_id = u.id
           WHERE p.user_id = ?
           ORDER BY p.created_at DESC''',
        (user_id,)
    ).fetchall()
    conn.close()
    return posts

def create_post(user_id, title, content, category, tags):
    """Insert a new post."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO posts (user_id, title, content, category, tags) VALUES (?,?,?,?,?)',
        (user_id, title, content, category, tags)
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def update_post(post_id, title, content, category, tags):
    """Update an existing post."""
    conn = get_db()
    conn.execute(
        'UPDATE posts SET title=?, content=?, category=?, tags=? WHERE id=?',
        (title, content, category, tags, post_id)
    )
    conn.commit()
    conn.close()

def delete_post(post_id):
    """Delete a post by id."""
    conn = get_db()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
