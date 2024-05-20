################################################################################
# 1. 本文件为登陆界面的后端逻辑
# 2. 使用Flask框架，实现用户登录、注册、管理员、数据库添加用户等功能
# 3. 该示例的ORM模型位于models.py中，数据库配置位于本文件
# 4. 本文件使用到了两个模板文件：login.html和admin.html，但仅用于示例，推荐前后端分离
################################################################################

from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User

# MySQL配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '9966330'
DATABASE = 'flask-web'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.secret_key = 'your_secret_key'

db.init_app(app)
with app.app_context():
	db.create_all()

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/admin')
def admin():
	if session.get('admin'):
		session['admin'] = False  # 重置session
		return render_template('add_user.html')

	flash('您并未表达出对流萤小姐的爱，无法登陆至管理员界面')
	return redirect(url_for('home'))

@app.route('/add_user', methods=['POST'])
def add_user():
	# 添加数据库数据
	if request.method == 'POST':
		add_username = request.form['add_u']
		add_password = request.form['add_p']

		# ORM对象
		user = User(username=add_username, password=add_password)
		db.session.add(user)
		db.session.commit()

		flash('成功添加用户')

	return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	# 处理登录请求，login.html中使用到form表当，并为Post请求
	# 因此可以通过request.form获取表单数据
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		# 验证用户信息
		query_user = User.query.filter_by(username=username, password=password).first()
		if query_user and username in query_user.username and password == query_user.password:
			flash('登录成功')
			return redirect(url_for('home'))
		elif username=='admin' and password=='i love firefly':
			session['admin'] = True
			return redirect(url_for('admin'))
		else:
			flash('用户名或密码错误')

		return render_template('login.html')



if __name__ == '__main__':
	app.run(debug=True)