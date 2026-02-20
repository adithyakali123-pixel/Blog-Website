# Best4You — Student Knowledge Sharing Blog

A full-stack blog application built with **Python (Flask)**, **SQLite**, **HTML**, **CSS**, and **JavaScript**.

## Features

- ✅ User Registration & Login with secure password hashing (SHA-256 + salt)
- ✅ Create, Read, Update, Delete (CRUD) blog posts
- ✅ 4 categories: Coding, Interview Prep, Placement Experience, Technical Articles
- ✅ Filter posts by category
- ✅ User profile with post history
- ✅ Responsive design (mobile-friendly)
- ✅ Flash messages for user feedback
- ✅ Session-based authentication

## Project Structure

```
best4you/
├── app.py              # Flask app entry point, blueprint registration
├── database.py         # SQLite setup, all DB queries
├── requirements.txt    # Python dependencies
├── routes/
│   ├── __init__.py
│   ├── auth.py         # /login, /register, /logout
│   ├── posts.py        # /write, /post/<id>, /post/<id>/edit, /post/<id>/delete
│   └── main.py         # / (home with filtering)
├── templates/
│   ├── base.html       # Shared layout (nav, flash, footer)
│   ├── home.html       # Home page with post list + sidebar
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   ├── write.html      # Create new post
│   ├── edit_post.html  # Edit existing post
│   ├── post_detail.html# Full post view
│   └── profile.html    # User profile + my posts
└── static/
    ├── css/
    │   └── main.css    # All styles
    └── js/
        └── main.js     # Flash auto-dismiss, nav highlight
```

## Setup & Run

```bash
# 1. Install Flask
pip install flask

# 2. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The SQLite database (`best4you.db`) is created automatically on first run.

## Tech Stack

| Layer     | Technology           |
|-----------|----------------------|
| Backend   | Python, Flask        |
| Database  | SQLite (built-in)    |
| Frontend  | HTML5, CSS3, JS (ES6)|
| Auth      | SHA-256 + salt hash  |
| Sessions  | Flask server sessions|
