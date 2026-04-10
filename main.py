import csv
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
import config
from forms import CafeForm

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open(config.DATA_CSV, mode="a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                form.cafe.data, form.location.data,
                form.open.data, form.close.data,
                form.coffee_rating.data, form.wifi_rating.data,
                form.power_rating.data,
            ])
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open(config.DATA_CSV, newline="", encoding="utf-8") as f:
        cafe_list = list(csv.DictReader(f))
    return render_template("cafes.html", cafes=cafe_list, headers=config.CSV_HEADERS)


if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT)
