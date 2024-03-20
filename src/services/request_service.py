import threading

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models import MeetingRequest, db, Account, AccountRequest, ActiveMeeting
from sqlalchemy import func, null
from geoalchemy2 import shape, WKTElement
from shapely import buffer, set_srid
import geopandas as gpd
import json


@jwt_required(optional=False)
def send_request():
    username = get_jwt_identity()
    account = Account.query.filter_by(username=username).first()
    request_exists = MeetingRequest.query.filter_by(id=account.id).first() is not None

    if request_exists:
        return jsonify({"error": "Request pending"}), 409

    to_shapely = set_srid(shape.to_shape(account.location), 4326)
    shapely_buffer = set_srid(buffer(to_shapely, .017, quad_segs=8, cap_style="square"), 4326)
    wkt_buffer = WKTElement(shapely_buffer.wkt, srid=4326)
    request_form = request.form.to_dict()

    new_request = MeetingRequest(
        message=request_form['message'],
        status="pending",
        buffer=wkt_buffer,
        account_id=account.id
    )

    db.session.add(new_request)
    db.session.commit()

    meeting_request = MeetingRequest.query.filter_by(account_id=account.id).first()

    account_request = AccountRequest(
        account_id=account.id,
        meeting_request_id=meeting_request.id
    )

    db.session.add(account_request)
    db.session.commit()

    # spatial search -

    receivers_list = db.session.query(Account, MeetingRequest).filter(
        func.ST_Within(account.location, meeting_request.buffer)).all()

    for receiver in receivers_list:
        if account.id != receiver[0].id and receiver[1].id == meeting_request.id:
            new_account_request = AccountRequest(
                account_id=receiver[0].id,
                meeting_request_id=meeting_request.id
            )
            db.session.add(new_account_request)
            db.session.commit()

    ## add meeting_request id to account object
    Account.query.filter_by(username=username).update(dict(record_id=meeting_request.id))
    db.session.commit()

    ## update existing Active Meeting if exists, otherwise create it Active meeting

    active_meeting_exists = ActiveMeeting.query.filter_by(account_id=account.id).first() is not None

    if active_meeting_exists:
        ActiveMeeting.query.filter_by(account_id=account.id).update(dict(meeting_request_id_=meeting_request.id))
        ActiveMeeting.query.filter_by(account_id=account.id).update(dict(location=account.location))
        db.session.commit()
    else:
        active_meeting = ActiveMeeting(
            firstname=account.firstname,
            lastname=account.lastname,
            location=account.location,
            account_id=account.id,
            meeting_request_id=account.record_id
        )
        db.session.add(active_meeting)
        db.session.commit()

    db.session.remove()
    return jsonify({
        "userMessage": "Request sent to users within 2km"
    })


@jwt_required(optional=False)
def delete():
    response = jsonify({"userMessage": "Request deleted"})
    username = get_jwt_identity()
    account = Account.query.filter_by(username=username).first()
    MeetingRequest.query.filter_by(id=account.id).delete()
    db.session.commit()

    Account.query.filter_by(username=username).update(dict(record_id=null))
    db.session.commit()

    db.session.remove()
    return response


@jwt_required(optional=False)
def request_list():
    username = get_jwt_identity()

    account = Account.query.filter_by(username=username).first()
    requests = AccountRequest.query.filter_by(account_id=account.id).all()

    if not requests:
        return jsonify({
            "userMessage": "No active requests. Check again later"
        })

    print(requests)

    print(type(requests))

    required_data = []

    for account_request in requests:
        sub_request = {}
        required_meeting_request = MeetingRequest.query.filter_by(id=account_request.meeting_request_id).first()
        sub_request['accountmessage'] = required_meeting_request.message
        owner_account = Account.query.filter_by(record_id=required_meeting_request.id).first()
        print(owner_account)
        print(type(owner_account))
        sub_request['firstname'] = owner_account.firstname
        sub_request['lastname'] = owner_account.lastname
        sub_request['meeting_request_id'] = required_meeting_request.id
        sub_request['account_id'] = owner_account.id
        sub_request['sex'] = owner_account.sex
        sub_request['created'] = required_meeting_request.created.strftime("%m/%d/%Y, %H:%M:%S")
        print(required_meeting_request.created.strftime("%m/%d/%Y, %H:%M:%S"))
        string_date = owner_account.dob.strftime("%Y")
        year_birth = int(string_date)
        age = 2024 - year_birth
        sub_request['age'] = age
        print(age)
        print(sub_request['age'])
        print(sub_request)
        print(type(sub_request))

        required_data.append(sub_request)

        print(required_data)
        print(type(required_data))

    json_data = json.dumps(required_data)
    db.session.remove()
    return jsonify({
        "userMessage": "Requests queried",
        "requiredData": json_data
    })


@jwt_required(optional=False)
def decline_request():
    username = get_jwt_identity()
    request_form = request.form.to_dict()
    request_id = request_form['meeting_request_id']

    account = Account.query.filter_by(username=username).first()
    AccountRequest.query.filter_by(account_id=account.id, meeting_request_id=request_id).delete()
    db.session.commit()
    response = jsonify({"userMessage": "Account Request deleted"})
    db.session.remove()
    return response


@jwt_required(optional=False)
def accept_request():
    username = get_jwt_identity()
    request_form = request.form.to_dict()
    meeting_request_id = request_form['meeting_request_id']

    account = Account.query.filter_by(username=username).first()

    active_meeting_exists = ActiveMeeting.query.filter_by(account_id=account.id).first() is not None

    if active_meeting_exists:
        ActiveMeeting.query.filter_by(account_id=account.id).update(dict(meeting_request_id_=meeting_request_id))
        ActiveMeeting.query.filter_by(account_id=account.id).update(dict(location=account.location))
        db.session.commit()
    else:
        active_meeting = ActiveMeeting(
            firstname=account.firstname,
            lastname=account.lastname,
            location=account.location,
            account_id=account.id,
            meeting_request_id=meeting_request_id
        )
        db.session.add(active_meeting)
        db.session.commit()

    # Once request accepted or declined, user no longer in pending status
    AccountRequest.query.filter_by(account_id=account.id).delete()
    db.session.commit()

    meeting_request = MeetingRequest.query.filter_by(id=meeting_request_id).first()

    response = {
        "created": meeting_request.created,
        "userMessage": account.username + " is registered for the meeting. Wait for participants to join: "
    }

    db.session.remove()
    return response
