from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

## 设置app.config中关于数据库的参数
## SQLAlchemy(app)会自动从app.config中读取数据库的配置
# MySQL所在的主机名
HOSTNAME = '127.0.0.1'
# MySQL的监听端口号，默认3306
PORT = '3306'
# MySQL的用户名，在安装MySQL时由用户创建
USERNAME = 'root'
# MySQL的密码，在安装MySQL时由用户创建
PASSWORD = '150181'
# MySQL的数据库名
DATABASE = 'demo'

# 创建app应用
app = Flask(__name__)
# 应用到app.config中
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
# 连接SQLAlchemy到Flask应用
db = SQLAlchemy(app)

# 使用Migrate对象将ORM模型映射成表需要四步
# 1. 创建Migrate对象，并传入app和db
# 2. 在命令行中输入 flask db init 初始化迁移仓库，会在项目目录下生成一个migrations文件夹。该步骤仅需执行一次
# 3. 在命令行中输入 flask db migrate 生成迁移脚本，该步骤会根据ORM模型生成迁移脚本，需要每次更新ORM模型后执行
# 4. 在命令行中输入 flask db upgrade 将迁移脚本同步到数据库中，需要每次更新ORM模型后执行
migrate = Migrate(app, db)

# 表：作者
class Author(db.Model):
	__tablename__ = 'author'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(80), nullable=False)
	age = db.Column(db.Integer, nullable=False)

with app.app_context():
	db.create_all()


if __name__ == '__main__':
	app.run()
