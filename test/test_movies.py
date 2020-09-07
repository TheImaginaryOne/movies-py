from test.test_common import client_with_data
from web.movies import MOVIES_ON_PAGE


def test_movies_basic():
    client, repo = client_with_data()
    response = client.get('/movies?page=0')
    #print(response.data)
    for i in range(MOVIES_ON_PAGE):  # TODO
        assert bytes(repo.movies[i].title, 'utf8') in response.data


def test_movies_filter_genre():
    client, repo = client_with_data()
    response = client.get('/movies?page=0&genre=Adventure&genre=Action')
    #print(response.data)
    assert bytes('Suicide Squad', 'utf8') in response.data
    assert bytes('Guardians of the Galaxy', 'utf8') in response.data
