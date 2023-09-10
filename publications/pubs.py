from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, Response
)
from . import db
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField
from sqlalchemy.exc import SQLAlchemyError
from wtforms.validators import DataRequired


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    middle_initial = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    institution = db.Column(db.String(255))

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    location = db.Column(db.String(255))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    # presentation = db.relationship('presentation', backref='conference', lazy=True)
class Presentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    conference_name = db.Column(db.String(255), db.ForeignKey('conference.name'))
    # conference = db.relationship('conference', backref=db.backref('presentation', lazy=True))


bp = Blueprint('pubs', __name__)


class PresentationForm(FlaskForm):
    title = StringField('Title')
    conference_name = SelectField('Conference Name', validators=[DataRequired()], choices=[])
    new_choice = StringField('New Conference Name')
    submit = SubmitField('Add Choice')

    def add_choice(self):
        new_choice = self.new_choice.data.strip()
        if new_choice and new_choice not in [choice[0] for choice in self.conference_name.choices]:
            conference = Conference(
                name=new_choice
            )
            self.conference_name.choices.append((new_choice, new_choice))
            self.new_choice.data = ''

# class PresentationForm(FlaskForm):
#     title = StringField('Title')
#     authors = StringField('Authors')
#     year = IntegerField('Year')
#     month = SelectField('Month', choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
#                                           (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
#                                           (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])
#     day = IntegerField('Day')
#     conference_name = SelectField('Conference Name', validators=[DataRequired()], choices=[])
#
#     location = StringField('Location')
#     journal = StringField('Journal')
#     volume = StringField('Volume')
#     issue = StringField('Issue')
#     pages = StringField('Pages')
#     doi = StringField('DOI')
#     pmid = StringField('PMID')
#     pmcid = StringField('PMCID')
#     submit = SubmitField('Submit')
class PeopleForm(FlaskForm):
    first_name = StringField('First Name')
    middle_initial = StringField('Middle Initial')
    last_name = StringField('Last Name')
    email = StringField('Email')
    institution = StringField('Institution')
    submit = SubmitField('Submit')
@bp.route('/', methods=['GET', 'POST'])
def index():
    presentation_form = PresentationForm()
    presentation_form.conference_name.choices = ['11th US HAB Conference', 'COHH Annual Meeting'
        # (conference.name, conference.name) for conference in Conference.query.all()
                                                  ]
    people_form = PeopleForm()
    people = People.query.all()
    presentation = Presentation.query.all()
    if people_form.validate_on_submit():
        try:
            person = People(
                first_name=people_form.first_name.data,
                middle_initial=people_form.middle_initial.data,
                last_name=people_form.last_name.data,
                email=people_form.email.data,
                institution=people_form.institution.data
            )
            db.session.add(person)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
    if presentation_form.validate_on_submit():
        try:
            presentation = Presentation(
                title=presentation_form.title.data,
                conference_name=presentation_form.conference_name.data
            )
            db.session.add(presentation)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)

        presentation = Presentation.query.all()
        people = People.query.all()


    return render_template('pubs/index.html', people_form=people_form,
                           people=people,
                           presentation_form=presentation_form
                           )
