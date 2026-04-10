import sys
import csv
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent.parent / ".env")

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

import config

app = Flask(__name__, template_folder=str(config.BASE_DIR / "templates"))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-env")
Bootstrap5(app)


def get_csv_path() -> Path:
    """Return the runtime CSV, seeding from input/ if it does not exist."""
    if not config.DATA_CSV.exists():
        config.DATA_CSV.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(config.INPUT_CSV, config.DATA_CSV)
    return config.DATA_CSV


class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    location = StringField(
        "Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()]
    )
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField(
        "Coffee Rating", choices=config.COFFEE_CHOICES, validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        "Wifi Strength Rating", choices=config.WIFI_CHOICES, validators=[DataRequired()]
    )
    power_rating = SelectField(
        "Power Socket Availability",
        choices=config.POWER_CHOICES,
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = [
            form.cafe.data,
            form.location.data,
            form.open.data,
            form.close.data,
            form.coffee_rating.data,
            form.wifi_rating.data,
            form.power_rating.data,
        ]
        with open(get_csv_path(), mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(new_row)
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open(get_csv_path(), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cafe_list = list(reader)
    return render_template("cafes.html", cafes=cafe_list, headers=config.CSV_HEADERS)


if __name__ == "__main__":
    app.run(debug=True, port=config.PORT)
