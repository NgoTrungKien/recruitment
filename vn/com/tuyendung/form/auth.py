from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    user_id = StringField('Số CCCD/CMT', validators=[DataRequired()]
                          , render_kw={"placeholder": "Số CCCD/CMT"}
                          )
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ thông tin')
    submit = SubmitField('Đăng nhập')


class AccountRegisterForm(FlaskForm):
    user_id = StringField('Số CCCD/CMT', validators=[DataRequired()]
                          , render_kw={"placeholder": "Số CCCD/CMT"})
    email = StringField('Email', validators=[DataRequired(), Email()]
                        , render_kw={"placeholder": "Email: vidu@gmail.com"})
    name = StringField('Họ & tên', validators=[DataRequired()]
                       , render_kw={"placeholder": "Họ & tên"})
    password = PasswordField('Mật khẩu', validators=[DataRequired()]
                             , render_kw={"placeholder": "Mật khẩu"})
    submit = SubmitField('Tạo tài khoản')
