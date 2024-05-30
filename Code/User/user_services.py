from flask import Flask
from Config import User, ReturnCode, RuleCheck, db, UserConfig
from User.Mail import SendMail

class UserDao:
	# ## SELECT是不必要的 ##
	# @staticmethod
	# def get_user_all():
	# 	return User.query.all()
	#
	# @staticmethod
	# def get_user_id(id):
	# 	db_user = User.query.get(id)
	#
	# @staticmethod
	# def get_user_username(username):
	# 	return User.query.filter_by(username=username)
	#
	# @staticmethod
	# def get_user_mail(mail):
	# 	return User.query.filter_by(mail=mail)

	## UPDATE ##
	@staticmethod
	def update_user_id(id, user_request):
		db_user = User.query.get(id)
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		# 使用列表推导式赋值
		request_keys = ['username', 'name', 'password', 'gender', 'phone', 'mail']
		username, password, name, gender, phone, mail = (user_request.get(key) for key in request_keys)

		# 检测
		if username is not None and not RuleCheck.check_username_in_rules(username):
			return ReturnCode.USERNAME_NOT_ALLOWED
		if username is not None and RuleCheck.check_username_not_repeat(username):
			return ReturnCode.USERNAME_REPEATED
		if gender is not None and not RuleCheck.check_gender_in_rules(gender):
			return ReturnCode.GENDER_NOT_ALLOWED
		if mail is not None and not RuleCheck.check_mail_in_rules(mail):
			return ReturnCode.MAIL_NOT_ALLOWED
		if mail is not None and not RuleCheck.check_mail_not_repeat(mail):
			return ReturnCode.MAIL_REPEATED

		db_user.username = username if username is not None else db_user.username
		db_user.name = name if name is not None else db_user.name
		db_user.gender = gender if gender is not None else db_user.gender
		db_user.phone = phone if phone is not None else db_user.phone
		db_user.mail = mail if mail is not None else db_user.mail
		db.session.commit()

		return ReturnCode.SUCCESS

	@staticmethod
	def update_user_password(id, password):
		db_user = User.query.get(id)
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		if password is None:
			return ReturnCode.FAIL

		if not RuleCheck.check_password_in_rules(password):
			return ReturnCode.PASSWORD_NOT_ALLOWED

		db_user.password = password
		db.session.commit()

		return ReturnCode.SUCCESS


	## DELETE ##
	@staticmethod
	def delete_user_id(id):
		delete_user = User.query.get(id)
		if delete_user is None:
			return ReturnCode.USER_NOT_EXIST

		db.session.delete(delete_user)
		db.session.commit()

		return ReturnCode.SUCCESS

	## INSERT ##
	@staticmethod
	def insert_user(user_request):
		result_keys = ['username', 'password', 'name', 'gender', 'phone', 'mail']
		username, password, name, gender, phone, mail = (user_request.get(key) for key in result_keys)

		# TODO:封装
		if username is None or not RuleCheck.check_username_in_rules(username):
			return ReturnCode.USERNAME_NOT_ALLOWED
		if username is None or not RuleCheck.check_username_not_repeat(username):
			return ReturnCode.USERNAME_REPEATED
		if password is None or not RuleCheck.check_password_in_rules(password):
			return ReturnCode.PASSWORD_NOT_ALLOWED
		if name is None:
			return ReturnCode.INFO_NOT_ALLOWED
		if gender is None or not RuleCheck.check_gender_in_rules(gender):
			return ReturnCode.GENDER_NOT_ALLOWED
		if phone is None:
			return ReturnCode.INFO_NOT_ALLOWED
		if mail is None or not RuleCheck.check_mail_in_rules(mail):
			return ReturnCode.MAIL_NOT_ALLOWED
		if mail is None or not RuleCheck.check_mail_not_repeat(mail):
			return ReturnCode.MAIL_REPEATED

		insert_user = User(username=username, password=password, name=name, gender=gender, phone=phone, mail=mail,
		                   max_borrow_days=UserConfig.MAX_BORROW_DAYS, max_borrow_books=UserConfig.MAX_BORROW_BOOKS)
		db.session.add(insert_user)
		db.session.commit()

		return ReturnCode.SUCCESS


class UserServices:
	@staticmethod
	def login(username, password):
		db_user = User.query.filter_by(username=username).first()  # username为Unique，所以不会出现查询到多条记录的情况
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		if password != db_user.password:
			return ReturnCode.PASSWORD_NOT_ALLOWED

		return ReturnCode.SUCCESS

	@staticmethod
	def register(user_request):
		return UserDao.insert_user(user_request)

	@staticmethod
	def deregister(id):
		return UserDao.delete_user_id(id)

	@staticmethod
	def change_password(id, user_request):
		return UserDao.update_user_id(id, user_request)

	@staticmethod
	def update_user(id, user_request):
		return UserDao.update_user_id(id, user_request)

	@staticmethod
	def send_mail(mail):
		SendMail.generate_random_code(mail)
		return SendMail.send_mail(mail)