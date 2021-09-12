from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import URLField, IntegerField
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets.html5 import NumberInput
from wtforms_components import EmailField

from vn.com.tuyendung.model.company import Company


class JobRegisterForm(FlaskForm):
    title = StringField('Tiêu đề dự án', validators=[DataRequired()])
    content = TextAreaField('Nội dung công việc', validators=[DataRequired()])
    demand_qty = IntegerField('Số lượng cần tuyển dụng', widget=NumberInput(min=1),default=1,
                              validators=[InputRequired()])
    company = SelectField('Công ty', choices=[],
                          coerce=str,
                          validators=[DataRequired()])
    submit = SubmitField('Tạo dự án')

    def __init__(self, *args, **kwargs):
        super(JobRegisterForm, self).__init__(*args, **kwargs)
        companies = [(str(company.id), company.name) for company in Company.all()]
        self.company.choices = companies
        self.company.default = [0]
