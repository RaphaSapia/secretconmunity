from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from secretcommunity.models import User
from flask_login import current_user

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    key = PasswordField('Key', validators=[DataRequired(), Length(6, 10)])
    reminds_me = BooleanField('Remind Me')
    submit_login = SubmitField('Login')




class FormCreate(FlaskForm):
    user = StringField('User Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    key = PasswordField('Key', validators=[DataRequired(), Length(6, 10)])
    confirm_key = PasswordField('Confirm Key', validators=[DataRequired(), EqualTo('key'), Length(6, 10)])
    submit_create = SubmitField('Create')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')


class Form_editprofile(FlaskForm):
    user = StringField('User Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    photo_profile = FileField('Photo Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    esp_python = BooleanField('Python')
    esp_java = BooleanField('Java')
    esp_pbi = BooleanField('Power BI')
    esp_html_css = BooleanField('HTML e CSS')
    esp_js = BooleanField('JavaScript')
    esp_sql = BooleanField('SQL')
    submit_editprofile = SubmitField('Edit Profile')
    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered')

class Form_createpost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(3, 50)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit_createpost = SubmitField('Create Post')


