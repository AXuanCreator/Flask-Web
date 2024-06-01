from flask import Flask, Blueprint, request

from Config import ReturnCode, Book
from Utils import Response, ResponseCode, Helper
from .book_services import BookServices

book_bp = Blueprint('book', __name__)


# 创建书籍
@book_bp.route('/', methods=['POST'])
def add_book():
    book_request = request.get_json()
    title = book_request['title']
    author = book_request['author']
    category_id = book_request['category_id']
    publisher = book_request['publisher']
    quantity = book_request['quantity']

    class new_book:
        def __init__(self, title, author, category_id, publisher, quantity):
            self.title = title
            self.author = author
            self.category_id = category_id
            self.publisher = publisher
            self.quantity = quantity

    book = new_book(title, author, category_id, publisher, quantity)

    result = BookServices.insert_book(book)

    latest_book = Book.query.order_by(Book.id.desc()).first()
    latest_book_id = latest_book.id

    match result:
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, '图书添加成功', latest_book_id)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, '连接失败', None)


# 根据id获取单个书籍
@book_bp.route('/<id>', methods=['GET'])
def query_book_id(id):
    book = BookServices.get_book(id)

    if book:
        return Response.response(ResponseCode.SUCCESS, '书籍查找成功', Helper.to_dict(book))
    else:
        return Response.response(ResponseCode.BOOK_NOT_EXIST, '未找到书籍', None)


# 修改书籍
@book_bp.route('/<id>', methods=['PUT'])
def modify_book(id):
    BookServices.update_book(id, request.json)
    result = BookServices.get_book(id)
    return Response.response(ResponseCode.SUCCESS, '书籍更改成功', Helper.to_dict(result))



@book_bp.route('/<id>', methods=['DELETE'])
def delete_book(id):
    match BookServices.delete_book(id):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, '书籍删除成功', id)
        case ReturnCode.BOOK_NOT_EXIST:
            return Response.response(ResponseCode.BOOK_NOT_EXIST, '未找到书籍', None)
