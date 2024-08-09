from flask import Blueprint, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required

local_admin_ctrl = Blueprint('local_admin_ctrl', __name__, url_prefix='/local-admin')

# Define local admin permissions
local_admin_permission = Permission(RoleNeed('local_admin'))

@local_admin_ctrl.route('/dashboard', methods=['GET'])
@login_required
@local_admin_permission.require(http_exception=403)  # Only local admin can access
def local_admin_dashboard():
    return jsonify({'message': 'Welcome to the local admin dashboard'})

@local_admin_ctrl.errorhandler(403)
def permission_denied(e):
    return jsonify({'message': 'Access denied'}), 403