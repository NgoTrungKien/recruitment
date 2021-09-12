from datetime import date, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.fields.html5 import URLField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import DateInput
from wtforms_components import EmailField


class CandidateRegisterForm(FlaskForm):
    name = StringField('Họ & tên ứng viên', validators=[DataRequired()])
    gender = RadioField('Giới tính', choices=[('1', 'Nam'), ('0', 'Nữ')], default='1')
    date_of_birth = DateField('Ngày sinh', format='%Y-%m-%d', widget=DateInput(),
                              validators=[DataRequired()],
                              default=date.today() - timedelta(days=6570))
    address = StringField('Địa chỉ', validators=[DataRequired()])
    phone = StringField('Số điện thoại liên lạc', validators=[DataRequired()])
    email = EmailField('Email liên lạc', validators=[DataRequired()])
    identity_no = StringField('Số CCCD/CMT của ứng viên', validators=[DataRequired()])
    submit = SubmitField('Đăng ký ứng viên')
