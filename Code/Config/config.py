############################### VERSION 1.0 ###############################
# 此模块用于设置Flask应用的配置
# 可以通过app.config.from_object(AppConfig)来读取所有参数
############################### VERSION 1.0 ###############################
class AppConfig():
	# MySQL
	HOSTNAME = '127.0.0.1'
	PORT = '3306'
	USERNAME = 'root'
	PASSWORD = '9966330'
	DATABASE = 'flask-web'  # 架构名

	SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'your_secret_key'

	# FLASK
	DEBUG = True


class DbConfig:
	pass


class UserConfig:
	MAX_BORROW_BOOKS = 30
	MAX_BORROW_DAYS = 30


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
	NAME_NOT_ALLOWED = 'NAMENOTALLOWED'


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
