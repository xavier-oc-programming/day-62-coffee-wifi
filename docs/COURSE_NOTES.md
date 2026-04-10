# Course Notes — Day 62

## Exercise Description

Build a Flask web application called "Coffee & Wifi" that allows users to:

1. **Browse cafes** — view a table of cafes with their name, location link,
   opening/closing times, coffee quality rating, wifi strength, and power socket
   availability.

2. **Submit a new cafe** — fill in a WTForms form (rendered with Bootstrap 5)
   and append the entry to a CSV file that acts as the data store.

## Skills Practised

- Flask routing (`@app.route`) with GET and POST methods
- WTForms `FlaskForm` with `StringField`, `SelectField`, `SubmitField`
- WTForms validators: `DataRequired`, `URL`
- Bootstrap 5 form rendering via `flask_bootstrap` (`render_form`)
- Jinja2 template inheritance (`{% extends %}`, `{% block %}`)
- Reading and appending to a CSV file with Python's `csv` module
- Redirecting after a successful POST (`redirect(url_for(...))`)

## Notes

- The `SECRET_KEY` was hardcoded in the original course solution. Redacted with
  `*****` in committed files. In the advanced build it is loaded from `.env`.
- The CSV path was relative in the original (`"cafe-data.csv"`). Fixed to use
  `Path(__file__).parent` in both builds.
