from flask import Flask, request, jsonify
from flask_cors import CORS

from Config import db, AppConfig
from Admin import admin_bp
from Book import book_bp
from User import user_bp

def create_app():
	# 创建Flask应用实例，对所有域名开放
	app = Flask(__name__)
	CORS(app)

	# 读取所有参数
	app.config.from_object(AppConfig)

	# 加载蓝图
	app.register_blueprint(user_bp, url_prefix='/user')
	app.register_blueprint(book_bp, url_prefix='/book')
	app.register_blueprint(admin_bp, url_prefix='/admin')

	# 初始化数据库
	db.init_app(app)
	with app.app_context():
		db.create_all()  # 将ORM模型同步至数据库

	return app


if __name__ == '__main__':
	app = create_app()
	app.run()