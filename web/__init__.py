from flask import Flask, render_template, url_for
from werkzeug.utils import redirect


def setup_app(app: Flask):
    @app.errorhandler(404)
    def error_404(_):
        return render_template('404.html')

    @app.route('/')
    def index():
        return redirect(url_for('movies.show'))