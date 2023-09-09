from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, Response
)
from . import db
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField

class People(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255))
  middle_initial = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  email = db.Column(db.String(255))
  institution = db.Column(db.String(255))



bp = Blueprint('pubs', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')