from flask import Blueprint, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required

developer_ctrl = Blueprint('developer_ctrl', __name__, url_prefix='/developer')

# Define admin permissions
developer_permission = Permission(RoleNeed('developer'))

@developer_ctrl.route('/dashboard', methods=['GET'])
@login_required
@developer_permission.require(http_exception=403)  # Only admin can access
def admin_dashboard():
    return jsonify({'message': 'Welcome to the admin dashboard'})

@developer_ctrl.errorhandler(403)
def permission_denied(e):
    return jsonify({'message': 'Access denied'}), 403