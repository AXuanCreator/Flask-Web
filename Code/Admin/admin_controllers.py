from flask import Flask, Blueprint, request
from admin_services import AdminService
from Code.Utils.response import ResponseCode, Response

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    service_code = AdminService.login(username=username, password=password)
    if service_code == 1:
        admin = AdminService.get_admin_by_username(username)
        return Response.response(ResponseCode.LOGIN_SUCCESS, '登录成功', admin.id)
    if service_code == 0:
        return Response.response(ResponseCode.WRONG_PASSWORD, '密码错误', 0)
    if service_code == -1:
        return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, '管理员不存在', 0)

@admin_bp.route('/<int:id>', methods=['GET'])
def query_admin_info(id):
    """获取管理员的基本信息"""
    admin = AdminService.get_admin_by_id(id)
    if admin:
        return Response.response(ResponseCode.SUCCESS, '查询成功', admin)
    return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, '用户不存在', 0)

@admin_bp.route('/<int:id>', methods=['PUT'])
def modify_admin_info():
    """修改管理员的基本信息"""
    pass


@admin_bp.route('/<int:id>/password', methods=['PUT'])
def modify_admin_password():
    """修改管理员的登录密码"""
    pass
