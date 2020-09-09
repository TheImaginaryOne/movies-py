from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from domainmodel.repository import Repository


def unwrap_or(x, default):
    return default if x is None else x


MOVIES_ON_PAGE = 15


class SearchForm(FlaskForm):
    director = SelectField('Director')
    actors = SelectMultipleField('Actors')
    genres = SelectMultipleField('Genres')
    submit = SubmitField('submit')

def ratings():
    return [(i, i) for i in range(1, 11)]

class ReviewForm(FlaskForm):
    review_text = TextAreaField('Review text')
    rating = SelectField('Rating')
    submit = SubmitField('Submit')

def movies_blueprint(repository: Repository):
    blueprint = Blueprint('movies', __name__, template_folder='templates', static_folder='static')

    @blueprint.route('/movies/<int:index>/review', methods=['GET', 'POST'])
    def review(index):
        form = ReviewForm()
        form.rating.choices = ratings()
        movie = repository.get_movie(index)
        if movie is None:
            return render_template('404.html'), 404
        return render_template('review_form.html', movie_index=index, movie=movie, form=form, errors=form.review_text.errors)

    @blueprint.route('/movies/<int:index>')
    def single_movie(index):
        movie = repository.get_movie(index)
        if movie is None:
            return render_template('404.html'), 404
        return render_template('single_movie.html', movie=movie, index=index)

    @blueprint.route('/movies')
    def show():
        form = SearchForm(request.args)

        form.director.choices = [("", "--")] + [(x.director_full_name, x.director_full_name) for x in
                                                repository.directors]
        form.actors.choices = [(x.actor_full_name, x.actor_full_name) for x in repository.actors]
        form.genres.choices = [(x.genre_name, x.genre_name) for x in repository.genres]

        director = form.director.data
        actors = list(map(lambda x: x.strip(), form.actors.data))
        genres = list(map(lambda x: x.strip(), form.genres.data))
        # print(director, actors, genres_split)
        try:
            page: int = int(request.args.get('page', '0'))
            results, is_not_end = repository.view_movies(page * MOVIES_ON_PAGE, MOVIES_ON_PAGE, director, actors,
                                                         genres)

            previous_id = page - 1 if page >= 1 and len(results) > 0 else None
            next_id = page + 1 if is_not_end else None

            query = request.args.to_dict()
            query.pop('page', None)

            return render_template('movies.html', movies=results, previous_id=previous_id, next_id=next_id, form=form,
                                   url_query=query)
        except ValueError:
            # TODO
            return render_template('movies.html', movies=[], form=form, url_query={})

    return blueprint
