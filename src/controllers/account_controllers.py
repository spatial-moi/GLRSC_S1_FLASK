from src.services.account_service import generate_account, login_token, access_account, \
    account_logout, delete_account, change_password, store_geolocation

import threading
# ----------------------------------------------- #

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522


def generate():
    return generate_account()


def login():
    return login_token()


def access():
    return access_account()


def logout():
    return account_logout()


def delete():
    return delete_account()


def password():
    return change_password()


def store_location():
    return store_geolocation()
