from flask import Blueprint, render_template
from flask_login import login_required, current_user

from vn.com.tuyendung.__global__ import MALE, FEMALE
from vn.com.tuyendung.form.candidate import CandidateRegisterForm
from vn.com.tuyendung.model.candidate import Candidate

candidate = Blueprint('candidate', __name__)


@candidate.route('/')
@login_required
def home():
    return render_template('candidate/home.html', segment='candidate',
                           candidates=Candidate.filter_collaborator(current_user.id))


@candidate.route('/register', methods=['GET'])
@login_required
def register():
    return render_template('candidate/register.html', segment='candidate', form=CandidateRegisterForm())


@candidate.route('/register', methods=['POST'])
@login_required
def registration():
    form = CandidateRegisterForm()
    try:
        if form.validate_on_submit():
            candidate = Candidate.filter_by_identity_no_and_collaborator(user_id=current_user.id,
                                                                         identity=form.identity_no.data)
            if candidate:
                message = f'<a class="text-warning">Bạn đã đăng ký ứng viên này trước đó. Vui lòng kiểm tra lại</a>'
            else:
                candidate = Candidate(name=form.name.data
                                      , gender=(lambda x: MALE if x == '1' else FEMALE)(form.gender.data)
                                      , date_of_birth=form.date_of_birth.data
                                      , address=form.address.data
                                      , phone=form.phone.data
                                      , email=form.email.data
                                      , identity_no=form.identity_no.data
                                      , collaborator_id=current_user.id)
                candidate.create_or_update()
                message = f'<a class="text-success">Ứng viên {candidate.name} đã được đăng ký thành công.</a>'
        else:
            errors = []
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    errors.append(f'{form[fieldName].label.text}')  #: {err}')
            message = f'<a class="text-warning">Đã có lỗi xảy ra, vui lòng kiểm tra lại dữ liệu đã nhập.<br/> {errors}</a>'
    except Exception as error:
        message = f'<a class="text-danger">{error.__str__()}.</a>'
    return render_template('candidate/register.html', segment='candidate', form=form, message=message)


@candidate.route('/profile/<id>', methods=['GET'])
@login_required
def profile(id: int):
    candidate = Candidate.filter_by_id_and_collaborator(user_id=current_user.id,
                                                                 id=id)
    if candidate is None:
        return render_template('candidate/home.html', segment='candidate',
                               candidates=Candidate.filter_collaborator(current_user.id)
                               , message=f'<a class="text-warning">Sai thông tin. Vui lòng kiểm tra lại</a>')
    return render_template('candidate/profile.html', segment='candidate', candidate=candidate)
