#!/user/bin/env python3
# -*- coding: utf-8 -*-
from Config import Admin, db


class AdminService:

    @staticmethod
    def get_admin_by_id(id):
        return Admin.query.get(id)

    @staticmethod
    def get_admin_by_username(username):
        return Admin.query.filter_by(username=username).first()

    @staticmethod
    def login(username, password):
        """
        :return: -1：管理员不存在；0：密码错误；1：登陆成功
        """
        login_admin = Admin.query.filter_by(username=username).first()
        if login_admin:
            if login_admin.password == password:
                return 1
            return 0
        return -1

    @staticmethod
    def update_password(id, password):
        origin_password = password.get('origin_password')
        new_password = password.get('new_password')
        updated_admin = Admin.query.get(id)
        if updated_admin:
            if updated_admin.password != origin_password:
                return 0
            updated_admin.password = new_password if password is not None else updated_admin.password
            return 1
        return -1

    @staticmethod
    def update_admin(id, info_json):
        """
        更新用户信息
        :param id:用户 id
        :param info_json: 请求体 json
        :return: -1：管理员不存在；1：修改成功
        """
        update_field = ['username', 'name', 'phone', 'email']
        username, name, phone, email = (
            info_json.get(key) for key in update_field)
        updated_admin = Admin.query.get(id)
        if updated_admin:
            updated_admin.username = username if username is not None else updated_admin.username
            updated_admin.name = name if name is not None else updated_admin.name
            updated_admin.phone = phone if phone is not None else updated_admin.phone
            updated_admin.email = email if email is not None else updated_admin.email
            db.session.commit()
            return 1
        return -1
