import traceback

from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

from vn.com.tuyendung.form.project import JobRegisterForm
from vn.com.tuyendung.model.candidate import Candidate
from vn.com.tuyendung.model.company import Company
from vn.com.tuyendung.model.project import Project
from vn.com.tuyendung.model.recruitment import Recruitment

recruitment = Blueprint('recruitment', __name__)


@recruitment.route('/')
def home():
    return render_template('recruitment/home.html', segment='recruitment', projects=Project.all())


@recruitment.route('/dang-ky/<id>', methods=['GET'])
@login_required
def register(id):
    try:
        candidates = Candidate.filter_collaborator(current_user.id)
        project = Project.get(int(id))
        count = 0
        for candidate in candidates:
            recruitment = Recruitment.filter(candidate.id, project.id)
            if recruitment is None:
                recruitment = Recruitment(candidate=candidate, project=project)
                recruitment.create_or_update()
                count = count + 1
        message = f'<a class="text-success">Bạn đã đăng ký thành công {count} ứng viên vào dự án {project.title} của công ty {project.company.name}.</a>'
    except Exception as error:
        message = f'<a class="text-danger">{error.__str__()}.</a>'
    return render_template('recruitment/home.html', segment='recruitment', projects=Project.all(), message=message)
