from math import ceil

from flask import Blueprint, request
from Config import ReturnCode, BookCategory
from Utils import Response, ResponseCode, Helper
from .bookcategory_services import BookCategoryServices

bookcategory_bp = Blueprint('book-category', __name__)


@bookcategory_bp.route('/', methods=['POST', 'GET'])
def book_category_info():
	if request.method == 'POST':
		# 添加图书类别
		data = request.get_json()
		name = data['name']

		match BookCategoryServices.insert_book_category(name):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '类别添加成功', BookCategory.query.filter_by(name=name).first().id)
			case ReturnCode.CATEGORY_EXIST:
				return Response.response(ResponseCode.CATEGORY_EXIST, '类别名字重复,添加失败', BookCategory.query.filter_by(name=name).first().id)

	elif request.method == 'GET':
		# 分页获取类别
		try:
			page = int(request.args.get('page', 1))  # 页码
			per_page = int(request.args.get('per_page', 10))  # 每页书数
		except ValueError:
			return Response.response(ResponseCode.FAILED, '参数错误', None)

		categories, total = BookCategoryServices.list_book_categories(page, per_page)

		# 将分类载入到列表
		categories_list = [
			{'id': category.id, 'name': category.name, 'quantity': category.quantity, 'create_at': category.create_at}
			for category in categories]

		if categories_list:
			total_pages = ceil(total / per_page)    # 向上取整
			response_data = {
				'categories': categories_list,
				'total': total,
				'page': page,
				'per_page': per_page,
				'total_pages': total_pages
			}
			return Response.response(ResponseCode.SUCCESS, '获取全部图书类别', response_data)
		else:
			return Response.response(ResponseCode.CATEGORY_NOT_EXIST, '图书类别为空', None)


@bookcategory_bp.route('/<id>', methods=['PUT', 'DELETE'])
def book_category_change(id):
	if request.method == 'PUT':
		# 更新分类
		new_name = request.get_json().get('name')

		match BookCategoryServices.update_book_category(id, new_name):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '书籍类别更新成功', Helper.to_dict(BookCategory.query.filter_by(name=new_name).first()))
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, '书籍类别不存在或更改信息有误(重复)', None)

	elif request.method == 'DELETE':
		# 删除分类
		match BookCategoryServices.delete_book_category(id):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, '书籍类别删除成功', id)
			case ReturnCode.CATEGORY_NOT_EXIST:
				return Response.response(ResponseCode.CATEGORY_NOT_EXIST, '书籍类别不存在，删除失败', None)
