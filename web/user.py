from flask import Blueprint, render_template, request, url_for, session, Flask
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, PasswordField, ValidationError

from domainmodel.repository import Repository


# Only A-Z|a-z|_ allowed (test!?)
def validate_username(form, field):
    if len(field.data) == 0:
        raise ValidationError("Username must not be empty")
    for ch in field.data:
        if not (ch.isalnum() or ch == '_'):
            raise ValidationError("Username must only have a-z, A-Z or _")


MIN_PASSWORD_LENGTH = 8


def validate_password(form, field):
    if len(field.data) < MIN_PASSWORD_LENGTH:
        raise ValidationError(f"Password must have at least {MIN_PASSWORD_LENGTH} characters")


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
        if 'user' in session:
            return redirect(url_for('movies.show'))
        error = None
        if request.method == 'POST':
            user_id = repository.login(form.username.data, form.password.data)
            if user_id is not None:
                session.clear()
                session['user'] = user_id
                return redirect(url_for('movies.show'))
            else:
                error = "Wrong username or password"
        return render_template("login.html", form=form, error=error)

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if request.method == 'POST':
            # print(form.username.data, form.password.data)
            if form.validate() and repository.add_user(form.username.data, form.password.data):
                return redirect(url_for("user.login"))
        return render_template("register.html", form=form, errors=form.username.errors + form.password.errors)

    return bp


# makes this available to templates
def inject_current_user(app: Flask, repository: Repository):
    @app.context_processor
    def current_user():
        if 'user' in session:
            return {"current_user": repository.get_user(session['user'])}
        return {"current_user": None}
    return current_user
