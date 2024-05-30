from flask import Flask
from Config import User
from Config.helper import ReturnCode
class UserServices:
	## SELECT ##
	@staticmethod
	def get_user_all():
		return User.query.all()

	@staticmethod
	def get_user_id(id):
		return User.query.get(id)

	@staticmethod
	def get_user_username(username):
		return User.query.filter_by(username=username)

	@staticmethod
	def get_user_mail(mail):
		return User.query.filter_by(mail=mail)

	## UPDATE ##
	@staticmethod
	def update_user_id(id, user_request):
		db_user = User.query.get(id)
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		# 使用列表推导式赋值
		request_keys = ['username', 'name', 'gender', 'phone', 'mail']
		username, name, gender, phone, mail = (user_request.get(key) for key in request_keys)




