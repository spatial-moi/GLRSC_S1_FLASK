from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, unset_jwt_cookies, jwt_required
from bcrypt import _bcrypt
from src.models import Account, db
from geoalchemy2 import WKTElement
import threading


# you can now use some_session to run multiple queries, etc.
# remember to close it when you're finished!


def generate_account():
    print("runs generate account")
    request_form = request.form.to_dict()
    username = request_form['username']
    password = request_form['password']
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    # Check if account exists

    db.session.begin()
    account_exists = Account.query.filter_by(username=username).first() is not None

    if account_exists:
        return jsonify({"error": "Username already in user"}), 409
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    salt = _bcrypt.gensalt()
    pw_hash = _bcrypt.hashpw(password.encode('utf-8'), salt)

    new_account = Account(
        username=username,
        password=pw_hash,
        dob=request_form['dob'],
        city=request_form['city'],
        sex=request_form['sex'],
        firstname=request_form['firstname'],
        lastname=request_form['lastname']
    )
    username = new_account.username
    try:

        db.session.add(new_account)
        print(threading.active_count())
        print(threading.current_thread())
        print(threading.enumerate())
        db.session.commit()
        print(threading.active_count())
        print(threading.current_thread())
        print(threading.enumerate())
    finally:
        db.session.remove()
        print(threading.active_count())
        print(threading.current_thread())
        print(threading.enumerate())

    return jsonify({
        "userMessage": "Account generated, Welcome " + username
    })


def login_token(cryptor=None):
    print("runs login token")
    request_form = request.form.to_dict()
    username = request_form['username']
    password = request_form['password']

    try:
        db.session.begin()
        account = Account.query.filter_by(username=username).first()
    finally:
        db.session.remove()

    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    if account is None:
        return jsonify({"error": "Wrong email or password"}), 401

    if not _bcrypt.checkpw(password.encode('utf-8'), account.password):
        return jsonify({"error": "Unauthorized"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({
        "userMessage": "Successfully logged in, " + username,
        "username": username,
        "access_token": access_token
    })


@jwt_required(optional=False)
def access_account():
    db.session.begin()
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    print('runs access account')
    username = get_jwt_identity()
    account = Account.query.filter_by(username=username).first()

    response_body = {
        "firstname": account.firstname,
        "lastname": account.lastname,
        "username": account.username,
        "dob": account.dob,
        "city": account.city,
        "sex": account.sex,
        "userMessage": "Account accessed"
    }
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    db.session.remove()
    return response_body


@jwt_required(optional=False)
def account_logout():
    response = jsonify({"userMessage": "Account logged out"})
    unset_jwt_cookies(response)
    db.session.remove()
    return response


@jwt_required(optional=False)
def delete_account():
    response = jsonify({"userMessage": "Account deleted"})
    username = get_jwt_identity()
    Account.query.filter_by(username=username).delete()
    try:
        db.session.commit()
    finally:
        db.session.close_all()
    db.session.remove()
    return response


@jwt_required(optional=False)
def change_password():
    request_form = request.form.to_dict()
    new_password = request_form['new_password']
    username = get_jwt_identity()
    salt = _bcrypt.gensalt()
    new_pw_hash = _bcrypt.hashpw(new_password.encode('utf-8'), salt)
    try:
        Account.query.filter_by(username=username).update(dict(password=new_pw_hash))
        db.session.commit()
    finally:
        db.session.close_all()
    db.session.remove()
    return jsonify({"userMessage": "Password successfully changed"})


@jwt_required(optional=False)
def store_geolocation():
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    request_form = request.form.to_dict()
    latitude = request_form['latitude']
    longitude = request_form['longitude']
    username = get_jwt_identity()
    point = WKTElement('POINT({0} {1})'.format(longitude, latitude), srid=4326)

    try:
        Account.query.filter_by(username=username).update(dict(location=point))
        db.session.commit()
        db.session.close()
    finally:
        db.session.close_all()
    db.session.remove()
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    return jsonify({"userMessage": "Private location stored in database",
                    "latitude": latitude,
                    "longitude": longitude
                    })
