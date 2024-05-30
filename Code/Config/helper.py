import re

from db_models import User


class ReturnCode:
	SUCCESS = 'SUCCESS'
	FAIL = 'FAIL'
	USERNAME_NOT_ALLOWED = 'USERNAMENOTALLOWED'
	USERNAME_REPEATED = 'USERNAMEREPEATED'
	PASSWORD_NOT_ALLOWED = 'PASSWORDNOTALLOWED'
	GENDER_NOT_ALLOWED = 'GENDERNOTALLOWED'
	MAIL_NOT_ALLOWED = 'MAILNOTALLOWED'
	MAIL_REPEATED = 'MAILREPEATED'
	INFO_NOT_ALLOWED = 'INFONOTALLOWED'
	USER_NOT_EXIST = 'USERNOTEXIST'


class Regex:
	"""
	正则表达式
	^ ：表示开头
	a-z ：表示匹配小写字母
	[...] ：表示一个字符的规则
	* ：表示前面的[...]可以有零次或多次
	{a,b} ：表示前面的符合[...]的字符至少有a个，至多有b个
	(?=.*[...]) ：正向肯定预查，表示字符串里至少包含一个符合[...]规则的字符
	"""
	username_pattern = r'^[a-zA-Z][a-zA-Z0-9]{4,}$'
	password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$'
	mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'


class RuleCheck:
	gender_set = {'男', '女', '男人', '女人', '男性', '女性', '沃尔玛购物袋', '武装直升机', 'man', 'lady'}
	@staticmethod
	def check_username_not_repeat(username: str):
		return User.query.filter_by(username) is None

	@staticmethod
	def check_username_in_rules(username: str):
		return len(username) <= 80 and re.match(Regex.username_pattern, username) is not None

	@staticmethod
	def check_password_in_rules(password: str):
		return len(password) <= 80 and re.match(Regex.password_pattern, password) is not None

	@staticmethod
	def check_gender_in_rules(gender: str):
		return len(gender) <= 20 and gender.lower() in RuleCheck.gender_set

	@staticmethod
	def check_mail_in_rules(mail: str):
		return len(mail) <= 80 and re.match(Regex.mail_pattern, mail) is not None