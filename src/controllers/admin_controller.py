from flask import Blueprint, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required

admin_ctrl = Blueprint('admin_ctrl', __name__, url_prefix='/admin')

# Define permissions
admin_permission = Permission(RoleNeed('admin'))

@admin_ctrl.route('/dashboard', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)  # Only admin can access
def admin_dashboard():
    return jsonify({'message': 'Welcome to the admin dashboard'})

@admin_ctrl.errorhandler(403)
def permission_denied(e):
    return jsonify({'message': 'Access denied'}), 403
