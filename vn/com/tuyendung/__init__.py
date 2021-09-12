from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from vn.com.tuyendung.config import Config

app = Flask(__name__)
db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
    })

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Vui lòng đăng nhập trước khi sử dụng.'


# mail = Mail()


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception = None):
        db.session.remove()


def register_extensions(app):
    configure_database(app)
    db.init_app(app)
    login.init_app(app)


def register_blueprints(app):
    from .controller import main, auth, company, project, candidate,recruitment
    app.register_blueprint(main)
    app.register_blueprint(auth)  # , url_prefix='/auth'
    app.register_blueprint(company, url_prefix='/company')
    app.register_blueprint(project, url_prefix='/id')
    app.register_blueprint(candidate, url_prefix='/candidate')
    app.register_blueprint(recruitment, url_prefix='/du-an')


def create_app(config_class = Config):
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)
    return app
