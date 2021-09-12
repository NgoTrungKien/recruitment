from flask import Blueprint, render_template
from flask_login import login_required

from vn.com.tuyendung.form.company import CompanyRegisterForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html', segment='index')
