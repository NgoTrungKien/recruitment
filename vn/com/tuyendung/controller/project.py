import traceback

from flask import Blueprint, render_template, url_for
from flask_login import login_required

from vn.com.tuyendung.form.project import JobRegisterForm
from vn.com.tuyendung.model.company import Company
from vn.com.tuyendung.model.project import Project

project = Blueprint('id', __name__)


@project.route('/')
@login_required
def home():
    return render_template('project/home.html', projects=Project.all(), segment='id')


@project.route('/register', methods=['GET'])
@login_required
def register():
    return render_template('project/register.html', form=JobRegisterForm(), segment='id')


@project.route('/register', methods=['POST'])
@login_required
def registration():
    form = JobRegisterForm()
    try:
        if form.validate_on_submit():
            company = Company.get(int(form.company.data))
            project = Project(title=form.title.data
                              , content=form.content.data
                              , demand_qty=form.demand_qty.data
                              , company=company)
            project.create_or_update()
            message = f'<a class="text-success">Dự án {project.title} đã được đăng ký thành công.</a>'
        else:
            errors = []
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    errors.append(f'{form[fieldName].label.text}')  #: {err}')
            message = f'<a class="text-warning">Đã có lỗi xảy ra, vui lòng kiểm tra lại dữ liệu đã nhập.<br/> {errors}</a>'
    except Exception as error:
        message = f'<a class="text-danger">{error.__str__()}.</a>'
    return render_template('project/register.html', form=form, segment='id',
                           message=message)


@project.route('/profile/<id>', methods=['GET'])
@login_required
def profile(id: int):
    try:
        project = Project.get(id)
        return render_template('project/profile.html', project=project, segment='id')
    except Exception as error:
        return url_for('id.home')
