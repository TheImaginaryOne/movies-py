from flask import Blueprint, render_template, request
from domainmodel.repository import Repository

MOVIES_ON_PAGE = 15


def movies_blueprint(repository: Repository):
    blueprint = Blueprint('movies', __name__, template_folder='templates', static_folder='static')

    @blueprint.route('/movies')
    def show():
        try:
            page: int = int(request.args.get('page', '0'))
            results, is_not_end = repository.view_movies(page * MOVIES_ON_PAGE, MOVIES_ON_PAGE)

            previous_id = page - 1 if page >= 1 and len(results) > 0 else None
            next_id = page + 1 if is_not_end else None

            return render_template('movies.html', movies=results, previous_id=previous_id, next_id=next_id)
        except ValueError:
            return render_template('movies.html', movies=[])

    return blueprint
