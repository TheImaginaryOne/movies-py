from flask import session, current_app

from domainmodel.repository import Repository


class InvalidUser(Exception):
    pass


def is_logged_in(repository: Repository):
    return 'user' in session and repository.has_user(session['user'])


def login(repository: Repository, username, password):
    user_id = repository.login(username, password)

    current_app.logger.info(f"Login ({username})")
    if user_id is not None:
        current_app.logger.info("Login successful")
        session.clear()
        session['user'] = user_id
        return True

    return False


def register(repository: Repository, username, password):
    if repository.add_user(username, password):
        current_app.logger.info(f"Register ({username})")
        return True
    return False


