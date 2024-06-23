from flask import Blueprint, request, render_template
from Utils.response import ResponseCode, Response
from Utils.helper import Helper
from Borrow.borrow_services import BorrowService

borrow_bp = Blueprint('borrow', __name__)


########################################################################
# 真实URL为 /borrow
# GET请求：查询某个特定信息的借阅列表
# POST请求：借阅书籍
########################################################################
@borrow_bp.route('/', methods=['GET', 'POST'])
def book_borrow():
	if request.method == 'GET':
		res = BorrowService.list_borrow(request.args)
		return Response.response(ResponseCode.SUCCESS, '查询成功', [Helper.to_dict(e) for e in res])
	elif request.method == 'POST':
		res_code = BorrowService.borrow_book(request.form)
		if res_code == -3:
			return render_template('error.html', output='图书已借阅')
		if res_code == -2:
			return render_template('error.html', output='图书不存在')
		if res_code == -1:
			return render_template('error.html', output='用户不存在')
		if res_code == 0:
			return render_template('error.html', output='借阅受限')
		if res_code > 0:
			return Response.response(ResponseCode.SUCCESS, '借阅成功', res_code)


########################################################################
# 真实URL为 /borrow/<id>/return
# POST请求：归还书籍
########################################################################
@borrow_bp.route('/<id>/return', methods=['POST'])
def return_book(id):
	res_code = BorrowService.return_book(id)
	if res_code == -2:
		return render_template('error.html', output='借阅记录不存在')
	if res_code == -1:
		return render_template('error.html', output='无法重复归还')
	if res_code == 0:
		return Response.response(ResponseCode.RETURN_OVERDUE, '逾期归还', 0)
	if res_code == 1:
		return Response.response(ResponseCode.SUCCESS, '归还成功', id)


########################################################################
# 真实URL为 /borrow/<id>/return
# POST请求：续借书籍
########################################################################
@borrow_bp.route('/<id>/renew', methods=['POST'])
def renew_book(id):
	res_code = BorrowService.renew_book(id)
	if res_code == -2:
		return render_template('error.html', output='借阅记录不存在')
	if res_code == -1:
		return render_template('error.html', output='图书已归还')
	if res_code == 0:
		return render_template('error.html', output='借阅逾期，请先归还')
	if res_code == 1:
		return Response.response(ResponseCode.SUCCESS, '续借成功', id)
