from flask import Blueprint
from src.controllers.account_controllers import (generate, login, access, logout, delete, password,
                                                 store_location)
account_bp = Blueprint('accounts', __name__)

account_bp.route('/generate', methods=['POST'])(generate)
account_bp.route('/login_token', methods=['POST'])(login)
account_bp.route('/account')(access)
account_bp.route('/logout', methods=["POST"])(logout)
account_bp.route('/delete', methods=['DELETE'])(delete)
account_bp.route('/password', methods=['PATCH'])(password)
account_bp.route('/store_location', methods=['PATCH'])(store_location)
