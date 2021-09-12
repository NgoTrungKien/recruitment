from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from vn.com.tuyendung.form.auth import LoginForm, AccountRegisterForm
from vn.com.tuyendung.model.user import User
from .. import login as login_manager

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = LoginForm()
        if form.validate_on_submit():
            id = form.user_id.data
            password = form.password.data
            user = User.get(id)
            if user is None:
                return render_template('accounts/login.html', msg='Tài khoản không tồn tại!!!', form=form)
            status = user.verify_pass(provided_password=password)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')
            if status:
                login_user(user, remember=form.remember_me.data)
                return redirect(next_page)
            else:
                return render_template('accounts/login.html',
                                       msg='Sai thông tin đăng nhập. Vui lòng nhập lại tài khoản/mật khẩu.!!!',
                                       form=form)
        return render_template('accounts/login.html', title='Đăng nhập', form=form)
    except Exception as error:
        return render_template('accounts/login.html',
                               msg=error.__str__(),
                               form=form)


@auth.route('/register', methods=['GET'])
def register():
    return render_template('accounts/register.html',
                           msg=None
                           , success=False
                           , form=AccountRegisterForm())


@auth.route('/register', methods=['POST'])
def registration():
    try:
        form = AccountRegisterForm()
        if form.validate_on_submit():
            id = form.user_id.data
            email = form.email.data
            user = User.get(id=id)
            if user:
                return render_template('accounts/register.html',
                                       msg='Số CCCD/CMT đã được đăng ký trước đó, vui lòng kiểm tra.'
                                       , success=False
                                       , form=form)
            user = User.filter(email=email)
            if user:
                return render_template('accounts/register.html'
                                       , msg='Email đã được đăng ký trước đó, vui lòng kiểm tra.'
                                       , success=False
                                       , form=form)
            user = User(id=id, email=email, name=form.name.data, password=form.password.data)
            user.create_or_update()
            return render_template('accounts/register.html',
                                   msg='Tài khoản đã được tạo thành công. Vui lòng <a href="/login">Đăng nhập</a>',
                                   success=True,
                                   form=form)
        else:
            errors = []
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    errors.append(f'{form[fieldName].label.text}: {err}')
            return render_template('accounts/register.html'
                                   , msg=errors
                                   , success=False
                                   , form=form)
    except Exception as error:
        return render_template('accounts/register.html'
                               , msg=error.__str__()  # 'Đã có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.'
                               , success=False
                               , form=AccountRegisterForm())
        # return traceback.format_exc()


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('error/page-403.html'), 403


@auth.errorhandler(403)
def access_forbidden(error):
    return render_template('error/page-403.html'), 403


@auth.errorhandler(404)
def not_found_error(error):
    return render_template('error/page-404.html'), 404


@auth.errorhandler(500)
def internal_error(error):
    return render_template('error/page-500.html'), 500
