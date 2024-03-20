from src.services.meeting_service import midpoint, get_requestor_midpoint


def get_midpoint():
    return midpoint()


def get_owner_midpoint():
    return get_requestor_midpoint()
