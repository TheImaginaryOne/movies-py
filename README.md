# CS235 (Fresh Oranges)
The Flask project for the 2020 S2 CompSci 235 practical assignment.

## Instructions (Linux)

Set up a new `settings.cfg` file for Flask config. The `TMDB_KEY` is required for fetching
image urls from [The Movie Database](https://www.themoviedb.org/).

Create a new virtual environment to deploy:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest
FLASK_DEBUG=1 CONFIG=settings.cfg python -m flask run
```
Note if `FLASK_DEBUG=1`, then there is a demo user with username `user1234` and
password `pass1234`.

## Screenshot
Home page
![Home page](homepage.png)
Single movie
![Movie page](movie-page.png)
