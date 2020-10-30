# CS235 (Fresh Oranges)
The Flask project for the 2020 S2 CompSci 235 practical assignment.

## Instructions (Linux)

Set up a new `settings.cfg` file for Flask config. 

The `TMDB_KEY` is required for fetching
image urls from [The Movie Database](https://www.themoviedb.org/).
### Example 

```
TMDB_KEY = '012345678'
SECRET_KEY = 'secret123'
REPOSITORY = 'database' # or 'memory' for an in-memory repository
DATABASE_URI = 'sqlite:///epic.sqlite3'
```

Create a new virtual environment to deploy:

```
python -m venv venv # must be python 3
source venv/bin/activate
pip install -r requirements.txt
python -m pytest
FLASK_ENV=development CONFIG=settings.cfg python -m flask run
```
Note if `FLASK_DEBUG=1` (or `FLASK_ENV=development` which does the some thing), then the `SECRET_KEY` is TEST.
Also, run `CONFIG=settings.cfg python -m flask load-data` to reload the movies data (wiping all other
data in the process).

## Screenshot
Home page
![Home page](homepage.png)
Single movie
![Movie page](movie-page.png)
