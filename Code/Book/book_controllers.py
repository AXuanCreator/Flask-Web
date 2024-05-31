from flask import Flask, Blueprint, request

from Config import ReturnCode, Book
from Utils import Response, ResponseCode
from .book_services import BookServices

book_bp = Blueprint('book', __name__)


@book_bp.route('/', methods=['POST'])
def add_book():
    assert request.method == 'POST'

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

    # TODO 获取id的方法有些不妥
    # 获取插入前最后一个插入的书籍的ID
    latest_book = Book.query.order_by(Book.id.desc()).first()
    latest_book_id = latest_book.id

    match BookServices.insert_book(book):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, 'Book added successfully', latest_book_id + 1)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, 'Bad request', None)


@book_bp.route('/<id>', methods=['GET'])
def get_book(id):
    book = BookServices.get_book(id)
    if book:
        return Response.response(ResponseCode.SUCCESS, 'Book found', book)
    else:
        return Response.response(ResponseCode.NOT_FOUND, 'Book not found', None)


@book_bp.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    book_request = request.get_json()
    match BookServices.update_book(id, book_request):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, 'Book updated successfully', None)
        case ReturnCode.BOOK_NOT_FOUND:
            return Response.response(ResponseCode.NOT_FOUND, 'Book not found', None)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, 'Bad request', None)


@book_bp.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    match BookServices.delete_book(id):
        case ReturnCode.SUCCESS:
            return Response.response(ResponseCode.SUCCESS, 'Book deleted successfully', None)
        case ReturnCode.BOOK_NOT_FOUND:
            return Response.response(ResponseCode.NOT_FOUND, 'Book not found', None)
        case _:
            return Response.response(ResponseCode.BAD_REQUEST, 'Bad request', None)
