from src.services.request_service import send_request, delete, request_list, decline_request, accept_request


def request():
    return send_request()


def delete_request():
    return delete()


def get_requests():
    return request_list()


def decline():
    return decline_request()

def accept():
    return accept_request()
