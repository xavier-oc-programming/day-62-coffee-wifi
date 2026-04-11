# Coffee & Wifi — Day 62

Flask web app to browse and submit cafes with ratings for coffee quality, wifi strength, and power socket availability.

Finding a cafe that actually has reliable wifi, enough power sockets, and decent coffee is harder than it should be. Users browse a crowd-sourced table of rated cafes and submit new ones through a validated form — name, Google Maps link, opening hours, and three emoji ratings. It's built with Flask and WTForms, styled with Bootstrap 5, and persists data to a CSV file with no database required.

---

## Quick start

```bash
git clone https://github.com/xavier-oc-programming/day-62-coffee-wifi.git
cd day-62-coffee-wifi
pip install -r requirements.txt
cp .env.example .env          # then edit .env and set SECRET_KEY
python main.py
```

Open `http://127.0.0.1:5002` in your browser.

---

## Routes

| Method | Path     | Description                              |
|--------|----------|------------------------------------------|
| GET    | `/`      | Home page                                |
| GET    | `/cafes` | Table of all cafes with Maps links       |
| GET    | `/add`   | Submission form                          |
| POST   | `/add`   | Validate form → append to CSV → redirect |

---

## File structure

```
main.py          ← Flask app — routes only
forms.py         ← CafeForm (WTForms)
config.py        ← constants, env loading
cafe-data.csv    ← data store (CSV, committed)
templates/
  base.html      ← Bootstrap 5 layout
  index.html     ← home page
  add.html       ← submission form
  cafes.html     ← cafe table with column headers
static/css/
  styles.css     ← dark theme overrides
requirements.txt
.env.example
docs/
  COURSE_NOTES.md
```

---

## Environment variables

Copy `.env.example` to `.env` and fill in:

| Variable     | Description                        |
|--------------|------------------------------------|
| `SECRET_KEY` | Flask session signing key — any random string |

---

## Design decisions

**CSV over a database** — the project teaches WTForms and routing, not ORM setup. A CSV keeps the focus on what matters at Day 62 and is readable without any tooling.

**`config.py` for all constants** — form choices, the CSV path, the port, and the secret key name all live in one place. Changing any of them is a one-line edit.

**`forms.py` separated out** — keeps `main.py` focused on routes. A file with only route handlers is easy to read at a glance.

**`SECRET_KEY` from `.env`** — hardcoding a signing key is a bad habit even in throwaway projects. Loading it from the environment keeps the pattern portable.

**`DictReader` in the cafes route** — named column access (`cafe["Wifi"]`) instead of positional index (`row[4]`). Safer when columns change and readable without knowing the schema by heart.

---

## Course context

**100 Days of Code — Day 62**
Flask · WTForms · Bootstrap 5 · CSV persistence · Jinja2 template inheritance
