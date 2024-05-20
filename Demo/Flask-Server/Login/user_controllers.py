from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from services import UserService

# 初始化蓝图对象
user_bp = Blueprint('user', __name__)
@user_bp.route('/')
def home():
	return render_template('login.html')

@user_bp.route('/admin')
def admin():
	if session.get('admin'):
		session['admin'] = False  # 重置session
		return render_template('add_user.html')

	flash('您并未表达出对流萤小姐的爱，无法登陆至管理员界面')
	return redirect(url_for('home'))

@user_bp.route('/add_user', methods=['POST'])
def add_user():
	# 添加数据库数据
	if request.method == 'POST':
		add_username = request.form['add_u']
		add_password = request.form['add_p']

		# ORM对象
		if UserService.create_user(add_username, add_password):
			flash('成功添加用户')
		else:
			flash('添加用户失败')

	return redirect(url_for('home'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
	# 处理登录请求，login.html中使用到form表当，并为Post请求
	# 因此可以通过request.form获取表单数据
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		# 验证用户信息
		query_user = UserService.get_user_by(username=username).first()  # username是唯一的，因此只取第一个
		if query_user and username in query_user.username and password == query_user.password:
			flash('登录成功')
			return redirect(url_for('home'))
		elif username=='admin' and password=='i love firefly':
			session['admin'] = True
			return redirect(url_for('admin'))
		else:
			flash('用户名或密码错误')

		return render_template('login.html')