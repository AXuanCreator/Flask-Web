################################################################################
# 1. 本组件Login为登陆界面的后端逻辑
# 2. 使用Flask框架，实现用户登录、注册、管理员、数据库编辑用户等功能
# 3. 本组件分为三层：Service、Controller、Model，分别实现业务逻辑、控制器、数据库模型
# 4. 其中，user_controllers.py使用蓝图管理。
# 4. 本文件使用到了两个模板文件：login.html和admin.html，但仅用于示例，推荐前后端分离
################################################################################

from flask import Flask
from flask_cors import CORS

from models import db
from config import Config

from user_controllers import user_bp
def create_app():
	# 创建Flask应用实例
	app = Flask(__name__)
	CORS(app)

	app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
	app.config['SECRET_KEY'] = Config.SECRET_KEY

	app.register_blueprint(user_bp)

	# 初始化数据库
	db.init_app(app)

	with app.app_context():
		db.create_all()

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(debug=True)
