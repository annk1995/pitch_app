from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class PitchForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    category = SelectField('Category', choices=[('Love', 'Love'), ('Life', 'Life'), ('Motivation', 'Motivation')],
                           validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')


class Vote(FlaskForm):
    submit = SubmitField('Like')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post')