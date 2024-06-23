from flask import Flask, Blueprint, request
from .admin_services import AdminService
from Utils import ResponseCode, Response
from Utils import Helper

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    res_code = AdminService.login(username=username, password=password)
    if res_code == 1:
        admin = AdminService.get_admin_by_username(username)
        return Response.response(ResponseCode.LOGIN_SUCCESS, '登录成功', admin.id)
    if res_code == 0:
        return Response.response(ResponseCode.WRONG_PASSWORD, '密码错误', 0)
    if res_code == -1:
        return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, '管理员不存在', 0)


@admin_bp.route('/<int:id>', methods=['GET', 'PUT'])
def admin_info(id):
    if request.method == 'GET':
        """获取管理员的基本信息"""
        admin = AdminService.get_admin_by_id(id)
        if admin:
            return Response.response(ResponseCode.SUCCESS, '查询成功', Helper.to_dict(admin))
        return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, '用户不存在', 0)
    elif request.method == 'PUT':
        """修改管理员的基本信息"""
        res_code = AdminService.update_admin(id, request.get_json())
        if res_code == 1:
            return Response.response(ResponseCode.SUCCESS, '修改成功', id)
        if res_code == -1:
            return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, '管理员不存在', 0)
        return Response.response(ResponseCode.FAILED, '系统错误', 0)


@admin_bp.route('/<int:id>/password', methods=['PUT'])
def modify_admin_password(id):
    """修改管理员的登录密码"""
    res_code = AdminService.update_password(id, request.get_json())
    if res_code == 1:
        return Response.response(ResponseCode.SUCCESS, '修改成功', id)
    if res_code == -1:
        return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, '管理员不存在', 0)
    if res_code == 0:
        return Response.response(ResponseCode.WRONG_PASSWORD, '密码错误', 0)
