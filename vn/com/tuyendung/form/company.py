from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired
from wtforms_components import EmailField


class CompanyRegisterForm(FlaskForm):
    name = StringField('Tên công ty', validators=[DataRequired()])
    address = StringField('Địa chỉ', validators=[DataRequired()])
    phone = StringField('Số điện thoại liên lạc', validators=[DataRequired()])
    email = EmailField('Email liên lạc', validators=[DataRequired()])
    website = URLField('Website công ty', validators=[DataRequired()])
    logo = URLField('Logo công ty', validators=[DataRequired()])
    submit = SubmitField('Đăng ký')