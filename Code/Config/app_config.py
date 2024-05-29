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
