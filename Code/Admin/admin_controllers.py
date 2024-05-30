from flask import Flask, Blueprint

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['POST'])
def login():
    """管理员登录"""
    pass


@admin_bp.route('/<int:id>', methods=['GET'])
def query_admin_info():
    """获取管理员的基本信息"""
    pass


@admin_bp.route('/<int:id>', methods=['PUT'])
def modify_admin_info():
    """修改管理员的基本信息"""
    pass


@admin_bp.route('/<int:id>/password', methods=['PUT'])
def modify_admin_password():
    """修改管理员的登录密码"""
    pass
