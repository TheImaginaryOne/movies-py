from flask import Blueprint, render_template, request, session, redirect, url_for, current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from domainmodel.repository import Repository
from domainmodel.review import Review
from web import services


def unwrap_or(x, default):
    return default if x is None else x




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
    blueprint = Blueprint('movies', __name__, template_folder='templates', static_folder='static', url_prefix='/movies')

    @blueprint.route('/<int:index>/review', methods=['GET', 'POST'])
    def review(index):
        if not services.user.is_logged_in(repository):
            return redirect(url_for("user.login"))

        movie = services.movies.get_movie(repository, index)
        if movie is None:
            return render_template('404.html'), 404
        form = ReviewForm()
        form.rating.choices = ratings()

        try:
            rating = int(form.rating.data)
        except:
            return render_template('review_form.html', movie_index=index, movie=movie, form=form,
                                   errors=form.review_text.errors)

        services.movies.add_review(repository, index, form.review_text.data, rating)

        return redirect(url_for('movies.single_movie', index=index))

    @blueprint.route('/<int:index>')
    def single_movie(index):
        movie = services.movies.get_movie(repository, index)
        if movie is None:
            return render_template('404.html'), 404

        reviews = services.movies.get_reviews(repository, index)
        return render_template('single_movie.html',
                               movie=movie,
                               index=index,
                               reviews=reviews,
                               poster_url=services.movies.get_poster_url(movie))

    @blueprint.route('')
    def show():
        form = SearchForm(request.args)

        form.director.choices = [("", "--")] + [(x.full_name, x.full_name) for x in
                                                repository.directors]
        form.actors.choices = [(x.full_name, x.full_name) for x in repository.actors]
        form.genres.choices = [(x.name, x.name) for x in repository.genres]

        # print(director, actors, genres_split)
        try:
            page: int = int(request.args.get('page', '0'))
            results, is_not_end = services.movies.view_movies(repository, page,
                                                              form.director.data,
                                                              form.actors.data,
                                                              form.genres.data)

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
