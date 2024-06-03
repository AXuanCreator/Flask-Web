import math

from flask import Flask, Blueprint, request

from Config import ReturnCode, Book
from Utils import Response, ResponseCode, Helper
from .book_services import BookServices

book_bp = Blueprint('book', __name__)


@book_bp.route('/', methods=['POST', 'GET'])
def book_info():
	if request.method == 'POST':
		# 添加书籍
		book_request = request.get_json()
		match BookServices.insert_book(book_request):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '图书添加成功', Book.query.filter_by(title=book_request.get('title')).first())
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, '信息有误或获取分类失败', None)
			case _:
				return Response.response(ResponseCode.BAD_REQUEST, '连接失败', None)

	elif request.method == 'GET':
		# 根据关键词获取多个书籍
		keywords = request.get_json()
		try:
			# 获取页码和每页的数量
			page = int(request.args.get('page', 1))
			per_page = int(request.args.get('per_page', 10))
		except ValueError:
			return Response.response(ResponseCode.FAILED, '参数错误', None)

		books, total = BookServices.list_book(keywords, page, per_page)

		if not books:
			return Response.response(ResponseCode.BOOK_NOT_EXIST, "无符合条件的书籍", None)
		else:
			total_pages = math.ceil(total / per_page)
			response_data = {
				'books': Helper.to_dict_list(books),
				'total': total,
				'page': page,
				'per_page': per_page,
				'total_pages': total_pages
			}
			return Response.response(ResponseCode.SUCCESS, "书籍查找成功", response_data)


@book_bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def book_operation(id):
	if request.method == 'GET':
		book = BookServices.get_book(id)
		if book:
			return Response.response(ResponseCode.SUCCESS, '书籍查找成功', Helper.to_dict(book))
		else:
			return Response.response(ResponseCode.BOOK_NOT_EXIST, '未找到书籍', None)

	elif request.method == 'PUT':
		# 更新书籍信息
		book_request = request.get_json()
		match BookServices.update_book(id, book_request):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '书籍更改成功', Helper.to_dict(Book.query.get(id)))
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, '未找到书籍分类', None)

	elif request.method == 'DELETE':
		# 删除书籍
		match BookServices.delete_book(id):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '书籍删除成功', id)
			case ReturnCode.BOOK_NOT_EXIST:
				return Response.response(ResponseCode.BOOK_NOT_EXIST, '未找到书籍', None)
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, '对应书籍的分类不存在', None)