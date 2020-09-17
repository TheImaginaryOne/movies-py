from flask import Blueprint, render_template, request, url_for, session, Flask, current_app as app
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, PasswordField, ValidationError

from domainmodel.repository import Repository

# Only A-Z|a-z|_ allowed (test!?)
from web import services


def validate_username(form, field):
    if len(field.data) == 0:
        raise ValidationError(ErrorMessages.non_empty_username)
    for ch in field.data:
        if not (ch.isalnum() or ch == '_'):
            raise ValidationError(ErrorMessages.invalid_username)


MIN_PASSWORD_LENGTH = 8

class ErrorMessages:
    non_empty_username = 'Username must not be empty'
    invalid_username = 'Username must only have a-z, A-Z or _'
    invalid_password = f'Password must have at least {MIN_PASSWORD_LENGTH} characters'
    duplicate_username = 'Username already exists'
    invalid_login = 'Wrong username or password'


def validate_password(form, field):
    if len(field.data) < MIN_PASSWORD_LENGTH:
        raise ValidationError(ErrorMessages.invalid_password)


class LoginForm(FlaskForm):
    username = StringField('User')
    password = PasswordField('Password')
    submit = SubmitField('submit')


class RegisterForm(FlaskForm):
    username = StringField('User', [validate_username])
    password = PasswordField('Password', [validate_password])
    submit = SubmitField('submit')


def blueprint(repository: Repository):
    bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

    @bp.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for("user.login"))

    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if services.user.is_logged_in(repository):
            return redirect(url_for('movies.show'))
        error = None
        if request.method == 'POST':
            if services.user.login(repository, form.username.data, form.password.data):
                return redirect(url_for('movies.show'))
            else:
                error = ErrorMessages.invalid_login
        return render_template("login.html", form=form, error=error)

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        errors = []
        if request.method == 'POST':
            # print(form.username.data, form.password.data)
            if form.validate():
                if services.user.register(repository, form.username.data, form.password.data):
                    return redirect(url_for("user.login"))
                else:
                    errors.append(ValidationError(ErrorMessages.duplicate_username))
            errors.extend(form.username.errors)
            errors.extend(form.password.errors)

        app.logger.info(f"Errors: {errors}")

        return render_template("register.html", form=form, errors=errors)

    return bp


# makes this available to templates
def inject_current_user(app: Flask, repository: Repository):
    @app.context_processor
    def current_user():
        if services.user.is_logged_in(repository):
            return {"current_user": repository.get_user(session['user'])}
        return {"current_user": None}
    return current_user
