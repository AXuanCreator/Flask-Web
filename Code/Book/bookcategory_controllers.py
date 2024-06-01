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


# 获取类别
# todo 分页
@bookcategory_bp.route('/', methods=['GET'])
def get_book_category():
    categories = BookCategoryServices.get_book_categories()

    categories_list = [{'id': category.id, 'name': category.name, 'quantity': category.quantity, 'creation_date': category.creation_date} for category in categories]

    if categories_list:
        return Response.response(ResponseCode.SUCCESS, '获取全部图书类别', categories_list)
    else:
        return Response.response(ResponseCode.CATEGORY_NOT_EXIST, '图书类别被为空', None)


@bookcategory_bp.route('/<id>', methods=['PUT'])
def update_book_category(id):
    new_name = request.get_json().get('name')

    if BookCategoryServices.get_book_category_by_name(new_name):
        return Response.response(ResponseCode.CATEGORY_EXIST, '书籍类别已经存在,更新失败',
                                 Helper.to_dict(BookCategoryServices.get_book_category_by_name(new_name)))
    book_category = BookCategoryServices.update_book_category(id, new_name)
    new_category = BookCategory.query.get(book_category.id)
    return Response.response(ResponseCode.SUCCESS, '书籍类别更新成功', Helper.to_dict(new_category))


@bookcategory_bp.route('/<id>', methods=['DELETE'])
def delete_book_category(id):
    result = BookCategoryServices.delete_book_category(id)
    match result:
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, '书籍类别删除成功', id)
        case ReturnCode.CATEGORY_NOT_EXIST:
            return Response.response(ResponseCode.CATEGORY_NOT_EXIST, '书籍类别不存在，删除失败', None)

