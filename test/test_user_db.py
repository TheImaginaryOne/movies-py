from flask import session

from test.test_common import client_with_db_empty as client
from web.user import ErrorMessages


def url(x):
    return f"http://localhost{x}"


def test_register(client):
    response = client.post('/register', data={'username': 'Oof_Aaa90_', 'password': 'foofoofoo'})
    assert response.headers['Location'] == url('/login')

    response = client.post('/register', data={'username': 'Oof_Aaa90_', 'password': 'foofoofoo'})
    # 200 = no redirect
    assert response.status_code == 200
    assert bytes(ErrorMessages.duplicate_username, 'utf') in response.data


def test_register_invalid(client):
    response = client.post('/register', data={'username': 'oof', 'password': 'foofoof'})
    assert response.status_code == 200
    assert bytes(ErrorMessages.invalid_password, 'utf') in response.data

    response = client.post('/register', data={'username': '', 'password': 'foofo'})
    assert response.status_code == 200
    assert bytes(ErrorMessages.non_empty_username, 'utf') in response.data

    response = client.post('/register', data={'username': 'F+_student', 'password': 'foofo'})
    assert response.status_code == 200
    assert bytes(ErrorMessages.invalid_username, 'utf') in response.data



def test_login_invalid(client):
    with client:
        response = client.post('/register', data={'username': 'oof', 'password': 'foofoofoo'})
        assert response.headers['Location'] == url('/login')
        assert 'user' not in session

        response = client.post('/login', data={'username': 'oof', 'password': 'foofoo'})
        assert response.status_code == 200
        assert 'user' not in session
        assert bytes(ErrorMessages.invalid_login, 'utf') in response.data

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
