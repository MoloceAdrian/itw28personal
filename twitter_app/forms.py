from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from twitter_app.models.user import User


class ScreenNameForm(FlaskForm):
    """Form object for the user to input a screen name."""

    screen_name = StringField(
        "Twitter Screen Name", validators=[DataRequired(), Length(min=4, max=20)]
    )

    submit = SubmitField("Search")


class UploadCSVFileForm(FlaskForm):
    """Form object for the user to input a csv file."""

    csv = FileField("User CSV", validators=[FileAllowed(["csv"])])

    submit = SubmitField("Submit")
