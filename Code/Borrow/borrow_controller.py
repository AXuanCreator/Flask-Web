from flask import Blueprint, request, render_template
from Utils.response import ResponseCode, Response
from Utils.helper import Helper
from Borrow.borrow_services import BorrowService

borrow_bp = Blueprint('borrow', __name__)

@borrow_bp.route('', methods=['GET'])
def query_borrow():
    res = BorrowService.list_borrow(request.args)
    return Response.response(ResponseCode.SUCCESS, '查询成功', [Helper.to_dict(e) for e in res])

@borrow_bp.route('', methods=['POST'])
def add_borrow():
    res_code = BorrowService.borrow_book(request.get_json())
    if res_code == -3:
        return render_template('error.html',output='图书已借阅')
    if res_code == -2:
        return render_template('error.html',output='图书不存在')
    if res_code == -1:
        return render_template('error.html',output='用户不存在')
    if res_code == 0:
        return render_template('error.html',output='借阅受限')
    if res_code > 0:
        return Response.response(ResponseCode.SUCCESS, '借阅成功', res_code)

@borrow_bp.route('/<id>/return', methods=['PUT'])
def return_book(id):
    res_code = BorrowService.return_book(id)
    if res_code == -2:
        return render_template('error.html',output='借阅记录不存在')
    if res_code == -1:
        return render_template('error.html',output='无法重复归还')
    if res_code == 0:
        return Response.response(ResponseCode.RETURN_OVERDUE, '逾期归还', 0)
    if res_code == 1:
        return Response.response(ResponseCode.SUCCESS, '归还成功', id)

@borrow_bp.route('/<id>/renew', methods=['PUT'])
def renew_book(id):
    res_code = BorrowService.renew_book(id)
    if res_code == -2:
        return render_template('error.html',output='借阅记录不存在')
    if res_code == -1:
        return render_template('error.html',output='无法重复归还')
    if res_code == 0:
        return render_template('error.html',output='借阅逾期，请先归还')
    if res_code == 1:
        return Response.response(ResponseCode.SUCCESS, '续借成功', id)