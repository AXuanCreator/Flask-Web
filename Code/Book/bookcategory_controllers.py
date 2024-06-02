from math import ceil

from flask import Flask, Blueprint, request
from Config import ReturnCode, BookCategory
from Utils import Response, ResponseCode, Helper
from .bookcategory_services import BookCategoryServices

bookcategory_bp = Blueprint('book-category', __name__)


# 添加图书类别
@bookcategory_bp.route('/', methods=['POST'])
def add_book_category():
    data = request.get_json()
    name = data['name']

    result = BookCategoryServices.insert_book_category(name)

    latest_book_category = BookCategory.query.order_by(BookCategory.id.desc()).first()
    latest_book_category_id = latest_book_category.id

    match result:
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, '类别添加成功', latest_book_category_id )
        case ReturnCode.CATEGORY_EXIST:
            return Response.response(ResponseCode.CATEGORY_EXIST, '类别名字重复,添加失败', BookCategory.query.filter_by(name=name).first().id)


# 分页获取类别
@bookcategory_bp.route('/', methods=['GET'])
def query_book_category():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        return Response.response(ResponseCode.FAILED, '参数错误', None)

    categories, total = BookCategoryServices.list_book_categories(page, per_page)

    categories_list = [{'id': category.id, 'name': category.name, 'quantity': category.quantity, 'creation_date': category.creation_date} for category in categories]

    if categories_list:
        total_pages = ceil(total / per_page)
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


# 更新类别名字
@bookcategory_bp.route('/<id>', methods=['PUT'])
def update_book_category(id):
    new_name = request.get_json().get('name')

    if BookCategoryServices.get_book_category_by_name(new_name):
        return Response.response(ResponseCode.CATEGORY_EXIST, '书籍类别已经存在,更新失败',
                                 Helper.to_dict(BookCategoryServices.get_book_category_by_name(new_name)))
    book_category = BookCategoryServices.update_book_category(id, new_name)
    new_category = BookCategory.query.get(book_category.id)
    return Response.response(ResponseCode.SUCCESS, '书籍类别更新成功', Helper.to_dict(new_category))


# 删除
@bookcategory_bp.route('/<id>', methods=['DELETE'])
def delete_book_category(id):
    result = BookCategoryServices.delete_book_category(id)
    match result:
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, '书籍类别删除成功', id)
        case ReturnCode.CATEGORY_NOT_EXIST:
            return Response.response(ResponseCode.CATEGORY_NOT_EXIST, '书籍类别不存在，删除失败', None)

