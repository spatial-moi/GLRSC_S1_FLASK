from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from src.models import Account, ActiveMeeting, db, AccountRequest
from geoalchemy2 import shape
import threading
from src.services import osmnx_service


def identify_partner(active_meeting, account):
    for meeting in active_meeting:
        if meeting.location != account.location:
            return meeting


def check_meetings(active_meeting, account):
    ## create origin node
    origin_point = shape.to_shape(account.location)
    origin_lon = origin_point.x
    origin_lat = origin_point.y
    origin_tuple = (origin_lat, origin_lon)
    longitudes = []
    latitudes = []
    for meeting in active_meeting:
        print(len(active_meeting))
        if len(active_meeting) != 2:
            print("More than two participants")
            origin_point = shape.to_shape(account.location)
            origin_lon = origin_point.x
            origin_lat = origin_point.y
            longitudes.append(origin_lon)
            latitudes.append(origin_lat)
            break

    if len(active_meeting) == 2:
        participants_meeting = identify_partner(active_meeting, account)
        dest_point = shape.to_shape(participants_meeting.location)
        dest_lon = dest_point.x
        dest_lat = dest_point.y
        destination = (dest_lat, dest_lon)
        print("just two participants")
        return osmnx_service.midpoint_two(origin_tuple, destination)

    requestor_record = ActiveMeeting.query.filter_by(owner=1).first()
    requestor_point = shape.to_shape(requestor_record.location)
    requestor_lon = requestor_point.x
    requestor_lat = requestor_point.y
    requestor_tuple = (requestor_lat, requestor_lon)
    return osmnx_service.midpoint_more(origin_tuple, longitudes, latitudes, requestor_tuple)


@jwt_required(optional=False)
def midpoint():
    username = get_jwt_identity()
    print(threading.active_count())

    account = Account.query.filter_by(username=username).first()

    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())
    request_form = request.form.to_dict()

    request_id = request_form['meeting_request_id']

    active_meeting = ActiveMeeting.query.filter_by(meeting_request_id=request_id).all()
    print(active_meeting)

    route_info = check_meetings(active_meeting, account)
    print("route info returned")
    print(route_info)
    print(type(route_info))
    db.session.commit()
    db.session.remove()
    return jsonify({
        "userMessage": "Midpoint Identified: " + str(route_info[1][1]) + ", " + str(route_info[1][0]) + ". Walk to "
                                                                                                        "the "
                                                                                                        "designated "
                                                                                                        "location "
                                                                                                        "for "
                                                                                                        "your "
                                                                                                        "meeting. Arrive within 15 minutes.",
        "route_info": route_info
    })


def r_check_meetings(active_meeting, account):
    ## create origin node
    origin_point = shape.to_shape(account.location)
    origin_lon = origin_point.x
    origin_lat = origin_point.y
    origin_tuple = (origin_lat, origin_lon)
    longitudes = []
    latitudes = []
    for meeting in active_meeting:
        print(len(active_meeting))
        if len(active_meeting) != 2:
            print("More than two participants")
            origin_point = shape.to_shape(account.location)
            origin_lon = origin_point.x
            origin_lat = origin_point.y
            longitudes.append(origin_lon)
            latitudes.append(origin_lat)
            break

    if len(active_meeting) == 2:
        participants_meeting = identify_partner(active_meeting, account)
        dest_point = shape.to_shape(participants_meeting.location)
        dest_lon = dest_point.x
        dest_lat = dest_point.y
        destination = (dest_lat, dest_lon)
        print("just two participants")
        return osmnx_service.r_midpoint_two(origin_tuple, destination)

    return osmnx_service.r_midpoint_more(origin_tuple, longitudes, latitudes)


@jwt_required(optional=False)
def get_requestor_midpoint():
    username = get_jwt_identity()
    account = Account.query.filter_by(username=username).first()
    active_meeting = ActiveMeeting.query.filter_by(meeting_request_id=account.record_id).all()

    if len(active_meeting) == 1:
        AccountRequest.query.filter_by(account_id=account.id, meeting_request_id=account.record_id).delete()
        ActiveMeeting.query.filter_by(meeting_request_id=account.record_id).delete()
        db.session.commit()
        return jsonify({
            "userMessage": "No users have registered for this meeting",
            "route_info": "None",
        })

    route_info = r_check_meetings(active_meeting, account)
    db.session.commit()
    db.session.remove()

    return jsonify({
        "userMessage": "Midpoint Identified: " + str(route_info[1][1]) + ", " + str(route_info[1][0]) + ". Walk to "
                                                                                                        "the "
                                                                                                        "designated "
                                                                                                        "location "
                                                                                                        "for "
                                                                                                        "your "
                                                                                                        "meeting. Arrive within 15 minutes. ",
        "route_info": route_info
    })
