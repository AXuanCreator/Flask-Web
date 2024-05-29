from flask import Blueprint, request, render_template, session, flash, redirect, url_for, jsonify
from services import UserService, Utils

# 初始化蓝图对象
user_bp = Blueprint('user', __name__)


@user_bp.route('/',methods=['GET'])
def home():
	return render_template('login.html')


@user_bp.route('/admin',methods=['GET'])
def admin():
	if session.get('admin'):
		return render_template('admin.html')

	flash('您并未表达出对流萤小姐的爱，无法登陆至管理员界面')
	return redirect(url_for('user.home'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		# 验证用户信息
		flag = UserService.check_user_login(username, password)
		if flag == 1:
			flash('登录成功')
			return redirect(url_for('user.home'))
		elif flag == 2:
			session['admin'] = True
			return redirect(url_for('user.admin'))
		else:
			flash('用户名或密码错误')

		return render_template('login.html')


@user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
	if session['admin'] and request.method == 'GET':
		session['admin'] = False  # 重置session
		return render_template('add_user.html')
	# 添加数据库数据
	if request.method == 'POST':
		add_username = request.form['add_u']
		add_password = request.form['add_p']

		# ORM对象
		if UserService.create_user(add_username, add_password):
			flash('成功添加用户')
		else:
			flash('添加用户失败')

	return redirect(url_for('user.home'))


@user_bp.route('/update_user', methods=['GET', 'POST'])
def update_user():
	if session['admin'] and request.method == 'GET':
		session['admin'] = False  # 重置session
		return render_template('update_user.html')

	# 更新数据库数据
	if request.method == 'POST':
		upd_id = request.form['upd_i']
		upd_username = request.form['upd_u']
		upd_password = request.form['upd_p']

		# 调用Service层
		if UserService.update_user(upd_id, upd_username, upd_password):
			flash('成功更新用户')
		else:
			flash('更新用户失败')

	return redirect(url_for('user.home'))


@user_bp.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
	if session['admin'] and request.method == 'GET':
		session['admin'] = False  # 重置session
		return render_template('delete_user.html')

	# 删除数据库数据
	if request.method == 'POST':
		del_i = request.form['del_i']

		# 调用Service层
		if UserService.delete_user(del_i):
			flash('成功删除用户')
		else:
			flash('删除用户失败')

	return redirect(url_for('user.home'))
