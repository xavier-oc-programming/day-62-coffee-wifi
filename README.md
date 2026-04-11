# Coffee & Wifi — Day 62

Flask web app to browse and submit cafes with ratings for coffee quality, wifi strength, and power socket availability.

Finding a cafe that actually has reliable wifi, enough power sockets, and decent coffee is harder than it should be. Users land on the home page, click through to a crowd-sourced table of rated cafes, and can submit a new entry — name, Google Maps link, opening hours, and three emoji ratings — through a validated form. Each submission is appended immediately to the data store and appears in the table on the next visit.

The app is built with Flask for routing and request handling, Flask-WTF and WTForms for form rendering and validation, and Bootstrap-Flask for Bootstrap 5 styling. Data is persisted to a CSV file read with `csv.DictReader` — no ORM or migration tooling required.

---

## Table of Contents

1. [Quick start](#1-quick-start)
2. [Usage](#2-usage)
3. [Data flow](#3-data-flow)
4. [Features](#4-features)
5. [Route map](#5-route-map)
6. [Architecture](#6-architecture)
7. [Module reference](#7-module-reference)
8. [Configuration reference](#8-configuration-reference)
9. [Environment variables](#9-environment-variables)
10. [Design decisions](#10-design-decisions)
11. [Course context](#11-course-context)
12. [Dependencies](#12-dependencies)

---

## 1. Quick start

```bash
git clone https://github.com/xavier-oc-programming/day-62-coffee-wifi.git
cd day-62-coffee-wifi
pip install -r requirements.txt
cp .env.example .env          # edit .env and set SECRET_KEY
python main.py
```

Open `http://127.0.0.1:5002` in your browser.

---

## 2. Usage

**Browse cafes**
1. Land on the home page (`/`)
2. Click **Show Me!**
3. View the table of cafes — name, Maps link, hours, and emoji ratings

**Submit a new cafe**
1. From the home page, click **Add a Cafe** — or navigate to `/add` directly
2. Fill in the form: name, Google Maps URL, opening time, closing time, and three ratings
3. Click **Submit** — the entry is appended to the CSV and you are redirected to `/cafes`

---

## 3. Data flow

```
Browser request
      │
      ▼
Flask route (main.py)
      │
      ├── GET /cafes
      │     └── csv.DictReader(cafe-data.csv)
      │           └── Template render → cafes.html (table)
      │
      ├── GET /add
      │     └── CafeForm() instantiated
      │           └── Template render → add.html (form)
      │
      └── POST /add
            ├── Flask-WTF CSRF check
            ├── WTForms field validation (DataRequired, URL)
            ├── csv.writer.writerow() → cafe-data.csv (append)
            └── redirect → /cafes
```

---

## 4. Features

- Home page with links to the cafe list and the submission form
- Cafe table with column headers, Google Maps links, and emoji ratings
- WTForms submission form with client-side and server-side validation
- URL validator on the Maps field — rejects non-URL input
- Emoji select fields for coffee quality, wifi strength, and power socket availability
- Bootstrap 5 dark theme with custom CSS overrides
- CSV persistence — no database setup required

---

## 5. Route map

| Method | Path     | Auth | Description                              |
|--------|----------|------|------------------------------------------|
| GET    | `/`      | —    | Home page                                |
| GET    | `/cafes` | —    | Table of all cafes with Maps links       |
| GET    | `/add`   | —    | Blank submission form                    |
| POST   | `/add`   | —    | Validate form → append to CSV → redirect |

---

## 6. Architecture

```
main.py            ← Flask app instance — route handlers only
forms.py           ← CafeForm (WTForms) — framework-agnostic
config.py          ← all constants and environment loading
cafe-data.csv      ← data store (CSV, committed)
templates/
  base.html        ← Bootstrap 5 layout, shared CSS link, Jinja2 blocks
  index.html       ← home page with navigation buttons
  add.html         ← submission form rendered with render_form()
  cafes.html       ← cafe table, DictReader output, Maps links
static/
  css/styles.css   ← dark background, link colour, jumbotron overrides
requirements.txt   ← pinned pip dependencies + Python version note
.env.example       ← SECRET_KEY placeholder (committed)
docs/
  COURSE_NOTES.md  ← original exercise description and skills covered
```

---

## 7. Module reference

### `main.py`

| Function    | Returns              | Description                                        |
|-------------|----------------------|----------------------------------------------------|
| `home()`    | rendered template    | Renders `index.html`                               |
| `add_cafe()`| rendered template or redirect | GET: renders blank form. POST: validates, appends row, redirects to `/cafes` |
| `cafes()`   | rendered template    | Reads CSV via `DictReader`, passes list of dicts and headers to `cafes.html` |

### `forms.py`

| Class      | Fields                                                                 | Description                        |
|------------|------------------------------------------------------------------------|------------------------------------|
| `CafeForm` | `cafe`, `location`, `open`, `close`, `coffee_rating`, `wifi_rating`, `power_rating`, `submit` | WTForms form for cafe submission |

### `config.py`

| Symbol          | Description                                         |
|-----------------|-----------------------------------------------------|
| `SECRET_KEY`    | Loaded from `SECRET_KEY` env var via `python-dotenv` |
| `PORT`          | Flask dev server port                               |
| `DEBUG`         | Flask debug flag                                    |
| `DATA_CSV`      | `Path` to `cafe-data.csv` relative to `config.py`  |
| `CSV_HEADERS`   | Column name list for table header rendering         |
| `COFFEE_CHOICES`| Emoji strings for coffee rating select field        |
| `WIFI_CHOICES`  | Emoji strings for wifi strength select field        |
| `POWER_CHOICES` | Emoji strings for power socket select field         |

---

## 8. Configuration reference

| Constant        | Default                             | Description                            |
|-----------------|-------------------------------------|----------------------------------------|
| `SECRET_KEY`    | `"change-me-set-in-.env"`           | Flask session signing key (override via `.env`) |
| `PORT`          | `5002`                              | Flask dev server port                  |
| `DEBUG`         | `True`                              | Enables Flask debug mode               |
| `DATA_CSV`      | `<project root>/cafe-data.csv`      | Path to the CSV data store             |
| `CSV_HEADERS`   | `["Cafe Name", …, "Power"]`         | Column names rendered as table headers |
| `COFFEE_CHOICES`| `["☕️", …, "☕☕☕☕☕"]`             | Coffee quality rating options          |
| `WIFI_CHOICES`  | `["✘", …, "💪💪💪💪💪"]`            | Wifi strength rating options           |
| `POWER_CHOICES` | `["✘", …, "🔌🔌🔌🔌🔌"]`            | Power socket availability options      |

---

## 9. Environment variables

| Variable     | Required | Description                                    |
|--------------|----------|------------------------------------------------|
| `SECRET_KEY` | Yes      | Flask session signing key — any random string  |

Copy `.env.example` to `.env` and set the value. The `.env` file is gitignored and never committed.

---

## 10. Design decisions

**CSV over a database** — the project teaches WTForms and routing, not ORM setup. A CSV keeps the focus on what matters at Day 62 and is readable without any tooling.

**`config.py` for all constants** — form choices, the CSV path, the port, and the secret key name all live in one place. Changing any of them is a one-line edit.

**`forms.py` separated out** — keeps `main.py` focused on routes. `forms.py` has no Flask imports, so it is framework-agnostic and easy to unit-test in isolation.

**`SECRET_KEY` from `.env`** — hardcoding a signing key is a bad habit even in throwaway projects. Loading it from the environment keeps the pattern portable to any Flask project.

**`DictReader` over plain `reader`** — named column access (`cafe["Wifi"]`) instead of positional index (`row[4]`). Safer when columns are reordered and readable without knowing the schema by heart.

---

## 11. Course context

**100 Days of Code — Day 62** · Flask · WTForms · Bootstrap 5 · CSV persistence · Jinja2 template inheritance

---

## 12. Dependencies

| Module            | Used in      | Purpose                                         |
|-------------------|--------------|-------------------------------------------------|
| `flask`           | `main.py`    | Web framework — routing, templates, redirects   |
| `Bootstrap-Flask` | `main.py`    | Renders WTForms with Bootstrap 5 styling        |
| `flask-wtf`       | `main.py`    | CSRF protection and Flask integration for WTForms |
| `wtforms`         | `forms.py`   | Form class, field types, validators             |
| `werkzeug`        | transitive   | WSGI utilities; pinned for compatibility        |
| `python-dotenv`   | `config.py`  | Loads `SECRET_KEY` from `.env`                  |
| `csv`             | `main.py`    | Reading (`DictReader`) and writing the CSV      |
| `pathlib`         | `config.py`  | Resolves file paths relative to the script      |
