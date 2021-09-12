from flask import Blueprint, render_template
from flask_login import login_required

from vn.com.tuyendung.form.company import CompanyRegisterForm
from vn.com.tuyendung.model.company import Company

company = Blueprint('company', __name__)


@company.route('/register', methods=['GET'])
@login_required
def register():
    return render_template('company/register.html', form=CompanyRegisterForm(), message='Đăng ký thông tin công ty mới',
                           segment='company')


@company.route('/register', methods=['POST'])
@login_required
def registration():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        company = Company.filter(form.name.data)
        if company:
            return render_template('company/register.html', form=CompanyRegisterForm(),
                                   message=f'<a class="text-danger">Công ty {form.name.data} đã được đăng ký trước đó.</a>',
                                   segment='company')
        company = Company(name=form.name.data, address=form.address.data, phone=form.phone.data
                          , email=form.email.data, website=form.website.data, logo=form.logo.data)
        company.create_or_update()
        return render_template('company/register.html', form=CompanyRegisterForm(),
                               message=f'<a class="text-success">Công ty {company.name} đã được đăng ký thành công.</a>',
                               segment='company')


@company.route('')
@login_required
def home():
    companies = Company.all()
    return render_template('company/home.html', companies=companies, segment='company')
