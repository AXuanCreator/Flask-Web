import math

from flask import Flask, Blueprint, request, render_template

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
				return render_template('error.html',output='信息有误或分类失败')
			case _:
				return render_template('error.html',output='未知错误')

	elif request.method == 'GET':
		# 根据关键词获取多个书籍
		keywords = request.get_json()
		try:
			# 获取页码和每页的数量
			page = int(request.args.get('page', 1))
			per_page = int(request.args.get('per_page', 10))
		except ValueError:
			return render_template('error.html',output='参数错误')

		books, total = BookServices.list_book(keywords, page, per_page)

		if not books:
			return render_template('error.html',output='无符合条件的书籍')
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
			return render_template('error.html',output='未找到书籍')

	elif request.method == 'PUT':
		# 更新书籍信息
		book_request = request.get_json()
		match BookServices.update_book(id, book_request):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '书籍更改成功', Helper.to_dict(Book.query.get(id)))
			case ReturnCode.FAIL:
				return render_template('error.html',output='未找到书籍分类')

	elif request.method == 'DELETE':
		# 删除书籍
		match BookServices.delete_book(id):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '书籍删除成功', id)
			case ReturnCode.BOOK_NOT_EXIST:
				return render_template('error.html',output='未找到书籍分类')
			case ReturnCode.FAIL:
				return render_template('error.html',output='对应书籍分类不存在')

@book_bp.route('/<id>/recommend', methods=['GET'])
def book_recommend(id):
	if request.method == 'GET':
		recommend_list = BookServices.recommend_book(id)

		if recommend_list:
			return Response.response(ResponseCode.SUCCESS, '推荐成功', recommend_list)

		return render_template('error.html',output='推荐失败')