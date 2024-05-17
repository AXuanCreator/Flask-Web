from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

## 设置app.config中关于数据库的参数
## SQLAlchemy(app)会自动从app.config中读取数据库的配置
# MySQL所在的主机名
HOSTNAME = '127.0.0.1'
# MySQL的监听端口号，默认3306
PORT = '3306'
# MySQL的用户名，在安装MySQL时由用户创建
USERNAME = 'root'
# MySQL的密码，在安装MySQL时由用户创建
PASSWORD = '9966330'
# MySQL的数据库名
DATABASE = 'exp_1'
# 应用到app.config中
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

# 创建数据库
db = SQLAlchemy(app)

# 测试数据库是否已连接
# with app.app_context():
# 	with db.engine.connect() as conn:
# 		# 使用text函数将字符串转换为可执行的SQLAlchemy对象
# 		rs = conn.execute(text('select 1'))
# 		print(rs.fetchone())  # Success : (1,)

class User(db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True, nullable=False)  # varchar
	password = db.Column(db.String(80), nullable=False)

# 等价==>MySQL: INSERT USER(username,password) VALUES('firefly', 'i will set the seas ablaze')
user = User(id=1,username='firefly', password='i will set the seas ablaze')

with app.app_context():
	db.create_all()  # 同步数据库

@app.route('/')
def index():
	return

if __name__ == '__main__':
	app.run(debug=True)
