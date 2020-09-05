from flask import Blueprint, render_template, request
from domainmodel.repository import Repository

MOVIES_ON_PAGE = 15


def movies_blueprint(repository: Repository):
    blueprint = Blueprint('simple', __name__, template_folder='templates', static_folder='static')

    @blueprint.route('/movies')
    def show():
        try:
            page: int = int(request.args.get('page', '0'))
            return render_template('movies.html', movies=repository.view_movies(page * MOVIES_ON_PAGE, MOVIES_ON_PAGE))
        except ValueError:
            return render_template('movies.html', movies=[])

    return blueprint
