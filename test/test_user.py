import pytest
from flask import session

from cs235init import create_app


@pytest.fixture
def client():
    return create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False}).test_client()


def url(x):
    return f"http://localhost{x}"


def test_register(client):
    response = client.post('/register', data={'username': 'oof', 'password': 'foofoofoo'})
    assert response.headers['Location'] == url('/login')

    response = client.post('/register', data={'username': 'oof', 'password': 'foofoofoo'})
    # 200 = no redirect
    assert response.status_code == 200


def test_register_invalid(client):
    response = client.post('/register', data={'username': 'oof', 'password': 'foofo'})
    assert response.status_code == 200

    response = client.post('/register', data={'username': '', 'password': 'foofo'})
    assert response.status_code == 200


def test_login_invalid(client):
    with client:
        response = client.post('/register', data={'username': 'oof', 'password': 'foofoofoo'})
        assert response.headers['Location'] == url('/login')
        assert 'user' not in session

        response = client.post('/login', data={'username': 'oof', 'password': 'foofoo'})
        assert response.status_code == 200
        assert 'user' not in session

        response = client.post('/login', data={'username': 'oofff', 'password': 'foofoofoo'})
        #print( response.headers)
        assert response.status_code == 200
        assert 'user' not in session


def test_login(client):
    response = client.post('/register', data={'username': 'oof', 'password': 'foofoofoo'})
    assert response.headers['Location'] == url('/login')

    with client:
        response = client.post('/login', data={'username': 'oof', 'password': 'foofoofoo'})
        assert response.headers['Location'] == url('/movies')
        assert 'user' in session

        # login redirects if logged in
        response = client.get('/login')
        assert response.headers['Location'] == url('/movies')


def test_logout(client):
    response = client.post('/register', data={'username': 'oof', 'password': 'foofoofoo'})
    assert response.headers['Location'] == url('/login')

    with client:
        response = client.post('/login', data={'username': 'oof', 'password': 'foofoofoo'})
        assert response.headers['Location'] == url('/movies')
        assert 'user' in session

        response = client.get('/logout')
        assert response.headers['Location'] == url('/login')
        assert 'user' not in session
