# Coffee & Wifi — Day 62

Flask web app to browse and submit cafes with ratings for coffee quality, wifi strength, and power socket availability.

Point the app at a city, walk in with your laptop, and you already know which cafe has the fastest wifi, the most power outlets, and the best espresso. Users browse a table of crowd-sourced entries and submit new cafes through a WTForms form rendered with Bootstrap 5. Each new entry is appended to a CSV file that acts as the data store — no database required.

Two builds live side by side: **original** preserves the course solution exactly (single `main.py`, hardcoded constants, relative paths), while **advanced** refactors it into a config-driven app with environment variable support, proper path handling, and a seeded data layer that separates committed seed data from runtime state.

No external APIs or credentials are required for the original build. The advanced build reads `SECRET_KEY` from a `.env` file so the Flask signing key is never hardcoded.

---

## Table of Contents

0. [Prerequisites](#0-prerequisites)
1. [Quick start](#1-quick-start)
2. [Builds comparison](#2-builds-comparison)
3. [Usage](#3-usage)
4. [Data flow](#4-data-flow)
5. [Features](#5-features)
6. [Navigation flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module reference](#8-module-reference)
9. [Configuration reference](#9-configuration-reference)
10. [Data schema](#10-data-schema)
11. [Environment variables](#11-environment-variables)
12. [Design decisions](#12-design-decisions)
13. [Course context](#13-course-context)
14. [Dependencies](#14-dependencies)

---

## 0. Prerequisites

No external accounts needed. Python 3.10+ and pip are sufficient.

---

## 1. Quick start

```bash
git clone https://github.com/xavier-oc-programming/day-62-coffee-wifi.git
cd day-62-coffee-wifi
pip install -r requirements.txt

# Advanced build only — create a .env file:
cp .env.example .env
# Edit .env and set SECRET_KEY to any random string

python menu.py
```

The menu launches either build. Each build starts a Flask development server.
Open your browser to the URL printed in the terminal (e.g. `http://127.0.0.1:5002`).
Press `Ctrl+C` to stop the server and return to the menu.

---

## 2. Builds comparison

| Feature | Original | Advanced |
|---|---|---|
| Entry point | `original/main.py` | `advanced/main.py` |
| Port | 5002 | 5003 |
| Constants | Inline | `config.py` |
| `SECRET_KEY` | Hardcoded (`*****`) | `.env` via `python-dotenv` |
| CSV path | Fixed via `Path(__file__).parent` | Config constant + auto-seed from `input/` |
| Template data | List of rows | List of dicts (headers-aware) |
| Table headers | None | Rendered from `config.CSV_HEADERS` |

---

## 3. Usage

```
$ python menu.py

   ___        __  __           _      __        ___ __ _
  / __|___ / _|/ _|___ ___ (_)__ _ \ \      / (_)/ _(_)
 | |  / _ \  _|  _/ -_) -_)| / _` | \ \ /\ / /| | |_| |
 | |_| (_) |_| |_| \___\___|| \__,_|  \_V_/  |_|_\__|_|
  \___\___/                 |_/

      ☕  Coffee & Wifi Cafe Finder  💻

Select a build to run:

  1 → Original  (course solution, single file)
  2 → Advanced  (refactored with config, .env support)
  q → Quit

Your choice: 2
 * Running on http://127.0.0.1:5003
```

Navigate to `/` for the home page, `/cafes` to view all entries, `/add` to submit a new cafe.

---

## 4. Data flow

```
Input                  Fetch              Process           Output
─────────────────────────────────────────────────────────────────
GET /cafes         →  read CSV        →  parse rows    →  render cafes.html table
GET /add           →  render form     →  —              →  render add.html
POST /add          →  validate form   →  append row     →  redirect to /cafes
```

---

## 5. Features

**Both builds:**
- Home page with links to cafe list and add form
- `/cafes` — table of all cafes with Google Maps links
- `/add` — WTForms form with validation (DataRequired, URL)
- Emoji-based ratings for coffee, wifi, and power sockets
- Bootstrap 5 styling with dark background theme
- CSV persistence (append on submit)

**Advanced only:**
- `SECRET_KEY` loaded from `.env` (never hardcoded)
- All constants centralised in `config.py`
- `DictReader` for named column access in templates
- Table headers rendered dynamically from `config.CSV_HEADERS`
- Runtime CSV seeded automatically from `advanced/input/cafe-data.csv` on first run
- Separate ports per build (5002 original, 5003 advanced)

---

## 6. Navigation flow

```
menu.py
├── 1 → original/main.py  (port 5002)
│         └── /              home page
│               ├── /cafes   browse table
│               └── /add     submit form → /cafes
└── 2 → advanced/main.py  (port 5003)
          └── /              home page
                ├── /cafes   browse table (with headers)
                └── /add     submit form → /cafes
```

---

## 7. Architecture

```
day-62-coffee-wifi/
├── menu.py                  # Interactive build launcher
├── art.py                   # ASCII logo
├── requirements.txt         # pip dependencies
├── .env.example             # Template for .env
├── .gitignore
├── README.md
├── docs/
│   └── COURSE_NOTES.md      # Original exercise description
├── original/                # Course solution (preserved verbatim)
│   ├── main.py              # Flask app — routes, form, CSV I/O
│   ├── cafe-data.csv        # Seed data (committed)
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── add.html
│   │   └── cafes.html
│   └── static/css/styles.css
└── advanced/                # Refactored build
    ├── config.py            # All constants
    ├── main.py              # Flask app — loads .env, uses config
    ├── input/
    │   └── cafe-data.csv    # Committed seed data
    ├── data/                # Runtime CSV — gitignored
    │   └── .gitkeep
    ├── output/              # Reserved — gitignored
    │   └── .gitkeep
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── add.html
    │   └── cafes.html       # Uses DictReader output with named columns
    └── static/css/styles.css
```

---

## 8. Module reference

### `original/main.py`

| Symbol | Type | Description |
|---|---|---|
| `CafeForm` | `FlaskForm` | WTForms form with cafe fields and emoji rating selects |
| `home()` | route `GET /` | Renders `index.html` |
| `add_cafe()` | route `GET POST /add` | Renders form; on valid POST appends row to CSV and redirects |
| `cafes()` | route `GET /cafes` | Reads CSV as list of rows; renders `cafes.html` |

### `advanced/config.py`

| Symbol | Description |
|---|---|
| `BASE_DIR` | `Path(__file__).parent` — anchor for all paths |
| `INPUT_CSV` | Committed seed data at `advanced/input/cafe-data.csv` |
| `DATA_CSV` | Runtime data at `advanced/data/cafe-data.csv` (gitignored) |
| `PORT` | Flask server port (5003) |
| `COFFEE_CHOICES` | List of emoji strings for coffee rating select |
| `WIFI_CHOICES` | List of emoji strings for wifi rating select |
| `POWER_CHOICES` | List of emoji strings for power socket select |
| `CSV_HEADERS` | Column name list for table header rendering |

### `advanced/main.py`

| Symbol | Type | Description |
|---|---|---|
| `get_csv_path()` | function | Returns `DATA_CSV`, copying from `INPUT_CSV` if absent |
| `CafeForm` | `FlaskForm` | Same fields as original; choices sourced from `config` |
| `home()` | route `GET /` | Renders `index.html` |
| `add_cafe()` | route `GET POST /add` | Validates form; appends to runtime CSV; redirects |
| `cafes()` | route `GET /cafes` | Reads CSV via `DictReader`; passes list of dicts + headers to template |

---

## 9. Configuration reference

| Constant | Default | Description |
|---|---|---|
| `PORT` | `5003` | Flask dev server port (advanced build) |
| `INPUT_CSV` | `advanced/input/cafe-data.csv` | Committed seed cafe data |
| `DATA_CSV` | `advanced/data/cafe-data.csv` | Runtime cafe data (gitignored) |
| `COFFEE_CHOICES` | `["☕️", … "☕☕☕☕☕"]` | Coffee quality rating options |
| `WIFI_CHOICES` | `["✘", … "💪💪💪💪💪"]` | Wifi strength rating options |
| `POWER_CHOICES` | `["✘", … "🔌🔌🔌🔌🔌"]` | Power socket availability options |
| `CSV_HEADERS` | `["Cafe Name", …, "Power"]` | Column names for cafes table header |

---

## 10. Data schema

`cafe-data.csv` — comma-separated, UTF-8, first row is headers:

| Column | Example | Notes |
|---|---|---|
| `Cafe Name` | `Lighthaus` | Free text |
| `Location` | `https://goo.gl/maps/...` | Google Maps URL |
| `Open` | `11AM` | Free text |
| `Close` | `3:30PM` | Free text |
| `Coffee` | `☕☕☕☕️` | Emoji string, 1–5 cups |
| `Wifi` | `💪💪` | Emoji string or `✘` for none |
| `Power` | `🔌🔌🔌` | Emoji string or `✘` for none |

---

## 11. Environment variables

Required for the advanced build only.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session signing key — any random string |

Copy `.env.example` to `.env` and fill in the value. The `.env` file is gitignored and never committed.

---

## 12. Design decisions

**CSV as the data store** — no database setup, no migrations, no ORM. Perfect for a course exercise where the persistence requirement is "append a row and read it back". A real production app would use SQLite or PostgreSQL, but that would obscure the WTForms and routing skills being taught.

**`Path(__file__).parent` for CSV path** — the original course code used a bare `"cafe-data.csv"` string which resolves relative to the working directory. Running the app from a different directory silently breaks it. Using `Path(__file__).parent` makes the path relative to the script itself, so the app works from any working directory.

**Seed + runtime data split** — the advanced build keeps committed seed data in `advanced/input/` and writes runtime state to `advanced/data/` (gitignored). This means `git clone` always gives you a working app with sample data, while user additions stay local and don't clutter the repo.

**DictReader over plain reader** — `csv.DictReader` gives named column access in templates (`cafe["Wifi"]`) instead of positional index (`row[4]`). Safer when columns are reordered and readable without knowing the schema by heart.

**`SECRET_KEY` from `.env`** — hardcoding a signing key in source is a bad habit even in throwaway projects. The advanced build loads it from `.env` via `python-dotenv` so the pattern is portable to any real Flask project.

**Separate ports per build** — running original on 5002 and advanced on 5003 means both can coexist without port conflicts when switching between them.

---

## 13. Course context

**100 Days of Code — Day 62**
Topics: Flask, WTForms, Bootstrap 5 (via Bootstrap-Flask), CSV persistence, Jinja2 template inheritance.

The exercise builds a cafe-finder web app where strangers can contribute local knowledge. It introduces the full request/response cycle for a form-based web app: rendering a form, validating POST data, persisting the result, and redirecting.

See `docs/COURSE_NOTES.md` for the original exercise description.

---

## 14. Dependencies

| Module | Used in | Purpose |
|---|---|---|
| `flask` | both | Web framework — routing, templates, redirects |
| `flask_bootstrap` (`Bootstrap-Flask`) | both | Renders WTForms with Bootstrap 5 styling |
| `flask_wtf` | both | CSRF protection and Flask integration for WTForms |
| `wtforms` | both | Form class, field types, validators |
| `csv` | both | Reading and appending to the CSV data store |
| `pathlib.Path` | both | Resolve file paths relative to the script |
| `python-dotenv` | advanced | Load `SECRET_KEY` from `.env` |
| `shutil` | advanced | Copy seed CSV to data dir on first run |
