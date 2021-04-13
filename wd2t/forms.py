from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NewDecisionForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    description = StringField("Description")

    submit = SubmitField("Submit")
