from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import config


class CafeForm(FlaskForm):
    cafe         = StringField("Cafe name",           validators=[DataRequired()])
    location     = StringField("Google Maps URL",     validators=[DataRequired(), URL()])
    open         = StringField("Opening Time e.g. 8AM",   validators=[DataRequired()])
    close        = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating",     choices=config.COFFEE_CHOICES, validators=[DataRequired()])
    wifi_rating   = SelectField("Wifi Strength",     choices=config.WIFI_CHOICES,   validators=[DataRequired()])
    power_rating  = SelectField("Power Sockets",     choices=config.POWER_CHOICES,  validators=[DataRequired()])
    submit        = SubmitField("Submit")
