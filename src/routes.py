from flask import Blueprint
from src.controllers.account_controllers import (generate, login, access, logout, delete, password,
                                                 store_location)
from src.controllers.request_controllers import request, delete_request, get_requests, decline, accept
from src.controllers.meeting_controllers import get_midpoint, get_owner_midpoint

account_bp = Blueprint('accounts', __name__)
request_bp = Blueprint('requests', __name__)
meeting_bp = Blueprint('meetings', __name__)

account_bp.route('/generate', methods=['POST'])(generate)
account_bp.route('/login_token', methods=['POST'])(login)
account_bp.route('/account')(access)
account_bp.route('/logout', methods=["POST"])(logout)
account_bp.route('/delete', methods=['DELETE'])(delete)
account_bp.route('/password', methods=['PATCH'])(password)
account_bp.route('/store_location', methods=['PATCH'])(store_location)

request_bp.route('/send_request', methods=["POST"])(request)
request_bp.route('/delete_request', methods=['DELETE'])(delete_request)
request_bp.route('/requests')(get_requests)
request_bp.route('/declineRequest', methods=['DELETE'])(decline)
request_bp.route('/acceptRequest', methods=['POST'])(accept)

meeting_bp.route('/getMidpoint', methods=['POST'])(get_midpoint)
meeting_bp.route('/getOwnerMidpoint', methods=['PATCH'])(get_owner_midpoint)







