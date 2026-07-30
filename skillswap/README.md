# SkillSwap 🔁

A full-stack platform where people exchange skills instead of paying for courses — built entirely with **HTML, CSS, JavaScript, Flask, and SQLite**. No frameworks, no paid services.

## ✨ Features

- **Landing page** — hero, live skill search, featured teachers, "how it works", categories, animated community stats, testimonials, CTA
- **Auth** — signup (with profile photo upload + skills), login (remember me), logout
- **Dashboard** — welcome banner, stat cards, recent swap requests, my skills, notifications, quick actions
- **Browse Skills** — search + category filters, paginated skill cards
- **Profile pages** — banner, bio, skills offered/wanted, ratings, "Send Swap Request" modal
- **Swap Requests** — tabbed Incoming / Outgoing / Pending / Accepted / Rejected with accept/decline actions
- **Chat** — sidebar conversation list + message thread, all backed by the database
- **Settings** — edit profile, change password, dark mode toggle, delete account
- **Dark mode** — persisted via localStorage, applied instantly on load (no flash)
- Fully responsive: desktop, tablet, and mobile layouts

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 + Flask (Blueprints) |
| Database | SQLite (raw `sqlite3`, no ORM) |
| Frontend | Vanilla HTML, CSS, JavaScript (no frameworks) |
| Auth | Werkzeug password hashing + Flask sessions |

## 📂 Project Structure

```
skillswap/
├── app.py                 # Entry point
├── config.py               # Configuration
├── models/                 # Database layer (db.py, schema.sql)
├── routes/                 # Flask Blueprints (one file per feature)
├── static/
│   ├── css/                 # One stylesheet per page + shared base/components
│   ├── js/                  # One script per page + shared main/theme
│   ├── images/               # Logo, icons, illustrations
│   └── uploads/profile_pics/ # User-uploaded avatars
└── templates/               # Jinja2 templates (base.html + partials + pages)
```

## 🚀 Getting Started

1. **Install dependencies** (Python 3.8+ required):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   python app.py
   ```

3. **Open your browser** to:
   ```
   http://127.0.0.1:5000
   ```

The SQLite database (`database.db`) is created automatically on first run — no manual setup needed.

## 🎨 Design System

- **Colors:** Emerald/teal primary (`#0E7C66`), warm coral accent (`#FF6B4A`), warm neutral grays
- **Typography:** Sora (headings) + Inter (body) + JetBrains Mono (tags/accents)
- **Style:** Soft rounded corners, subtle glassmorphism, gradient accents, scroll-reveal animations, elevation-based shadows

All design tokens live in `static/css/base.css` as CSS custom properties — change a value there and it updates everywhere.

## 🔐 Notes

- Social login buttons on the Login/Signup pages are **UI only** (no real OAuth) — this was an explicit scope decision to keep the stack to HTML/CSS/JS/Flask/SQLite with no paid services.
- Chat is not real-time (no WebSockets) — messages load on page request/send. This keeps the stack dependency-free; swapping in polling or WebSockets later would be a straightforward enhancement.
- File uploads are limited to 3MB and validated by extension (`png`, `jpg`, `jpeg`, `gif`, `webp`).

## 📄 License

Built as a portfolio project. Free to use and modify.
